Django
======

Commands
---

- Virtual environment
```
cd <repository_root>

# Linux (bash)
python3 -m venv venv
source venv/bin/activate

# Windows (PowerShell)
python -m venv venv
venv/Scripts/Activate.ps1

- Install Django
```
pip install django
```

- Create project
```
django-admin startproject <project> [<base_dir>]  # default: create <project> sub directory
```

- Run local server
```
python manage.py runserver [host:port]  # default => host: 127.0.0.1, port: 8000
```

- Run shell
```
python manage.py shell
python manage.py shell_plus  # django-extensions
python manage.py dbshell  # DB cmdline client (sqlite3, mysql, psql, ...)
```

- Compatibility check
```
python -Wd manage.py
```

- Create Application
```
cd <project>
python manage.py startapp <app>
```

``` settings.py
INSTALLED_APPS = [
    ...,
    '<app>',
]
```

Model and Migration
---

- 大幅な変更を行った場合には、migration後うまく動かないこともある。
   特に、SQLiteは厳密な型がないので、型変更を伴うmigration後にTypeErrorが起きやすい。
   dbファイルとmigrationファイルを削除して作り直す。

- create models
```
python manage.py makemigrations [<app>]
python manage.py showmigrations [<app>]
python manage.py sqlmigrate <app> <migration_name>  # show sql
python manage.py migrate [<app>] [<migration_name>]
python manage.py showmigrations [<app>]
```

- Unapply
```
python manage.py showmigrations [<app>]
python manage.py migrate <app> zero  # zero: all
python manage.py showmigrations [<app>]
```


Django Command
---

``` <app>/management/commands/hello_command.py
python manage.py hello_command
```


Fixtures
---

- Export
```
python manage.py dumpdata --format json -o fixtures.json <app.model> ...
python manage.py dumpdata --indent 2 -o users.json auth.User
```

- Import
```
python manage.py loaddata fixtures.json
```


Admin
---

- Register models to admin.py
- Create a super user
```
python manage.py createsuperuser
ganq: hawkeye1
```

- Customizing Admin site
   * match namespaces to original admin site
        copy from Django source

- Restrict access
    * IP filter by Proxy/Web server
    * rename the url "/admin/" to "/akfggegjpwej/"


Debug Toolbar
---

``` settings.py
INSTALLED_APPS = [
    ...,
    'debug_toolbar',
]

MIDDLEWARE = [
    ...,
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]
```


Testing
---

- TestCases (django.test.testcases)
    * unittest.TestCase
    * \_SimpleTestCase
    *   \_TransactionTestCase
    *     \_TestCase
    *     \_LiveServerTestCase
    *       \_StaticLiveServerTestCase

``` test
python manage.py test
python manage.py test -v 2  # verbosity level
python manage.py test <app.package.module.class.method>
python manage.py test --tag=<tag>  # limit by <tag>
python manage.py test --exclude-tag=<tag>  # opposite above
```

``` coverage
coverage run manage.py test
coverage report
coverage report -m
coverage html
```


Django REST Framework
---

- ImageField
    requires Pillow package

- CORS (django-cors-headers)

- Pagination適用におけるUnorderedObjectListWarning
    - Model Metaにordering追加
        常時適用される点に注意
    - QuerySetにorder_by()追加
        必要時のみ適用できる
    - ModelViewSetにordering追加
        OrderingFilter併用時のみ有効

- Token authentication
```
python manage.py drf_create_token <user>
```

- OAuth2 (django-oauth-toolkit)
    * Application作成
        <site>/o/applications/
        もしくは、adminから直接作成
