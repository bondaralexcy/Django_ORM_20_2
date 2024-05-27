from django.db import models, connection

NULLABLE = {"null": True, "blank": True}


class Category(models.Model):
    # objects = None
    name = models.CharField(
        max_length=100,
        verbose_name="Наименование",
    )
    description = models.TextField(
        verbose_name="Описание",
        **NULLABLE,
    )

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

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Наименование",
        help_text="Введите наименование продукта",
    )
    description = models.TextField(
        verbose_name="Описание",
        **NULLABLE,
    )
    image = models.ImageField(
        upload_to="catalog/product",
        verbose_name="Изображение",
        **NULLABLE,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Категория",
        related_name="product",
    )
    price = models.PositiveIntegerField(
        verbose_name="Цена",
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

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["name"]

    def __str__(self):
        # Обрезаем описание продукта до 100 символов
        return f"{self.name} - {self.description}. Цена: {self.price}"
