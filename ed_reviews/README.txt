# SessionAuthentication
ganq: hawkeye1


# TokenAuthentication

```
>>> from rest_framework.authtoken.models import Token
>>> from django.contrib.auth.models import User
>>> user = User.objects.get(username='ganq')
>>> Token.objects.create(user=user)
<Token: 116828e883d542de79ce8c7d93ef7c3f0abf8b92>
```
