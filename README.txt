Django
======

Commands
---

- Create project
```
cd <repository_root>
python -m venv env
env/Scripts/Activate.ps1
pip install django

django-admin startproject <project>
```

- Run local server
```
python manage.py runserver [0:8080]  # default => 127.0.0.1:8000
```

- Run shell
```
python manage.py shell

- django-extensions
python manage.py shell_plus
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

Model and Migration
---

- 大幅な変更を行った場合には、migration後うまく動かないこともある。
   特に、SQLiteは厳密な型がないので、型変更を伴うmigration後にTypeErrorが起きやすい。
   dbファイルとmigrationファイルを削除して作り直す。
- create models
```
python manage.py makemigrations [<app_label>]
python manage.py showmigrations
python manage.py sqlmigrate <app_label> <migration_name>
python manage.py migrate
python manage.py showmigrations
```

Django Command
---

``` management/commands/hello_command.py
python manage.py hello_command
```

Import/Export
```
python manage.py loaddata fixtures.json
python manage.py dumpdata --format json -o fixtures.json <app_label[.ModelName]>
python manage.py dumpdata --indent 2 -o users.json auth.User
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


Test
----

```
python manage.py test -v 2
coverage report -m
coverage html
```

- nose
``` settings.py
INSTALLED_APPS = [
    ...,
    'django_nose',
]

...

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    '--with-coverage',
    '--cover-erase',
    '--cover-inclusive',
    '--cover-package=games',
]
```


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
