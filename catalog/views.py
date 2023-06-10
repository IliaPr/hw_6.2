from django.shortcuts import render

from catalog.models import Product, Contact
from django.views.generic import ListView, DetailView



# Create your views here.

class HomeListView(ListView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Product.objects.all()
        return context

class ContactListView(ListView):
    model = Contact

def contact_page(request):
    return render(request, 'catalog/contact.html')

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


