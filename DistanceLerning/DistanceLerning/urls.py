from django.urls import include
from django.contrib import admin
from django.urls import path
from DistanceLerning.settings import VERSION


urlpatterns = [
    path('admin/', admin.site.urls),
    path(f'api/{VERSION}/', include('main.urls')),
    path(f'api/{VERSION}/auth/', include('auth_app.urls')),
]
