from django.urls import path
from catalog.views import home_page, contact_page, product
from catalog.apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path('', home_page, name='home'),
    path('contact/', contact_page, name='contact'),
    path('home/', home_page, name='home'),
    path('product/', product, name='pr_pg'),
    path('product/<pk>/', product, name='product'),
]
