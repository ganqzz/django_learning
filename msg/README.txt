# Authentication

- Built-in
    * django.contrib.auth.urls
    * override default login template => registration/login.html
    * scratch LoginView, LogoutView (eventually not in use)
    * SignUpView
    * default LoginView, LogoutView
    * settings.
        LOGIN_REDIRECT_URL
        LOGOUT_REDIRECT_URL
        LOGIN_URL

- Custom User Model
    - using email field as identification instead of username field
    - UserManager(BaseUserManager)
    - PermissionsMixin
    - settings.AUTH_USER_MODEL
    - get_user_model()

- Authorization
    - PermissionRequiredMixin


# Packages
- markdown2


# Changes from the original

- misaka -> markdown2
- django-braces削除: prefetch_related, select_relatedを直接利用
- 脱Bootstrap3, 不要assets削除
- change import User: django.contrib.auth.models.User -> User = get_user_model()
- Typo: communities.views.py: Permissions -> Permission
- 不具合: Community名にascii以外を使用するとslugが""になる: ``slugify(text, allow_unicode=True)``
- Django3対応: ``{% load static %}``


# test account

ganq@hoge.com
hawkeye1
