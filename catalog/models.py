from django.db import models, connection
from users.models import User

NULLABLE = {"null": True, "blank": True}


class Category(models.Model):
    """
    Модель для хранения информации о категории продукта
    """

    # objects = None
    name = models.CharField(
        max_length=100,
        verbose_name="Наименование",
        help_text="Введите наименование категории",
    )
    description = models.TextField(
        verbose_name="Описание",
        help_text="Введите описание категории",
        **NULLABLE,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    @classmethod
    def truncate_table_restart_id(cls):
        """Метод очистки таблицы со сбросом автоинкремента счетчика
        Спасибо, Владислав Печеневский"""
        with connection.cursor() as cursor:
            cursor.execute(
                f"TRUNCATE TABLE {cls._meta.db_table} RESTART IDENTITY CASCADE"
            )


class Product(models.Model):
    """
    Модель для хранения информации о продукте
    """

    name = models.CharField(
        max_length=100,
        verbose_name="Наименование",
        help_text="Введите наименование продукта",
    )
    description = models.TextField(
        verbose_name="Описание",
        help_text="Введите описание товара",
        **NULLABLE,
    )
    image = models.ImageField(
        upload_to="catalog/product",
        verbose_name="Изображение",
        help_text="Добавьте изображение товара",
        **NULLABLE,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Категория",
        help_text="Введите категорию товара",
        related_name="product",
    )
    price = models.PositiveIntegerField(
        verbose_name="Цена",
        **NULLABLE,
    )
    created_at = models.DateTimeField(
        null=True,
        verbose_name="Дата создания",
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        null=True,
        verbose_name="Дата последнего изменения",
        auto_now=True,
    )
    is_published = models.BooleanField(default=False, verbose_name="Опубликован")
    owner = models.ForeignKey(
        User, verbose_name="Владелец", on_delete=models.SET_NULL, **NULLABLE
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["name"]

    def __str__(self):
        # Обрезаем описание продукта до 100 символов
        return self.name


class Contact(models.Model):
    """
    Модель для хранения информации о контактах
    """

    name = models.CharField(
        max_length=100,
        verbose_name="Имя",
    )
    phone = models.CharField(
        max_length=50,
        verbose_name="Телефон",
        **NULLABLE,
    )
    message = models.TextField(
        verbose_name="Сообщение",
        **NULLABLE,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"


class Version(models.Model):
    """
    Модель для хранения информации о версиях
    """

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="Продукт"
    )
    number = models.PositiveIntegerField(verbose_name="Номер версии", **NULLABLE)
    name = models.CharField(max_length=100, verbose_name="Название", **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name="Активная")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Версия"
        verbose_name_plural = "Версии"
        ordering = ["number"]
