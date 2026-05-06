from django.core.management import BaseCommand, call_command
from django.contrib.auth.models import Group

class Command(BaseCommand):
    def handle(self, *args: str, **kwargs: dict) -> None:
        """Метод загрузки тестовых фикстур групп в базу данных из файла"""
        Group.objects.all().delete()
        path_fixtures = "fixtures/auth/groups.json"
        call_command("loaddata", path_fixtures)
        self.stdout.write(self.style.SUCCESS(f"Данные успешно загружены из {path_fixtures}"))
