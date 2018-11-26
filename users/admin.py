from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import myUser
from django.contrib.auth.models import User
# Register your models here.

# admin.site.unregister(User)


admin.site.register(myUser, UserAdmin)
