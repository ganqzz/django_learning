# Changes from the original

- misaka -> markdown2
- change import User: django.contrib.auth.models.User -> accounts.models.User
- Typo: communities.views.py: Permissions -> Permission
- 不具合: Community名にascii以外を使用するとslugが""になる（unicode-slugify）

# Authentication
- Built-in
    * django.contrib.auth.urls
    * LoginView, LogoutView
    * settings.
        LOGIN_REDIRECT_URL
        LOGOUT_REDIRECT_URL
        LOGIN_URL

- Custom User Model
    - PermissionsMixin
    - settings.AUTH_USER_MODEL
    - get_user_model()

- Authorization
    - PermissionRequiredMixin
