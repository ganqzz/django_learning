from django.contrib.auth import get_user_model

UserModel = get_user_model()


class NoAuthentication:
    """
    All requests will use the user "user_a" (part of the pre-existing data).
    Returns a two-tuple of (user, token)
    """

    def authenticate(self, request):
        return UserModel.objects.get(username='user_a'), None
