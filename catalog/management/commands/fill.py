import json
from django.core.management import BaseCommand
from catalog.models import Category, Product

# Кастомная команда, которая умеет заносить данные в базу данных,
# при этом предварительно ее зачищать от старых данных


class Command(BaseCommand):
    @staticmethod
    def json_read_categories():
        """Статический метод чтения данных из json-файла"""
        # Здесь мы получаем данные из фикстуры с категориями
        with open("category.json", encoding="utf-8") as json_file:
            return json.load(json_file)

    @staticmethod
    def json_read_products():
        """Статический метод записи данных  json-файл"""
        # Здесь мы получаем данные из фикстуры с продуктами
        with open("product.json", encoding="utf-8") as json_file:
            return json.load(json_file)


    def handle(self, *args, **options):
        # Cброс автоинкремента
        Category.truncate_table_restart_id()
        # Удалите все продукты
        Product.objects.all().delete()
        # Удалите все категории
        Category.objects.all().delete()

        # Создайте списки для хранения объектов
        product_list = []
        category_list = []

        # Обходим все значения категорий из фиктсуры
        for category in Command.json_read_categories():
            category_list.append(
                Category(
                    id=category["pk"],
                    name=category["fields"]["name"],
                    description=category["fields"]["description"],
                )
            )

        # Создаем объекты в базе с помощью метода bulk_create()
        Category.objects.bulk_create(category_list)
        print("Category - done")

        # Обходим все значения продуктов из фиктсуры
        for product in Command.json_read_products():
            product_list.append(
                Product(
                    id=product["pk"],
                    name=product["fields"]["name"],
                    description=product["fields"]["description"],
                    image=product["fields"]["image"],
                    category=Category.objects.get(pk=product["fields"]["category"]),
                    price=product["fields"]["price"],
                    created_at=product["fields"]["created_at"],
                    updated_at=product["fields"]["updated_at"],
                )
            )

        # Создаем объекты в базе с помощью метода bulk_create()
        Product.objects.bulk_create(product_list)
