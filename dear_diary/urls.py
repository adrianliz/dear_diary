from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda req: redirect('/diary/')),
    path('diary/', include('diary.urls')),
    path('admin/', admin.site.urls),
]
