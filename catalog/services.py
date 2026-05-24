from django.db.models import QuerySet

from catalog.models import Product


def get_category_products(category_id: int = 1) -> QuerySet[Product]:
    """Метод фильтрует товары по заданной пользователем категории"""
    return Product.objects.filter(category_id=category_id)
