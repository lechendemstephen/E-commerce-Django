from django.contrib import admin # type: ignore
from .models import Account
from django.contrib.auth.admin import UserAdmin # type: ignore
# Register your models here.
class AccountAdmin(UserAdmin): 
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_jioned', 'is_active')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)
