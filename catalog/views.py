from django.shortcuts import render

# Create your views here.
def home_page(request):
    return render(request, 'catalog/home.html')

def contact_page(request):
    return render(request, 'catalog/contact.html')
