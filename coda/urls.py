from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('api/', include('main.urls', namespace='api')),
    path('admin/', admin.site.urls),
]
