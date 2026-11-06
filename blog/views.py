from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post
from django.core.mail import send_mail
from django.conf import settings


class PostListView(ListView):
    """Список блоговых записей (только опубликованные)"""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        """Фильтрация: только опубликованные статьи"""
        return Post.objects.filter(is_published=True)


class PostDetailView(DetailView):
    """Детальная страница статьи + увеличение счётчика просмотров"""
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        post.views_count += 1
        post.save(update_fields=['views_count'])

        # Отправка письма при достижении 100 просмотров
        if post.views_count == 100:
            send_mail(
                subject=f'🎉 Статья "{post.title}" набрала 100 просмотров!',
                message=f'Поздравляем! Статья "{post.title}" достигла 100 просмотров.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=True,
            )

        return post

    def get_object(self, queryset=None):
        """Переопределяем: увеличиваем views_count при просмотре"""
        post = super().get_object(queryset)
        post.views_count += 1
        post.save(update_fields=['views_count'])
        return post


class PostCreateView(CreateView):
    """Создание новой статьи"""
    model = Post
    fields = ['title', 'content', 'preview', 'is_published']
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:post_list')


class PostUpdateView(UpdateView):
    """Редактирование статьи"""
    model = Post
    fields = ['title', 'content', 'preview', 'is_published']
    template_name = 'blog/post_form.html'

    def get_success_url(self):
        """Перенаправление на страницу отредактированной статьи"""
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.pk})


class PostDeleteView(DeleteView):
    """Удаление статьи"""
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')