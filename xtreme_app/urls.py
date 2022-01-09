from django.contrib import admin
from django.urls import path

from mail import views
urlpatterns = [
    path('admin/', admin.site.urls),
]