from rest_framework.response import Response


def check_permissions(permissions: list):
    def decorator(f):
        def func(request, *args, **kwargs):
            if False in permissions:
                return lambda request_, *args_, **kwargs_: Response(status=550)
            else:
                return f(request, *args, **kwargs)
