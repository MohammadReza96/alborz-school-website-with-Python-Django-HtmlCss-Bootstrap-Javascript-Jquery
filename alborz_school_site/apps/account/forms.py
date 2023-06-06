from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from apps.account.models import CustomUser

#####################################################################################################
#####################################################################################################
######################################################################## create user from admin panel

#--------------------------------------------------------------------------------- user creation form
class UserCreationForm(ModelForm):
    password =forms.CharField(label='Password',widget=forms.PasswordInput()) 
    re_password =forms.CharField(label='RePassword',widget=forms.PasswordInput())
    
    class Meta:
        model=CustomUser
        fields=['user_name','mobile_number']
    #----------------------------------- check password validation
    def clean_re_password(self):
        pass1=self.cleaned_data['password']
        pass2=self.cleaned_data['re_password']
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError('رمز ها باهم یکسان نیست')
        return pass2
    #----------------------------------- commit use for final confirm
    def save(self,commit=True):   
        user=super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
#-------------------------------------------------------------------------------- user modifying form
class UserChangeForm(ModelForm):
    password=ReadOnlyPasswordHashField(help_text='برای تغییر رمز عبور از <a href="../password">لینک</a> زیر اقدام کنید')  # for hashing the new password
    class Meta:
        model=CustomUser
        fields=['user_name','mobile_number','password','user_type','is_active','is_admin']

#####################################################################################################
#####################################################################################################
######################################################################## create user from admin panel

#--------------------------------------------------------------------------------- user register form
class RegisterUserForm(ModelForm):
    password =forms.CharField(label='رمز عبور',widget=forms.PasswordInput(attrs={'class':'form-control','id':'password','placeholder':'رمز عبور را وارد کنید'}))
    re_password =forms.CharField(label='تکرار رمز عبور',widget=forms.PasswordInput(attrs={'class':'form-control','id':'re_password','placeholder':'رمز عبور را وارد کنید'}))
    user_name=forms.CharField(label='نام کاربری',widget=forms.TextInput(attrs={'class':'form-control','id':'user_name','placeholder':'نام کاربری را وارد کنید'}))
    mobile_number=forms.CharField(label='شماره موبایل',widget=forms.TextInput(attrs={'class':'form-control','id':'mobile_number','placeholder':' شماره موبایل را وارد کنید'}))
    
    class Meta:
        model=CustomUser
        fields=[
            'user_name',
            'mobile_number',
            'password'
            ]
    #----------------------------------------- for checking if password and repassword are the same
    def clean_re_password(self):
        pass1=self.cleaned_data['password']
        pass2=self.cleaned_data['re_password']
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError('رمز ها باهم یکسان نیست')
        return pass2
    #---------------------------------------- for checking if user_name (mobile_number) is unique 
    def clean_user_name(self):
        user_name=self.cleaned_data['user_name']
        user_exists=CustomUser.objects.filter(user_name=user_name)
        if user_exists:
            raise ValidationError('این نام کاربری قبلا انتخاب شده است')
        return user_name    
#--------------------------------------------------------------------------------- user verify form
class VerifyRegisterForm(forms.Form):
    active_code=forms.CharField(
        label='کد فعال سازی',
        error_messages={'required':'این فیلد نمی تواند خالی باشد','invalid':'کد وارد شده صحیح نیست'},
        widget=forms.TextInput(attrs={'class':'form-control','id':'active_code','placeholder':'کد فعال سازی را وارد کنید'})
    )
#--------------------------------------------------------------------------------- user login form
class LoginUserForm(forms.Form):
    user_name=forms.CharField(label='نام کابری خود را وارد کنید',error_messages={'required':'این فیلد نمی تواند خالی باشد','invalid':'نام کابری وارد شده صحیح نیست'},widget=forms.TextInput(attrs={'class':'form-control','id':'user_name','placeholder':'نام کابری خود را وارد کنید'}))
    password =forms.CharField(label='رمز عبور',widget=forms.PasswordInput(attrs={'class':'form-control','id':'password','placeholder':'رمز عبور را وارد کنید'})) 
#--------------------------------------------------------------------------------- user forget password form
class RememberPassword(forms.Form):
    # user_name=forms.CharField(
    #     label='نام کاربری',
    #     error_messages={'required':'این فیلد نمی تواند خالی باشد','invalid':'نام کابری وارد شده صحیح نیست'},
    #     widget=forms.TextInput(attrs={'class':'form-control','placeholder':'نام کاربری را وارد کنید'})
    #     )
    mobile_number=forms.CharField(
        label='شماره موبایل',
        error_messages={'required':'این فیلد نمی تواند خالی باشد','invalid':'کد وارد شده صحیح نیست'},
        widget=forms.TextInput(attrs={'class':'form-control','id':'mobile_number','placeholder':'موبایل را وارد کنید'})
    )
#--------------------------------------------------------------------------------- user change password form
class ChangePassword(forms.Form):
    password =forms.CharField(label='رمز عبور',widget=forms.PasswordInput(attrs={'class':'form-control','id':'password','placeholder':'رمز عبور را وارد کنید'})) 
    re_password =forms.CharField(label='تکرار رمز عبور',widget=forms.PasswordInput(attrs={'class':'form-control','id':'re_password','placeholder':'رمز عبور را وارد کنید'}))
    
    #----------------------------------------- for checking if password and repassword are the same
    def clean_re_password(self):
        pass1=self.cleaned_data['password']
        pass2=self.cleaned_data['re_password']
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError('رمز ها باهم یکسان نیست')
        return pass2




