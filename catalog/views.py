from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Product, Contact
from .forms import ProductForm


class HomeView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = Product.objects.order_by('-created_at')[:5]
        print("\n=== Последние 5 продуктов ===")
        for product in queryset:
            print(f"Продукт: {product.name} | Цена: {product.price} | Категория: {product.category.name}")
        print("=============================\n")
        return queryset


class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contacts'] = Contact.objects.all()
        return context


class ProductListView(ListView):
    """Список всех продуктов — ДОСТУПЕН ВСЕМ (критерий)"""
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'


@method_decorator(login_required, name='dispatch')
class ProductDetailView(DetailView):
    """Детальная страница — только для авторизованных"""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


@method_decorator(login_required, name='dispatch')
class ProductCreateView(CreateView):
    """Создание — только для авторизованных"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')


@method_decorator(login_required, name='dispatch')
class ProductUpdateView(UpdateView):
    """Редактирование — только для авторизованных"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})


@method_decorator(login_required, name='dispatch')
class ProductDeleteView(DeleteView):
    """Удаление — только для авторизованных"""
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')