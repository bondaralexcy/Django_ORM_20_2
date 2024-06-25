from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import (
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    ContactsPageViews,
    Homepage,
)

app_name = CatalogConfig.name

urlpatterns = [
    path("", Homepage.as_view(), name="home"),
    path("products/", ProductListView.as_view(), name="product_list"),
    path("contact/", ContactsPageViews.as_view(), name="contact"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("create_product/", ProductCreateView.as_view(), name="create_product"),
    path(
        "delete_product/<int:pk>/", ProductDeleteView.as_view(), name="delete_product"
    ),
    path("edit_product/<int:pk>/", ProductUpdateView.as_view(), name="edit_product"),
]
