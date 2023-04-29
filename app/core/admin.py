from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core import models
from django.utils.translation import gettext_lazy as _

#Register your models here.

class AdminDash(BaseUserAdmin):
    ordering = ['id']
    list_display =['email' ,'first_name' , 'last_name']
    fieldsets = (
        (_('Login Info') , {'fields':('email' , 'password')}),
        (
            _('Permissions'),
            {
                'fields':(
                    'is_active',
                    'is_staff',
                    'is_superuser'
                )
            }
        ),
        (_('Important_Dates'),{'fields':('last_login',)})
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None ,{
            'classes':('wide',),
            'fields':(
                'email',
                'password1',
                'password2',
                'first_name',
                'last_name',
                'is_active',
                'is_staff',
                'is_superuser'
            )
        }),
    )


admin.site.register(models.User , AdminDash)
