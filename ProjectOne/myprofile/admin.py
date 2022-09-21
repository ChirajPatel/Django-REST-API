from django.contrib import admin

from .models import MyProfile


# Register your models here.
class MyProfileAdmin(admin.ModelAdmin):
    list_display = ("phone", "address", "user")


admin.site.register(MyProfile)
