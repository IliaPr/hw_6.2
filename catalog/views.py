from django.shortcuts import render

from catalog.models import Product


# Create your views here.
def home_page(request):
    context = {
        'object_list': Product.objects.all()
    }
    return render(request, 'catalog/home.html', context)

def contact_page(request):
    return render(request, 'catalog/contact.html')

def product(request, pk):
    product_item = Product.objects.get(pk=pk)
    context = {
        'title': product_item.name,
        'desc': product_item.description,
    }
    return render(request, 'catalog/product.html', context)
