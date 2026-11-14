from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product
from blog.models import Post


class Command(BaseCommand):
    help = 'Создаёт группы "Модератор продуктов" и "Контент-менеджер" с необходимыми правами'

    def handle(self, *args, **kwargs):
        # ===== 1. Группа "Модератор продуктов" =====
        moderator_group, created = Group.objects.get_or_create(name='Модератор продуктов')
        if created:
            self.stdout.write(self.style.SUCCESS('Создана группа "Модератор продуктов"'))
        else:
            self.stdout.write('Группа "Модератор продуктов" уже существует')

        # Получаем ContentType для Product и Post
        product_ct = ContentType.objects.get_for_model(Product)
        post_ct = ContentType.objects.get_for_model(Post)

        # Право can_unpublish_product (кастомное)
        can_unpublish_perm = Permission.objects.get(
            codename='can_unpublish_product',
            content_type=product_ct
        )
        # Право на удаление любого продукта (стандартное)
        delete_product_perm = Permission.objects.get(
            codename='delete_product',
            content_type=product_ct
        )
        # Права на управление блогом (для контент-менеджера)
        add_post_perm = Permission.objects.get(codename='add_post', content_type=post_ct)
        change_post_perm = Permission.objects.get(codename='change_post', content_type=post_ct)
        delete_post_perm = Permission.objects.get(codename='delete_post', content_type=post_ct)
        view_post_perm = Permission.objects.get(codename='view_post', content_type=post_ct)

        # Назначаем модератору: can_unpublish_product + delete_product
        moderator_group.permissions.set([can_unpublish_perm, delete_product_perm])
        self.stdout.write(self.style.SUCCESS(
            f'Группе "Модератор продуктов" назначены права: '
            f'{can_unpublish_perm.name}, {delete_product_perm.name}'
        ))

        # ===== 2. Группа "Контент-менеджер" (доп. задание) =====
        content_manager_group, created = Group.objects.get_or_create(name='Контент-менеджер')
        if created:
            self.stdout.write(self.style.SUCCESS('Создана группа "Контент-менеджер"'))
        else:
            self.stdout.write('Группа "Контент-менеджер" уже существует')

        # Назначаем все права на Post
        content_manager_group.permissions.set([
            add_post_perm, change_post_perm, delete_post_perm, view_post_perm
        ])
        self.stdout.write(self.style.SUCCESS(
            f'Группе "Контент-менеджер" назначены права на управление блогом'
        ))

        self.stdout.write(self.style.SUCCESS('\n✅ Все группы и права настроены!'))