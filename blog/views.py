from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post


def is_content_manager(user):
    """Проверка: пользователь — контент-менеджер"""
    return user.groups.filter(name='Контент-менеджер').exists()


class ContentManagerRequiredMixin(LoginRequiredMixin):
    """Миксин: доступ только для контент-менеджеров"""
    login_url = 'users:login'

    def dispatch(self, request, *args, **kwargs):
        if not is_content_manager(request.user):
            messages.error(request, 'Доступ разрешён только контент-менеджерам.')
            return redirect('blog:post_list')
        return super().dispatch(request, *args, **kwargs)


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(is_published=True)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.view_count += 1
        obj.save()

        if obj.view_count == 100:
            send_mail(
                subject='🎉 Поздравляем! Статья набрала 100 просмотров!',
                message=f'Ваша статья "{obj.title}" только что достигла отметки в 100 просмотров.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=False,
            )
        return obj


class PostCreateView(ContentManagerRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'preview', 'is_published']
    success_url = reverse_lazy('blog:post_list')


class PostUpdateView(ContentManagerRequiredMixin, UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'preview', 'is_published']

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.pk})


class PostDeleteView(ContentManagerRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')