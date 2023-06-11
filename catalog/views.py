from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse

from catalog.models import Product, Contact, Record
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView


# Create your views here.

class HomeListView(ListView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Product.objects.all()
        return context

class ContactListView(ListView):
    model = Contact

#def contact_page(request):
    #return render(request, 'catalog/contact.html')

class ProductListView(ListView):
    model = Product

class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        context['desc'] = self.object.description
        context['category'] = self.object.category
        context['price'] = self.object.price
        context['create_date'] = self.object.create_date
        context['change_date'] = self.object.change_date
        return context

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
