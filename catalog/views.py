from django.views.generic import ListView, TemplateView
from .models import Product, Contact

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