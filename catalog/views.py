from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from catalog.models import Product


def home(request: HttpRequest) -> HttpResponse:
    """Функция, рендерирующая страницу 'home'"""
    last_prod = Product.objects.order_by('-id')[:5]
    for i in last_prod:
        print(f'Товар: {i.name}, создан: {i.created_at}')
    return render(request, "catalog/home.html")


def contacts(request: HttpRequest) -> HttpResponse:
    """Функция, рендерирующая страницу 'contacts'"""
    return render(request, "catalog/contacts.html")


def contacts_post(request: HttpRequest) -> HttpResponse:
    """Функция, рендерирующая ответ пользователю на его POST сообщение"""
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        return HttpResponse(f"Данные пользователя {name} ({phone, message}) успешно приняты)!")
    return render(request, "catalog/contacts.html")
