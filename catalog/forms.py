from django import forms
from django.core.exceptions import ValidationError
from .models import Product
from .constants import FORBIDDEN_WORDS


class ProductForm(forms.ModelForm):
    """Форма создания/редактирования продукта с полной валидацией"""

    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']

    def __init__(self, *args, **kwargs):
        """Задание 3: стилизация всех полей через __init__"""
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                # Чекбокс как элемент формы (критерий оценки)
                field.widget.attrs.update({
                    'class': 'form-check-input',
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Введите описание продукта',
                })
            elif isinstance(field.widget, forms.ClearableFileInput):
                field.widget.attrs.update({
                    'class': 'form-control',
                    'accept': 'image/jpeg,image/png',
                })
            else:
                field.widget.attrs.update({
                    'class': 'form-control',
                })

    def _check_forbidden_words(self, value):
        """Проверка на запрещённые слова (регистронезависимо)"""
        if not value:
            return value
        value_lower = value.lower()
        for word in FORBIDDEN_WORDS:
            if word.lower() in value_lower:
                raise ValidationError(
                    f'Обнаружено запрещённое слово: "{word}". '
                    f'Пожалуйста, удалите его из текста.'
                )
        return value

    def clean_name(self):
        """Задание 1: валидация названия"""
        name = self.cleaned_data.get('name')
        return self._check_forbidden_words(name)

    def clean_description(self):
        """Задание 1: валидация описания"""
        description = self.cleaned_data.get('description')
        return self._check_forbidden_words(description)

    def clean_price(self):
        """Задание 2: цена не может быть отрицательной"""
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise ValidationError(
                f'Цена продукта не может быть отрицательной. '
                f'Вы ввели: {price}. Введите корректную стоимость.'
            )
        return price

    def clean_image(self):
        """Дополнительное задание: проверка формата и размера изображения"""
        image = self.cleaned_data.get('image')
        if not image:
            return image

        # Проверка формата (только JPEG и PNG)
        allowed_extensions = ['jpg', 'jpeg', 'png']
        ext = image.name.split('.')[-1].lower()
        if ext not in allowed_extensions:
            raise ValidationError(
                f'Недопустимый формат изображения: .{ext}. '
                f'Разрешены только JPEG и PNG.'
            )

        # Проверка размера (максимум 5 МБ)
        max_size = 5 * 1024 * 1024  # 5 МБ в байтах
        if image.size > max_size:
            size_mb = round(image.size / (1024 * 1024), 2)
            raise ValidationError(
                f'Размер файла слишком большой: {size_mb} МБ. '
                f'Максимально допустимый размер — 5 МБ.'
            )

        return image