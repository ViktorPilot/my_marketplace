from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Permission
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from catalog.forms import ProductForms
from catalog.models import Category, Contact, Product
from catalog.services import get_category_products
from config.settings import CACHE_ENABLE


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

    def get_queryset(self) -> QuerySet[Product]:
        """Метод отфильтровывает вывод товаров на главную страницу по заданному статусу публикации True,
        а также добавляет и извлекает из кэша главную страницу"""
        key = "list_products"
        cache_data = cache.get(key)

        if not CACHE_ENABLE:
            return Product.objects.filter(status=True)

        if cache_data is not None:
            return cache_data

        products_list = Product.objects.filter(status=True)
        cache.set(key, products_list, 60)
        return products_list


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

    def get_context_data(self, **kwargs: Any) -> dict:
        """Метод добавляет список всех групп пользователя из базы данных в контекст"""
        context = super().get_context_data()
        context["user_groups"] = self.request.user.groups.values_list("name", flat=True)
        return context


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

    def form_valid(self, form) -> Any:
        status = form.cleaned_data["status"]
        user = self.request.user
        form.instance.owner = user
        if not user.has_perm("catalog.can_unpublish_product") and status:
            raise PermissionDenied
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Класс контроллера создания нового товара"""

    model = Product
    form_class = ProductForms
    permission_required = "catalog.change_product"

    def form_valid(self, form) -> Any:
        """Метод ограничивает права доступа для изменения товара всех пользователей, кроме владельца и модератора"""
        user = self.request.user
        if user == form.instance.owner or user.groups.filter(name="moderators").exists():
            change_product = Permission.objects.get(codename="change_product")
            user.user_permissions.add(change_product)
            return super().form_valid(form)
        raise PermissionDenied

    def get_context_data(self, **kwargs: Any) -> dict:
        """Метод добавляет список всех категорий из базы данных в контекст"""
        context = super().get_context_data()
        context["category"] = Category.objects.all()
        return context

    def get_success_url(self) -> str:
        """Метод перенаправляет на страницу информации о созданном товаре"""
        return reverse_lazy("catalog:product_detail", kwargs={"pk": self.object.pk})


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Класс контроллера удаления товара"""

    model = Product
    success_url = reverse_lazy("catalog:home")
    permission_required = "catalog.delete_product"

    def post(self, request, *args, **kwargs):
        """Метод ограничивает права доступа для удаления товаров всех пользователей кроме владельца товара,
        и модераторов"""
        user = self.request.user
        obj = self.get_object()
        if user.email == obj.owner.email or user.groups.filter(name="moderators").exists():
            delete_product = Permission.objects.get(codename="delete_product")
            user.user_permissions.add(delete_product)
            return super().post(request, *args, **kwargs)
        raise PermissionDenied


class ProductFilterListView(ListView):
    """Класс контроллера списка товаров, отфильтрованных по категории"""

    model = Product
    template_name = "product_filter_list"

    def get_context_data(self, **kwargs: Any) -> dict:
        """Метод добавляет пагинатор в контекст для постраничного просмотра отфильтрованных товаров"""
        context = super().get_context_data()
        paginator = Paginator(self.get_queryset(), 3)
        page_number = self.request.GET.get("page")
        context["object_list"] = paginator.get_page(page_number)
        return context

    def get_queryset(self) -> QuerySet[Product]:
        """Метод отфильтровывает вывод товаров на главную страницу
        по заданному статусу публикации True и заданной категории"""
        category_id = self.kwargs["category_id"]
        product_filter = get_category_products(category_id)
        return product_filter.filter(status=True)
