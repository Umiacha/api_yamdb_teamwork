from django.contrib import admin

from .models import CustomUser


class UserAdmin(admin.ModelAdmin):
    exclude = ('groups',)  # Не получилось, но надо выкинуть это поле из админки + настроить при создании пользователя admin выставлять User.is_staff = True


admin.site.register(CustomUser)