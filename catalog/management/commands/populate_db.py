import os
from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Product, Category


class Command(BaseCommand):
    help = 'Очищает базу данных и загружает тестовые данные из фикстур'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('⚠️ Начинаем очистку базы данных...'))

        # 1. Предварительное удаление данных
        Product.objects.all().delete()
        Category.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('✅ База данных очищена.'))
        self.stdout.write(self.style.WARNING('📦 Начинаем загрузку фикстур...'))

        # 2. Используем существующие фикстуры через call_command
        fixtures_dir = os.path.join('catalog', 'fixtures')

        # Загружаем категории, затем продукты (важен порядок из-за ForeignKey!)
        call_command('loaddata', os.path.join(fixtures_dir, 'categories.json'))
        call_command('loaddata', os.path.join(fixtures_dir, 'products.json'))

        # 3. Выводим результат
        categories_count = Category.objects.count()
        products_count = Product.objects.count()

        self.stdout.write(self.style.SUCCESS('🎉 Данные успешно загружены!'))
        self.stdout.write(f'   Категорий в базе: {categories_count}')
        self.stdout.write(f'   Продуктов в базе: {products_count}')
