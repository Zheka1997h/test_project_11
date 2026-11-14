from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib import messages
from .models import Product, Contact
from .forms import ProductForm


class HomeView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        # Показываем только опубликованные продукты на главной
        return Product.objects.filter(is_published=True).order_by('-created_at')[:5]


class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contacts'] = Contact.objects.all()
        return context


class ProductListView(ListView):
    """Список продуктов — доступен всем, но только опубликованные"""
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(is_published=True)


@method_decorator(login_required, name='dispatch')
class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        user = self.request.user

        # Проверяем права для отображения кнопок
        is_owner = product.owner == user
        is_moderator = user.groups.filter(name='Модератор продуктов').exists()
        can_edit = is_owner or is_moderator
        can_unpublish = is_moderator and user.has_perm('catalog.can_unpublish_product')

        context['can_edit'] = can_edit
        context['can_delete'] = can_edit
        context['can_unpublish'] = can_unpublish
        context['is_owner'] = is_owner
        return context


@method_decorator(login_required, name='dispatch')
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        # Автоматически заполняем owner текущим пользователем
        form.instance.owner = self.request.user
        # По умолчанию новый продукт не опубликован (ждёт модерации)
        form.instance.is_published = False
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})

    def dispatch(self, request, *args, **kwargs):
        """Проверка: редактировать может только владелец или модератор"""
        product = self.get_object()
        is_owner = product.owner == request.user
        is_moderator = request.user.groups.filter(name='Модератор продуктов').exists()

        if not (is_owner or is_moderator):
            messages.error(request, 'У вас нет прав для редактирования этого продукта.')
            return redirect('catalog:product_detail', pk=product.pk)
        return super().dispatch(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')

    def dispatch(self, request, *args, **kwargs):
        """Удалять может владелец или модератор"""
        product = self.get_object()
        is_owner = product.owner == request.user
        is_moderator = request.user.groups.filter(name='Модератор продуктов').exists()

        if not (is_owner or is_moderator):
            messages.error(request, 'У вас нет прав для удаления этого продукта.')
            return redirect('catalog:product_detail', pk=product.pk)
        return super().dispatch(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class ProductUnpublishView(View):
    """Отмена публикации продукта — только для модераторов"""

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)

        # Проверяем право can_unpublish_product
        if not request.user.has_perm('catalog.can_unpublish_product'):
            messages.error(request, 'У вас нет прав для отмены публикации.')
            return redirect('catalog:product_detail', pk=product.pk)

        product.is_published = False
        product.save()
        messages.success(request, f'Публикация продукта "{product.name}" отменена.')
        return redirect('catalog:product_detail', pk=product.pk)