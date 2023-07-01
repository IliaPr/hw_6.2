from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, Contact, Record, Version, Category
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin

# Create your views here.

class AuthRequiredMixin(LoginRequiredMixin):
    login_url = '/login/'
class HomeListView(ListView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Product.objects.all()
        return context

class ContactListView(ListView):
    model = Contact

class ProductListView(LoginRequiredMixin, generic.ListView):
    model = Product
    extra_context = {'title': 'Список продукции', 'object_list': Product.objects.filter(status='Активна')}

    def get_object(self, queryset=None):
        return self.request.user

class ProductDetailView(LoginRequiredMixin,  generic.DetailView):
    model = Product
    permission_required = 'catalog.view_product'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = context_data['object']
        context_data['versions'] = Version.objects.filter(name_of_product=self.object, actual_version=True)
        return context_data

class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Product
    fields = ('name', 'description', 'preview', 'category', 'price', 'date_create', 'date_change', 'status', 'creator')
    success_url = reverse_lazy('main:product_list')
    permission_required = 'catalog.add_product'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form_with_formset.html'
    success_url = reverse_lazy('main:product_list')
    permission_required = 'catalog.change_product'

    def get_success_url(self, *args, **kwargs):
        return reverse('main:product_update', args=[self.get_object().pk])

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.user != self.request.user and not self.request.user.is_staff:
            raise Http404("Вы не являетесь владельцем этого товара")
        return self.object

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)
class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Product
    success_url = reverse_lazy('main:product_list')
    def test_func(self):
        return self.request.user.is_superuser

    def get_object(self, queryset=None):
        return self.request.user



class RecordListView(ListView):
    model = Record
    queryset = Record.objects.filter(published=True)


class RecordCreateView(CreateView):
    model = Record
    fields = ('title', 'content', 'preview', 'published')
    success_url = reverse_lazy('catalog:record_list')


class RecordUpdateView(UpdateView):
    model = Record
    fields = ('title', 'slug', 'content', 'preview', 'published', 'views_count')

class RecordDetailView(DetailView):
    model = Record

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        obj.views_count += 1
        obj.save()
        return obj
    def get_success_url(self):
        return self.object.get_absolute_url()


class RecordDeleteView(DeleteView):
    model = Record
    success_url = reverse_lazy('catalog:record_list')
    #def toggle_activity(request, slug):
        #record_item = get_object_or_404(Record, slug=slug)
        #record_item.toggle_published()
        #return redirect(reverse('catalog:record_detail', args=[record_item.slug]))


def toggle_activity(request, slug):
    record_item = get_object_or_404(Record, slug=slug)
    record_item.toggle_published()
    return redirect(reverse('catalog:record_detail', args=[record_item.slug]))
