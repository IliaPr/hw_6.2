from django.urls import path
from catalog.views import home_page, contact_page
from catalog.apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path('', home_page, name='home'),
    path('contact/', contact_page, name='contact'),
]