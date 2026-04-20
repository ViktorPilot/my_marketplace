from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse


from catalog.models import Category, Contact, Product


class ProductListView(ListView):
    """Класс объекта списка товаров"""
    model = Product

    def print_list_product(self):
        """Метод выводит в консоль пять крайних добавленных товаров"""
        for i in self.get_queryset().order_by("id").reverse()[:5]:
            print(f"Товар: {i.name}, создан: {i.created_at}")

    def get_context_data(self, **kwargs):
        """Метод добавляет пагинатор в контекст для постраничного просмотра товаров"""
        context = super().get_context_data()
        paginator = Paginator(self.get_queryset(), 3)
        page_number = self.request.GET.get("page")
        context['object_list'] = paginator.get_page(page_number)
        self.print_list_product()
        return context


class ContactListView(ListView):
    """Класс объекта списка контактов"""
    model = Contact

    def post(self, request):
        """Метод рендирующий ответ об успешном приеме контакта пользователя"""
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        return HttpResponse(f"Данные пользователя {name} ({phone, message}) успешно приняты)!")

    def get_queryset(self):
        """Метод выводит на страницу 'contact_list' три первых контакта из базы данных"""
        self.queryset = super().get_queryset().order_by('id')[:3]
        return self.queryset

class ProductDetailView(DetailView):
    """Класс объекта подробной информации о товаре"""
    model = Product

class ProductCreateView(CreateView):
    """Класс объекта создания нового товара"""
    model = Product
    fields = ['name', 'description', 'image', 'price', 'category']

    def get_context_data(self, **kwargs):
        """Метод добавляет список всех категорий из базы данных в контекст"""
        context = super().get_context_data()
        context['category'] = Category.objects.all()
        return context

    def get_success_url(self):
        """Метод перенаправляет на страницу информации о созданном товаре"""
        return reverse_lazy("catalog:product_detail", kwargs = {"pk": self.object.pk})
