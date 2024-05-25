from django.shortcuts import render, get_object_or_404
from catalog.models import Product


def index(request):
    products_list = Product.objects.all()
    # print(products_list)
    context = {
        'object_list': products_list,
        'title': 'Главная страница'
    }
    return render(request, "catalog/index.html", context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {'product': product,
               'title': 'Информация о товаре'
               }
    return render(request, "catalog/product_detail.html", context)


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        print(f"{name} ({email}): {message}")

    context = {'title': 'Контакты'}
    return render(request, "catalog/contact.html", context)