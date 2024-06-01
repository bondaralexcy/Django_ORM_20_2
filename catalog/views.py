from django.http import HttpResponseRedirect

from django.shortcuts import render, get_object_or_404
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from pytils.translit import slugify
from catalog.models import Product


# CBV
class ProductListView(ListView):
    model = Product
    template_name = "catalog/index.html"
    context_object_name = (
        "object_list"  # Это было не обязательно. По умолчанию и так object_list
    )
    extra_context = {"title": "Главная"}  # Передача статических данных


# CBV
class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    extra_context = {"title": "Информация о товаре"}


# CBV
class ContactView(TemplateView):
    """Класс-контроллер отображения страницы контактов"""

    template_name = "catalog/contact.html"
    extra_context = {"title": "Контакты"}

    def post(self, request, *args, **kwargs):
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        message = request.POST.get("message", "")
        print(f"{name} ({email}): {message}")

        # with open('contact_info.csv', mode='a', newline='') as file:
        #     writer = csv.writer(file)
        #     writer.writerow([name, phone, message])

        return HttpResponseRedirect(self.request.path)


class ProductCreateView(CreateView):
    model = Product
    fields = ("name", "category", "description", "purchase_price", "image")
    success_url = reverse_lazy("catalog:products")

    def form_valid(self, form):
        if form.is_valid():
            new_prod = form.save()
            new_prod.slug = slugify(new_prod.name)
            new_prod.save()

        return super().form_valid(form)


class ProductUpdateView(UpdateView):
    model = Product
    fields = ("name", "category", "description", "purchase_price", "image")
    success_url = reverse_lazy("catalog:products")

    def form_valid(self, form):
        if form.is_valid():
            new_prod = form.save()
            new_prod.slug = slugify(new_prod.name)
            new_prod.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("catalog:specific_product", args=[self.kwargs["pk"]])


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:products")
