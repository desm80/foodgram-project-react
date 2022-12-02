from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Отображение модели User в Админке."""

    list_display = (
        'pk',
        'username',
        'first_name',
        'last_name',
        'email',
        'role',
    )
    list_editable = (
        'first_name',
        'last_name',
        'role',
    )
    list_filter = (
        'username',
        'email',
    )
    search_fields = (
        'user',
        'author',
    )
    empty_value_display = '-пусто-'
