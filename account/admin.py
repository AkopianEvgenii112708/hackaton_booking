# Register your models here.

from django.contrib import admin

from account.models import CustomUser

admin.site.register(CustomUser)
