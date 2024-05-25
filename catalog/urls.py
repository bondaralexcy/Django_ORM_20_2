from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import index, product_detail, contact

app_name = CatalogConfig.name

urlpatterns = [
    path("", index, name="index"),
    path("contact/", contact, name="contact"),
    path("catalog/<int:pk>/", product_detail, name="product_detail"),
]
