from django.urls import path
from catalog.views import ProductListView, ProductDetailView, HomeListView, ContactListView
from catalog.apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('contact/', ContactListView.as_view(), name='contact'),
    path('home/', HomeListView.as_view(), name='home'),
    path('product/', ProductListView.as_view(), name='pr_pg'),
    path('product/<pk>/', ProductDetailView.as_view(), name='product'),
]
