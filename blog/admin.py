from django.contrib import admin
from .models import Blog, Collection, Comment
# Register your models here.

admin.site.register(Blog)
admin.site.register(Collection)
admin.site.register(Comment)
