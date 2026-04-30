from typing import Any

from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from catalog.forms import ProductForms
from catalog.models import Category, Contact, Product


class ProductListView(ListView):
    """Класс контроллера списка товаров"""

    model = Product

    def print_list_product(self) -> None:
        """Метод выводит в консоль пять крайних добавленных товаров"""
        for i in self.get_queryset().order_by("id").reverse()[:5]:
            print(f"Товар: {i.name}, создан: {i.created_at}")

    def get_context_data(self, **kwargs: Any) -> dict:
        """Метод добавляет пагинатор в контекст для постраничного просмотра товаров"""
        context = super().get_context_data()
        paginator = Paginator(self.get_queryset(), 3)
        page_number = self.request.GET.get("page")
        context["object_list"] = paginator.get_page(page_number)
        self.print_list_product()
        return context


class ContactListView(LoginRequiredMixin, ListView):
    """Класс контроллера списка контактов"""

    model = Contact

    def post(self, request: HttpRequest) -> HttpResponse:
        """Метод рендирующий ответ об успешном приеме контакта пользователя"""
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        return HttpResponse(f"Данные пользователя {name} ({phone, message}) успешно приняты)!")

    def get_queryset(self) -> QuerySet[Contact]:
        """Метод выводит на страницу 'contact_list' три первых контакта из базы данных"""
        self.queryset = super().get_queryset().order_by("id")[:3]
        return self.queryset


class ProductDetailView(LoginRequiredMixin, DetailView):
    """Класс контроллера подробной информации о товаре"""

    model = Product


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Класс контроллера создания нового товара"""

    model = Product
    form_class = ProductForms

    def get_context_data(self, **kwargs: Any) -> dict:
        """Метод добавляет список всех категорий из базы данных в контекст"""
        context = super().get_context_data()
        context["category"] = Category.objects.all()
        return context

    def get_success_url(self) -> str:
        """Метод перенаправляет на страницу информации о созданном товаре"""
        return reverse_lazy("catalog:product_detail", kwargs={"pk": self.object.pk})


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Класс контроллера создания нового товара"""

    model = Product
    form_class = ProductForms

    def get_context_data(self, **kwargs: Any) -> dict:
        """Метод добавляет список всех категорий из базы данных в контекст"""
        context = super().get_context_data()
        context["category"] = Category.objects.all()
        return context

    def get_success_url(self) -> str:
        """Метод перенаправляет на страницу информации о созданном товаре"""
        return reverse_lazy("catalog:product_detail", kwargs={"pk": self.object.pk})


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Класс контроллера создания нового товара"""

    model = Product
    success_url = reverse_lazy("catalog:home")
