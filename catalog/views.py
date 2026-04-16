from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404

from catalog.models import Contact, Product, Category


def home(request: HttpRequest) -> HttpResponse:
    """Функция, рендерирующая страницу 'home' и отображающая в консоли пять крайних добавленных товаров"""
    last_prod = Product.objects.order_by("-id")[:5]
    products = Product.objects.all()
    context ={'products': products}
    for i in last_prod:
        print(f"Товар: {i.name}, создан: {i.created_at}")
    return render(request, "catalog/home.html", context)


def contacts(request: HttpRequest) -> HttpResponse:
    """Функция, рендерирующая страницу 'contacts'"""
    contact = Contact.objects.all()
    context = {
        "names": [i.name for i in contact][-3:],
        "emails": [i.email for i in contact][-3:],
        "numbers": [i.number for i in contact][-3:],
    }
    return render(request, "catalog/contacts.html", context=context)


def contacts_post(request: HttpRequest) -> HttpResponse:
    """Функция, рендерирующая ответ пользователю на его POST сообщение"""
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        return HttpResponse(f"Данные пользователя {name} ({phone, message}) успешно приняты)!")
    return render(request, "catalog/contacts.html")

def product_detail(request: HttpRequest, pk: int) -> HttpResponse:
    """Функция, рендерирующая страницу информации детальной информации о товаре"""
    product = get_object_or_404(Product, id=pk)
    context = {'product': product}
    return render(request, 'catalog/product_detail.html', context)

def add_product(request: HttpRequest) -> HttpResponse:
    """Функция добавления товара в базу данных"""
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        image = request.POST.get('image')
        price = request.POST.get('price')
        input_category = request.POST.get('category')
        category = Category.objects.get_or_create(name=input_category)[0]
        Product.objects.create(name=name, description=description, image=image, price=price, category=category)
        return render(request, 'catalog/success_add_product.html')
    return render(request, 'catalog/add_product.html')
