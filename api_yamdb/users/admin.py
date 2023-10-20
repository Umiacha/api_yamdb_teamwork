from django.contrib import admin

from .models import CustomUser


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "bio",
        "role",
    )
    exclude = ("groups",)


admin.site.register(CustomUser, UserAdmin)
