# 2026-01-01 18:03
from django.contrib import admin
from django.urls import path, include
from core.views import index, profile, profiling, black_book

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', index, name='home'),
    path('profile/', profile, name='profile'),
    path('profiling/', profiling, name='profiling'),
    path('black-book/', black_book, name='black_book'),
]
