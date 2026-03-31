from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def home(request: HttpRequest) -> HttpResponse:
    """Функция, рендерирующая страницу 'home'"""
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
