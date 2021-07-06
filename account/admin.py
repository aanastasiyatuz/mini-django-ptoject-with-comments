from django.contrib import admin
from .models import MyUser

# простое отображение модели в админке
admin.site.register(MyUser)