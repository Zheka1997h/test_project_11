####
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Настройка отображения кастомной модели пользователя в админ-панели"""

    # 1. Поля, которые будут видны в общем списке пользователей
    list_display = ('email', 'username', 'phone', 'country', 'is_staff', 'is_active')

    # 2. Фильтры в правой колонке админки
    list_filter = ('is_staff', 'is_active', 'country')

    # 3. Поля, по которым работает поиск (лупа сверху)
    search_fields = ('email', 'username', 'phone')

    # 4. Сортировка по умолчанию
    ordering = ('email',)

    # 5. Группировка полей при РЕДАКТИРОВАНИИ существующего пользователя
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Персональная информация', {'fields': ('username', 'avatar', 'phone', 'country')}),
        ('Права доступа', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',),  # Сворачиваем этот блок, чтобы не мешал
        }),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )

    # 6. Группировка полей при СОЗДАНИИ нового пользователя через админку
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'phone', 'country'),
        }),
    )
