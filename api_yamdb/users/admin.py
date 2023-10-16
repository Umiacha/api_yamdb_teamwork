from django.contrib import admin

from .models import CustomUser


class UserAdmin(admin.ModelAdmin):
    exclude = ('groups',)


admin.site.register(CustomUser, UserAdmin)
