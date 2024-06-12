from django.contrib import admin # type: ignore
from .models import Account, UserProfile
from django.contrib.auth.admin import UserAdmin # type: ignore
from django.utils.html import format_html # type: ignore
# Register your models here.
class AccountAdmin(UserAdmin): 
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_jioned', 'is_active')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class UserProfileAdmin(admin.ModelAdmin): 
    def thumbnail(self, object): 
        try: 
            return format_html('<img src="{}" width="30" style="border-radius:50%;">'.format(object.profile_picture.url))
        except: 
            pass
    thumbnail.short_description = 'Profile Picture'
    list_display = ('thumbnail', 'user', 'city', 'state', 'country')

admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
