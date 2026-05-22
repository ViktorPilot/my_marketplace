from django.db import models

from users.models import CustomUser


class Product(models.Model):
    """Класс информации о товарах"""

    name = models.CharField(
        max_length=100, verbose_name="наименование товара", help_text="Введите наименование товара"
    )
    description = models.TextField(
        verbose_name="описание товара", blank=True, null=True, help_text="Введите описание товара"
    )
    image = models.ImageField(upload_to="product/image/", verbose_name="изображение товара", blank=True, null=True)
    category = models.ForeignKey(
        to="Category",
        on_delete=models.SET_NULL,
        verbose_name="категория товара",
        help_text="Введите категорию товара",
        null=True,
        related_name="product",
    )
    price = models.DecimalField(
        verbose_name="цена товара",
        blank=True,
        null=True,
        max_digits=20,
        decimal_places=2,
        help_text="Введите цену товара",
        default=0,
    )
    created_at = models.DateField(auto_now_add=True, verbose_name="дата создания товара", blank=True, null=True)
    updated_at = models.DateField(
        auto_now=True, verbose_name="дата последнего изменения товара", blank=True, null=True
    )
    status = models.BooleanField(verbose_name="статус публикации", default=False)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="product")

    def __str__(self) -> str:
        """Магический метод, возвращающий название товара"""
        return f"{self.name}"

    class Meta:
        """Класс метаданных для товаров"""

        verbose_name = "товар"
        verbose_name_plural = "товары"
        ordering = ["id"]
        db_table = "products"
        permissions = [
            ("can_unpublish_product", "Can unpublish product"),
        ]


class Category(models.Model):
    """Класс информации о категориях товаров"""

    name = models.CharField(
        max_length=100, verbose_name="наименование категории товара", help_text="Введите наименование категории товара"
    )
    description = models.TextField(verbose_name="описание категории товара", blank=True, null=True)

    def __str__(self) -> str:
        """Магический метод, возвращающий название категории товара"""
        return f"{self.name}"

    class Meta:
        """Класс метаданных для категорий товаров"""

        verbose_name = "категория"
        verbose_name_plural = "категории"
        ordering = ["id"]
        db_table = "category"


class Contact(models.Model):
    """Класс информации о контактах"""

    name = models.CharField(max_length=100, verbose_name="название компании")
    email = models.TextField(verbose_name="почта")
    number = models.TextField(verbose_name="номер телефона")

    def __str__(self) -> str:
        """Магический метод, возвращающий имя контакта"""
        return f"{self.name}"

    class Meta:
        """Класс метаданных для контактов"""

        verbose_name = "контакты"
        verbose_name_plural = "контакты"
        db_table = "contact"
