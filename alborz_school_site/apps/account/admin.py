from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.account.forms import UserCreationForm,UserChangeForm
from apps.account.models import CustomUser,CustomUserTeacherDetail,CustomUserVisitorDetail,CustomUserStudentDetail
#---------------------------------------------- ok
class CustomUserAdmin(UserAdmin):
    form =UserChangeForm
    add_form =UserCreationForm
    list_display= ('user_name','mobile_number','user_type','is_active','is_admin')
    list_filter=('is_active','is_admin')
    
    #--------------------------------------------- modify user
    fieldsets =(
        ('login details',{'fields':('user_name','password')}),
        ('personal info',{'fields':('mobile_number','user_type','active_code')}),
        ('permissions',{'fields':('is_active','is_admin','is_superuser','groups','user_permissions')})
    )
    #--------------------------------------------- create user
    add_fieldsets =(
        ('account details',{'fields':('user_name','mobile_number','password','re_password')}),
    )
    
    search_fields=('user_name',)
    ordering = ('user_name',)
    filter_horizontal =('groups','user_permissions')

admin.site.register(CustomUser,CustomUserAdmin)
#----------------------------------------------
class CustomUserTeacherDetailAdmin(admin.ModelAdmin):
    pass
#----------------------------------------------
class CustomUserStudentDetailAdmin(admin.ModelAdmin):
    pass
#----------------------------------------------
class CustomUserVisitorDetailAdmin(admin.ModelAdmin):
    pass

admin.site.register(CustomUserStudentDetail)
admin.site.register(CustomUserTeacherDetail)
admin.site.register(CustomUserVisitorDetail)
