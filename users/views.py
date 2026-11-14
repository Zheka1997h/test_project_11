from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm


def register_view(request):
    """Регистрация пользователя с отправкой приветственного письма"""
    if request.user.is_authenticated:
        return redirect('catalog:product_list')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Отправка приветственного письма
            send_mail(
                subject='Добро пожаловать в WebShop!',
                message=f'Привет, {user.username}!\n\nСпасибо за регистрацию в нашем магазине.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )

            messages.success(request, 'Регистрация успешна! Теперь вы можете войти.')
            return redirect('users:login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    """Авторизация по email и паролю"""
    if request.user.is_authenticated:
        return redirect('catalog:product_list')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('catalog:product_list')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    """Выход из системы"""
    logout(request)
    messages.info(request, 'Вы вышли из системы.')
    return redirect('catalog:home')


@login_required
def profile_view(request):
    """Просмотр и редактирование профиля (доп. задание)"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль обновлён!')
            return redirect('users:profile')
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'users/profile.html', {'form': form})