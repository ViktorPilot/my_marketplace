from catalog.models import Category, Product
from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    def handle(self, *args, **kwargs) -> None:
        """Метод загрузки тестовых фикстур категорий и товаров в базу данных из файла"""
        Category.objects.all().delete()
        Product.objects.all().delete()
        path_fixtures = 'fixtures/catalog/cat_and_prod.json'
        call_command('loaddata', path_fixtures)
        self.stdout.write(self.style.SUCCESS(f'Данные успешно загружены из {path_fixtures}'))




