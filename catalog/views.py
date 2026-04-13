from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from catalog.models import Contact, Product


def home(request: HttpRequest) -> HttpResponse:
    """Функция, рендерирующая страницу 'home' и отображающая в консоли пять крайних добавленных товаров"""
    last_prod = Product.objects.order_by("-id")[:5]
    for i in last_prod:
        print(f"Товар: {i.name}, создан: {i.created_at}")
    return render(request, "catalog/home.html")


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
