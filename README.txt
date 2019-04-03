Django
======

Commands
---

- Virtual environment
```
cd <repository_root>

# Linux (bash)
python3 -m venv env
source env/bin/activate

# Windows (PowerShell)
python -m venv env
env/Scripts/Activate.ps1

- Install Django
```
pip install django
```

- Create project
```
django-admin startproject <project> [<base_dir>]
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
python manage.py showmigrations
python manage.py sqlmigrate <app> <migration_name>  # show sql
python manage.py migrate
python manage.py showmigrations
```

- Unapply
```
python manage.py showmigrations
python manage.py migrate <app> zero
python manage.py showmigrations
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

- unittest.TestCase
- django.test
    * SimpleTestCase
    * TransactionTestCase
    * TestCase
    * LiveServerTestCase, StaticLiveServerTestCase

``` test
python manage.py test
python manage.py test -v 2  # verbosity level
python manage.py test <app.package.module.class.method>
python manage.py test --tag=<tag>
```

``` coverage
coverage run manage.py test
coverage report
coverage report -m
coverage html
```
