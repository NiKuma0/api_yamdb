from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin, UserCreationForm

User = get_user_model()


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'role',)


@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {
            'fields': ('username', 'first_name', 'last_name',)
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'role'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', ('password1', 'password2')),
        }),
    )
    empty_value_display = '-пусто-'
    list_display = ('email', 'username', 'role',
                    'first_name', 'last_name', 'bio',
                    'date_joined', 'is_staff')
    search_fields = ('username', 'email')
    list_filter = ('role', 'date_joined')
    add_form = UserForm
