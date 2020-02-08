# Authentication

- Built-in
    * django.contrib.auth.urls
    * override default login template => registration/login.html
    * scratch LoginView, LogoutView, SignUpView
    * settings.
        LOGIN_REDIRECT_URL
        LOGOUT_REDIRECT_URL
        LOGIN_URL

- Custom User Model
    - using email field as identification instead of username field
    - PermissionsMixin
    - settings.AUTH_USER_MODEL
    - get_user_model()

- Authorization
    - PermissionRequiredMixin


# Packages
- markdown2
- django-bootstrap3
- django-braces


# Changes from the original

- misaka -> markdown2
- change import User: django.contrib.auth.models.User -> User = get_user_model()
- Typo: communities.views.py: Permissions -> Permission
- 不具合: Community名にascii以外を使用するとslugが""になる（unicode-slugify）
