# from django.http import HttpResponseRedirect
# from django.shortcuts import render, get_object_or_404
from django.forms import inlineformset_factory
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from django.urls import reverse_lazy, reverse
from pytils.translit import slugify
from catalog.models import Product, Contact, Version
from catalog.forms import ProductForm, VersionForm, VersionFormset
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


class Homepage(TemplateView):
    Model = Contact
    template_name = "catalog/base.html"
    # random_article = Blog.objects.order_by('?')[:3]
    random_article = Contact.objects.all()
    extra_context = {"title": "Новый интернет-магазин"}

    def get_context_data(self, *args, **kwargs):
        # Количество контактов
        context_data = super().get_context_data(*args, **kwargs)
        context_data["total_count"] = Contact.objects.all().count()
        return context_data


# CBV
class ProductListView(LoginRequiredMixin, ListView):
    """
    Контроллер отвечает за отображение списка продуктов
    """

    model = Product
    # template_name = "catalog/index.html"
    # context_object_name = (
    #     "object_list"  # Это было не обязательно. По умолчанию и так object_list
    # )
    extra_context = {"title": "Каталог товаров"}  # Передача статических данных

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        list_product = Product.objects.all()

        for product in list_product:
            version = Version.objects.filter(product=product)
            activ_version = version.filter(is_active=True)
            if activ_version:
                product.active_version = activ_version.last().name
                product.number_version = activ_version.last().number
            else:
                product.active_version = "Нет активной версии"

        context_data["object_list"] = list_product
        return context_data


# CBV
class ProductDetailView(LoginRequiredMixin, DetailView):
    """
    Контроллер отвечает за отображение детальной информации о продукте
    """

    model = Product
    template_name = "catalog/product_detail.html"
    extra_context = {"title": "Информация о товаре"}


class ProductCreateView(LoginRequiredMixin, CreateView):
    """
    Контроллер отвечает за создание продукта
    """

    model = Product
    # fields = ("name", "category", "description", "purchase_price", "image")
    form_class = ProductForm
    success_url = reverse_lazy("catalog:product_list")
    extra_context = {"title": "Новый товар"}

    def form_valid(self, form):
        product = form.save()
        user = self.request.user
        product.owner = user
        product.slug = slugify(product.name)
        product.save()

        return super().form_valid(form)

    # def get_success_url(self):
    #     return reverse('catalog:product_list')


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """
    Контроллер отвечает за изменение продукта
    """

    model = Product
    form_class = ProductForm
    extra_context = {"title": "Внести изменения"}

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        ProductFormset = inlineformset_factory(
            Product, Version, form=VersionForm, formset=VersionFormset, extra=1
        )
        # print(f'Method = {self.request.method}')
        if self.request.method == "POST":
            # Передаем в контекст действия, выполненные в формсете SubjectFormset
            context_data["formset"] = ProductFormset(
                self.request.POST, instance=self.object
            )
        else:
            context_data["formset"] = ProductFormset(instance=self.object)
        return context_data

    def get_success_url(self):
        return reverse("catalog:product_detail", args=[self.kwargs.get("pk")])

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data["formset"]
        if form.is_valid and formset.is_valid():
            new_prod = form.save()
            new_prod.slug = slugify(new_prod.name)
            new_prod.save()

            # self.object = form.save()
            formset.instance = new_prod
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(
                self.get_context_data(form=form, formset=formset)
            )


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """
    Контроллер отвечает за удаление продукта
    """

    model = Product
    success_url = reverse_lazy("catalog:product_list")
    extra_context = {"title": "Удалить товар"}

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner or self.request.user.is_superuser:
            return self.object
        raise PermissionDenied


class ContactsPageViews(CreateView):
    """Сохранить информацию о контакте"""

    model = Contact
    fields = (
        "name",
        "phone",
        "message",
    )
    success_url = reverse_lazy("catalog:contact")
    template_name = "catalog/contact.html"
    extra_context = {"title": "Сохранить контакт"}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        number = len(Contact.objects.all())
        if number > 5:
            context["latest_contacts"] = Contact.objects.all()[number - 5 : number + 1]
        else:
            context["latest_contacts"] = Contact.objects.all()
        return context

    # def post(self, request, *args, **kwargs):
    # # Это метод из предыдущей реализации. Сохраняет данные в csv-файл
    #     name = request.POST.get("name", "")
    #     email = request.POST.get("email", "")
    #     message = request.POST.get("message", "")
    #     print(f"{name} ({email}): {message}")
    #
    #     # with open('contact_info.csv', mode='a', newline='') as file:
    #     #     writer = csv.writer(file)
    #     #     writer.writerow([name, phone, message])
    #
    #     return HttpResponseRedirect(self.request.path)
