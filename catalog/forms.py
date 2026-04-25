from django.core.exceptions import ValidationError
from django import forms

from catalog.models import Product

PROHIBITED_WORDS = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']


class ProductForms(forms.ModelForm):
    """Класс формы для модели товаров"""

    class Meta:
        """Класс метаданных для формы модели товаров"""
        model = Product
        exclude = ['created_at', 'updated_at', ]

    def __init__(self, *args, **kwargs):
        """Пепеопределение метода с добавлением пользовательского стиля"""
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'rows': '3'})

    def clean_name(self) -> str:
        """Метод проверяет наличие запрещенных слов при вводе пользователем названия товара"""
        name = self.cleaned_data.get('name')
        for word in name.lower().split():
            if word in PROHIBITED_WORDS:
                raise ValidationError(f'Слово "{word}" является запрещенным')
        return name

    def clean_description(self) -> str:
        """Метод проверяет наличие запрещенных слов при вводе пользователем описания товара"""
        description = self.cleaned_data.get('description')
        for word in description.lower().split():
            if word in PROHIBITED_WORDS:
                raise ValidationError(f'Слово "{word}" является запрещенным')
        return description

    def clean_price(self) -> int:
        """Метод проверяет, что пользователь ввел положительную цену товара"""
        price = self.cleaned_data.get('price')
        if price < 0:
            raise ValidationError('Цена не может быть отрицательной')
        return price

    def clean_image(self) -> str:
        """Метод проверяет на соответствие максимальному размеру файла"""
        image = self.cleaned_data.get('image')
        if image:
            if not str(image).endswith((".jpg", ".png")):
                raise ValidationError('Ошибка: Формат изображения не поддерживается')
            if image.size > 1024 * 1024 * 5:
                raise ValidationError('Ошибка: Размер файла больше 5 Мб')
        return image
