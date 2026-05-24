from django.urls import path
from django.views.decorators.cache import cache_page

from catalog import views
from catalog.apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path("home/", views.ProductListView.as_view(), name="home"),
    path("contacts/", views.ContactListView.as_view(), name="contacts"),
    path("product_detail/<int:pk>/", cache_page(60)(views.ProductDetailView.as_view()), name="product_detail"),
    path("add_product/", views.ProductCreateView.as_view(), name="add_product"),
    path("update_product/<int:pk>/", views.ProductUpdateView.as_view(), name="update_product"),
    path("delete_product/<int:pk>/", views.ProductDeleteView.as_view(), name="delete_product"),
    path("home_filter/<int:category_id>/", views.ProductFilterListView.as_view(), name="home_filter"),
]
