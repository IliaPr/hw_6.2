from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse

from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, Contact, Record, Version, Category
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

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

class ProductListView(ListView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        return context


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        return context


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product_list')
    template_name = 'catalog/product_form_with_version.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)

        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)




class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:product_list')



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
