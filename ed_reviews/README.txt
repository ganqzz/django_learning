# Users
ganq: hawkeye1: 116828e883d542de79ce8c7d93ef7c3f0abf8b92
testuser: testpassword: f4b25435dfdd5665aa584f8bcfbf0ed15ebdfba7


# TokenAuthentication

```
>>> from rest_framework.authtoken.models import Token
>>> from django.contrib.auth.models import User
>>> user = User.objects.get(username='ganq')
>>> Token.objects.create(user=user)
<Token: 116828e883d542de79ce8c7d93ef7c3f0abf8b92>
```
or
```
python manage.py drf_create_token <user>
```


# changes from the original

- Django: 1.x -> 2.x
    REST Frameworkに関してもアップデート対応。
- CourseSerializerに、HyperlinkedIdentityField（自分）を追加。
    HyperlinkedModelSerializerでやっていることと同じ。
- UnorderedObjectListWarning: Modelにordering追加。QuerySetのorder_by()では解消せず（2.1.3）
