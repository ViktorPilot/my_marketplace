from django.urls import path

from catalog import views
from catalog.apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path("home/", views.ProductListView.as_view(), name="home"),
    path("contacts/", views.ContactListView.as_view(), name="contacts"),
    path("product_detail/<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"),
    path("add_product/", views.ProductCreateView.as_view(), name="add_product"),
]
