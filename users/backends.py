####
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class EmailBackend(ModelBackend):
    """Бэкенд аутентификации по email вместо username"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        # username здесь — это email (из формы входа)
        email = username
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None