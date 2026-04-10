from django.core.management import call_command
from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    def handle(self, *args: str, **kwargs: dict) -> None:
        """Метод загрузки тестовых фикстур категорий и товаров в базу данных из файла"""
        Category.objects.all().delete()
        Product.objects.all().delete()
        path_fixtures = "fixtures/catalog/cat_and_prod.json"
        call_command("loaddata", path_fixtures)
        self.stdout.write(self.style.SUCCESS(f"Данные успешно загружены из {path_fixtures}"))
