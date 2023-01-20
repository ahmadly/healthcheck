# healthcheck

a very simple Django health check app

- easy to use
- no migration
- no extra dependency. only Django and Python 3.6+

## install

```shell
pip install easy-health-check
```

## usage

1. add `healthcheck` to `INSTALLED_APPS` in `settings.py`

```python

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'healthcheck',

]
    
```

2. add `healthcheck.urls` to `urlpatterns` in `urls.py`

```python
urlpatterns = [
    ...
    path('health/', include('healthcheck.urls')),
    ...
]
```

3. setting `HEALTHCHECK` in `settings.py`

```python
HEALTH_CHECK_TOKEN = None
HEALTH_CHECK_VIEW = 'healthcheck.views.HealthCheckView'
HEALTH_CHECK_FAIL_STATUS_CODE = 500
HEALTH_CHECK_SUCCESS_STATUS_CODE = 200
HEALTH_CHECK_FORBIDDEN_STATUS_CODE = 403

HEALTH_CHECK = [
    'healthcheck.checks.check_database_connection',
    'healthcheck.checks.check_cache_connection',
    'healthcheck.checks.check_internet_connection',
]

```

4. run server and go to `http://localhost:8000/health/`

```json
{
    "uuid": "8f45499108cf4407bd3533d08fe68b26",
    "timestamp": "2023-01-20T16:25:51.374452+00:00",
    "hostname": "Ahmads-MBP",
    "total_checks": 3,
    "failed_checks": 0,
    "results": [
        {
            "check": "healthcheck.checks.check_database_connection",
            "status": true,
            "message": "Database is reachable"
        },
        {
            "check": "healthcheck.checks.check_cache_connection",
            "status": true,
            "message": "Cache is reachable"
        },
        {
            "check": "healthcheck.checks.check_internet_connection",
            "status": true,
            "message": "Internet is reachable"
        }
    ]
}
```

## options

- `HEALTH_CHECK_TOKEN` is optional, if you want to use token for health check, set it to a string.
  set `Authorization` header to `Bearer <HEALTH_CHECK_TOKEN>` in request header.
- `HEALTH_CHECK_VIEW` is optional, if you want to use your own view, set it to a string. inherit
  from `healthcheck.views.HealthCheckView`

- `HEALTH_CHECK_FAIL_STATUS_CODE` is optional, if you want to use your own status code for fail, set it to an integer.
- `HEALTH_CHECK_SUCCESS_STATUS_CODE` is optional, if you want to use your own status code for success, set it to an
  integer.
- `HEALTH_CHECK_FORBIDDEN_STATUS_CODE` is optional, if you want to use your own status code for forbidden, set it to an
  integer.

- `HEALTH_CHECK` is optional, if you want to use your own checks, set it to a list of strings. each string is a path to
  a function. the function should return a tuple of two items. the first item is a boolean, the second item is a string.
  the boolean is the status of the check, the string is the message of the check.

```python
def check_database_connection() -> tuple[bool, str]:
    """
    check must return a tuple of (status, message)
    check must handle exceptions internally
    check must handle timeouts internally
    """

    return True, 'Database is reachable'

```

## contribute

if you have any idea, please open an issue or a pull request.

## todo

- [ ] add more checks
- [ ] add more tests
- [ ] add documentation
- [ ] add badges
- [ ] setup release workflow
- [ ] setup pypi.org