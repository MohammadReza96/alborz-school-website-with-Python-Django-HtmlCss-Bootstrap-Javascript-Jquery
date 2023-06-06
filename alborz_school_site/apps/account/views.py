from django.shortcuts import render,redirect
from apps.account.forms import RegisterUserForm,VerifyRegisterForm,LoginUserForm,ChangePassword,RememberPassword
from apps.account.models import CustomUser
from django.db.models import Q
from django.views import View
from modules.kavehnegar_module import send_sms
from modules.random_code_maker import code_maker
from django.contrib import messages
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.mixins import LoginRequiredMixin


#--------------------------------------------------------------------------------------------------------- register view
class RegisterUserView(View):
    # use for check in user is log in /log out / register /verify already
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index:home')
        return super().dispatch(request,*args,*kwargs)
    # for showing the form with get method
    def get(self,request,*args,**kwargs):
        register_form=RegisterUserForm()
        return render(request,'account_app/register_form.html',{'register_form':register_form})
    # for geting data from form with post method
    def post(self,request,*args,**kwargs):
        get_form=RegisterUserForm(request.POST)
        if get_form.is_valid():
            # first step clean data
            user=get_form.cleaned_data
            # second step create active code                        
            active_code=code_maker(6)
            # third step create user
            CustomUser.objects.create_user(
                user_name=user['user_name'],
                mobile_number=user['mobile_number'],
                active_code=active_code,
                password=user['password'],
                # name=user['name'],
                # family=user['family'],
                # email=user['email']
            )
            # fourth step send active code sms
            send_sms(user['mobile_number'],f'کد فعال سازی حساب شما {active_code} می باشد')
            # fifth step create session for verifying user in verfiy page
            request.session['user_session']={
                'active_code':str(active_code),
                'user_name':str(user['user_name']),
                'mobile_number':str(user['mobile_number']),
                'remember_password': False
            }
            # send a message in site if registering is successfull
            messages.success(request,'اطلاعات شما با موفقیت ثبت شد. لطفا کد فعال سازی پیامک شده را وارد کنید','success')
            return redirect('account:verify')
        return render(request,'account_app/register_form.html',{'register_form':get_form})
#--------------------------------------------------------------------------------------------------------- verify view
class VerifyRegisterUserView(View):
    # use for check in user is log in /log out / register /verify already
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index:home')
        return super().dispatch(request,*args,*kwargs)
    # for showing the form with get method
    def get(self,request,*args,**kwargs):
        verify_form=VerifyRegisterForm()
        return render(request,'account_app/verify_form.html',{'verify_form':verify_form})
    # for geting data from form with post method
    def post(self,request,*args,**kwargs):
        get_form=VerifyRegisterForm(request.POST)
        if get_form.is_valid():
            verify_user=get_form.cleaned_data
            # first step get user data from sesseion that we made in register class
            user_sessions=request.session['user_session']
            # second step is check the data that we get from form and the the data we have in session
            if verify_user['active_code']==user_sessions['active_code']:
                # chech if the user come from register page or remmeber page
                if user_sessions['remember_password'] ==False:
                    user=CustomUser.objects.get(user_name=user_sessions['user_name'])
                    user.is_active=True
                    user.active_code=code_maker(6)
                    user.save()
                    messages.success(request,'ثبت نام با موفقیت انجام شد','success')
                    return redirect('account:login')
                else:
                    return redirect('account:changepassword')
            # return an error message in front if permisions is not valid
            else:
                messages.error(request,'کد وارد شده معتبر نیست','danger')
                return render(request,'account_app/verify_form.html',{'verify_form':get_form})
            
        messages.error(request,'اطلاع وارد شده معتبر نیست','danger')
        return render(request,'account_app/verify_form.html',{'verify_form':get_form})
#--------------------------------------------------------------------------------------------------------- loging view
class LoginUserView(View):
    # use for check in user is log in /log out / register /verify already
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index:home')
        return super().dispatch(request,*args,*kwargs)
    # for showing the form with get method
    def get(self,request,*args,**kargs):
        login_form=LoginUserForm()
        return render(request,'account_app/login_form.html',{'login_form':login_form})
    # for geting data from form with post method
    def post(self,request,*args,**kargs):
        get_form=LoginUserForm(request.POST)
        if get_form.is_valid():
            user=get_form.cleaned_data
            # first step check autentication of user
            user_data=authenticate(username=user['user_name'],password=user['password'])
            if user_data is not None:
                db_user=CustomUser.objects.get(user_name=user['user_name'])
                # second step check if user is active or not (means user was verified before or not)
                if db_user.is_active==True:
                    if db_user.is_admin==False :
                        # send a message in fronend that user login seccessfully
                        messages.success(request,'ورود با موفقیت انجام شد','success')
                        # third step is to login user
                        login(request,user_data)
                        # for redirecting to index page
                        next_url=request.GET.get('next')
                        if next_url is not None:
                            return redirect(next_url)
                        else:
                            return redirect('index:home')
                    # if user is an super
                    else:
                        messages.error(request,'کاربر ادمین نمی تواند از این بخش وارد شود','warning')
                        return render(request,'account_app/login_form.html',{'login_form':get_form})
                # if user account is not activated
                else:
                    # print('index-not_active')  # for testing
                    messages.error(request,'حساب کاربری شما فعال نمی باشد','danger')
                    return render(request,'account_app/login_form.html',{'login_form':get_form})
            # if the user data is not truly entered
            else:
                # print('index-mistake')   # for testing
                messages.error(request,' نام کاربری یا رمز عبور را به درستی وارد نکرده اید!','danger')
                return render(request,'account_app/login_form.html',{'login_form':get_form})
        else:
            # print('index-mistake-FIRST')   # for testing
            return render(request,'account_app/login_form.html',{'login_form':get_form})
#--------------------------------------------------------------------------------------------------------- logout view
class LogoutUser(View):
    # use for check in user is log in /log out / register /verify already
    def dispatch(self, request, *args, **kwargs): 
        if not request.user.is_authenticated:
            return redirect('index:home')
        return super().dispatch(request,*args,*kwargs)
    # for showing the form with get method
    def get(self,request,*args,**kwargs):
        user_id=request.user.id
        # session_data=request.session[f'shop_card_{user_id}']
        logout(request)
        # request.session[f'shop_card_{user_id}']=session_data
        return redirect('index:home')
#--------------------------------------------------------------------------------------------------------- forget password view
class RememberPasswordView(View):
    # for showing the form with get method
    def get(self,request,*args,**kargs):
        remember_password=RememberPassword()
        return render(request,'account_app/rememberpassword_form.html',{'remember_password':remember_password})
    # for geting data from form with post method
    def post(self,request,*args,**kargs):
        get_form=RememberPassword(request.POST)
        if get_form.is_valid():
            user_data=get_form.cleaned_data
            # check if the user is exited or not
            try:
                # find the user by its mobile number
                user=CustomUser.objects.get(mobile_number=user_data['mobile_number'])
                active_code=code_maker(6)
                user.active_code=active_code
                user.save()
                send_sms(user_data['mobile_number'],f'کد تایید شماره موبایل شما {active_code} است')
                
                request.session['user_session']={
                    'active_code':str(active_code),
                    'user_name':user.user_name,
                    'mobile_number':str(user_data['mobile_number']),
                    'remember_password': True
                }
                
                messages.success(request,'جهت تغییر رمز عبور خود  کد دریافت شده را وارد کنید','success')
                return redirect('account:verify')
            except:
                messages.error(request,'نام کاربری موجود نیست','danger')
                return render(request,'account_app/rememberpassword_form.html',{'remember_password':get_form})
        else:
            messages.error(request,'فیلد ها را به درستی وارد کنید','danger')
            return render(request,'account_app/rememberpassword_form.html',{'remember_password':get_form})
#--------------------------------------------------------------------------------------------------------- changepassword view
class ChangePasswordView(View):
    # for showing the form with get method
    def get(self,request,*args,**kargs):
        change_password=ChangePassword()
        return render(request,'account_app/changepassword_form.html',{'change_password':change_password})
    # for geting data from form with post method
    def post(self,request,*args,**kargs):
        get_form=ChangePassword(request.POST)
        if get_form.is_valid():
            user_data=get_form.cleaned_data
            user_sessions=request.session['user_session']
            # check if the user is exited or not
            try:
                # find user by its mobile number to change his/her password
                user=CustomUser.objects.get(mobile_number=user_sessions['mobile_number'])
                user.set_password(user_data['password'])
                user.active_code=code_maker(6)
                user.save()
                messages.success(request,'رمز شما با موفقیت  تغییر کرد','success')
                
                request.session['user_session']={
                                'active_code':'',
                                'mobile_number':'',
                                'user_name':'',
                                'remember_password': False}
                return redirect('account:login')
            except:
                messages.error(request,' نام کابری موجود نیست','danger')
                return render(request,'account_app/changepassword_form.html',{'change_password':get_form})
        else:
            return render(request,'account_app/changepassword_form.html',{'change_password':get_form})
#--------------------------------------------------------------------------------------------------------- userpanel view
class UserPanelView(View):
    def get(self,request,*args,**kargs):
        return render(request,'account_app/user_panel.html')