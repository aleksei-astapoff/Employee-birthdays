from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Subscribe, User

from .forms import UserForm

admin.site.empty_value_display = '-Не задано-'


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Административная модель пользователя."""

    form = UserForm

    list_display = (
        'id', 'email', 'first_name', 'last_name', 'date_of_birth',
        'department', 'get_following_count', 'get_follower_count'
        )
    search_fields = (
        'email', 'first_name', 'last_name', 'date_of_birth', 'department')
    list_filter = (
        'email', 'first_name', 'date_of_birth', 'department'
        )
    readonly_fields = ('last_login',)
    fieldsets = (
        (None, {'fields': ('password',)}),
        ('Permissions', {'fields': ('is_staff',)}),
    )
    add_fieldsets = (
        (None, {
            'fields': (
                'email', 'password1', 'password2',
                'first_name', 'last_name', 'date_of_birth', 'department'),
        }),
        ('Permissions', {'fields': ('is_staff',)}),
    )

    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:
            obj.set_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)

    @admin.display(description='Количество подписчиков')
    def get_follower_count(self, obj):
        return obj.follower.count()

    @admin.display(description='Количество подписок')
    def get_following_count(self, obj):
        return obj.following.count()


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    """Административная модель подписок."""

    list_display = ('id', 'user', 'birthday_person')
    search_fields = ('user__email', 'birthday_person__email')
