from django.urls import path
from catalog.views import ProductListView, ProductDetailView, HomeListView, ContactListView, RecordListView, \
    RecordCreateView, RecordUpdateView, RecordDeleteView, RecordDetailView, toggle_activity
from catalog.apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('contact/', ContactListView.as_view(), name='contact'),
    path('home/', HomeListView.as_view(), name='home'),
    path('product/', ProductListView.as_view(), name='pr_pg'),
    path('product/<pk>/', ProductDetailView.as_view(), name='product'),
    path('records/', RecordListView.as_view(), name='record_list'),
    path('records/<slug:slug>/', RecordDetailView.as_view(), name='record_detail'),
    path('records_create/', RecordCreateView.as_view(), name='create_record'),
    path('records_update/<slug:slug>/', RecordUpdateView.as_view(), name='update_record'),
    path('records_delete/<slug:slug>/', RecordDeleteView.as_view(), name='delete_record'),
    path('toggle/<slug:slug>/', toggle_activity, name='toggle_activity')
]
