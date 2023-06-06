from django.db import models
from django.contrib.auth.models import User,AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.utils import timezone
from modules.file_upload_module import FileUploader

#----------------------------------------------------------------------------------------------------------------- ok
class CustomUserManager(BaseUserManager): 
    # create normal user
    def create_user(self,user_name,mobile_number,active_code=None,password=None):
        if not user_name:
            raise ValueError('نام کاربری باید وارد شود')
        user=self.model(
            user_name=user_name,
            mobile_number=mobile_number,            
            active_code=active_code,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    # create super user
    def create_superuser(self,user_name,mobile_number,password=None,active_code=None):
        user=self.create_user(
            user_name=user_name,
            mobile_number=mobile_number,
            active_code=active_code,
            password=password
        )
        user.is_active=True
        user.is_admin=True
        user.is_superuser=True
        user.save(using=self._db)
        return user
#----------------------------------------------------------------------------------------------------------------- ok
class CustomUser(AbstractBaseUser,PermissionsMixin):
    # user_name
    user_name=models.CharField(max_length=20,unique=True,verbose_name='نام کاربری')
    # user_data_information ---------------------
    mobile_number=models.CharField(max_length=11,null=True,blank=True,verbose_name='شماره موبایل')
    user_types=(('teacher','معلم'),('student','دانش آموز'),('visitor','کاربر عادی'),('superuser','سوپر یوزر'),('admin_post','ادمین مقالات'),('admin_exam','ادمین امتحانات'),('admin_regi','ادمین ثبت نام'),('writer','نویسنده'))
    user_type=models.CharField(max_length=50,verbose_name='نوع کاربر',blank=True,choices=user_types,default='visitor',null=True)
    # user_data_date 
    register_date=models.DateField(default=timezone.now,verbose_name='تاریخ ثبت نام')
    is_active=models.BooleanField(default=False,verbose_name='وضعیت کاربر')
    active_code=models.CharField(max_length=100,default=0,verbose_name='کد فعال سازی',null=True,blank=True)
    is_admin=models.BooleanField(default=False,verbose_name='وضعیت ادمینی')
    # fields from oneTomany or manyTomany relationship 

    USERNAME_FIELD='user_name'
    REQUIRED_FIELDS=['mobile_number']
    objects=CustomUserManager()
    
    def __str__(self):
        return self.user_name
    @property
    def is_staff(self):
        return self.is_admin
    class Meta:
        verbose_name='کاربر'
        verbose_name_plural='کاربران'
#-----------------------------------------------------------------------------------------------------------------
class CustomUserTeacherDetail(models.Model):
    # create an object from a class to save image
    file_upload=FileUploader('images','teachers')
    
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,verbose_name='کاربر',null=True,blank=True)
    name=models.CharField(max_length=50,blank=True,verbose_name='نام')
    family=models.CharField(max_length=50,blank=True,verbose_name='نام خانوادگی')
    user_slug=models.SlugField(max_length=50,verbose_name='شناسه کاربر',null=True,blank=True)
    email=models.EmailField(max_length=200,blank=True,verbose_name='ایمیل')
    image=models.ImageField(upload_to=file_upload.upload_to,verbose_name='عکس کاربر',null=True,blank=True)
    address=models.TextField(null=True,blank=True,verbose_name='ادرس')
    city=models.CharField(max_length=50,null=True,blank=True,verbose_name='شهر')
    province=models.CharField(max_length=50,null=True,blank=True,verbose_name='استان')
    postal_code=models.CharField(max_length=12,null=True,blank=True,verbose_name='کدپستی')
    register_date=models.DateField(default=timezone.now,verbose_name='تاریخ ثبت نام')
    update_date=models.DateField(auto_now=True,verbose_name='تاریخ آپدیت')

    class Meta:
        verbose_name='جدول اطلاعات استاد'
        verbose_name_plural='جدول اطلاعات اساتید'
#-----------------------------------------------------------------------------------------------------------------
class CustomUserStudentDetail(models.Model):
    # create an object from a class to save image
    file_upload=FileUploader('images','students')
    user_classes=(
        ('C1-1R','اول دبیرستان رشته ریاضی کد اول'),
        ('C1-2R','اول دبیرستان رشته ریاضی کد دوم'),
        ('C1-1E','اول دبیرستان رشته انسانی کد اول'),
        ('C1-2E','اول دبیرستان رشته انسانی کد دوم'),
        ('C1-1T','اول دبیرستان رشته تجربی کد اول'),
        ('C1-2T','اول دبیرستان رشته تجربی کد دوم'),
        ('C2-1R','دوم دبیرستان رشته ریاضی کد اول'),
        ('C2-2R','دوم دبیرستان رشته ریاضی کد دوم'),
        ('C2-1T','دوم دبیرستان رشته تجربی کد اول'),
        ('C2-2T','دوم دبیرستان رشته تجربی کد دوم'),
        ('C2-1E','دوم دبیرستان رشته انسانی کد اول'),
        ('C2-2E','دوم دبیرستان رشته انسانی کد دوم'),
        ('C3-1R','سوم دبیرستان رشته ریاضی کد اول'),
        ('C3-2R','سوم دبیرستان رشته ریاضی کد دوم'),
        ('C3-1T','سوم دبیرستان رشته تجربی کد اول'),
        ('C3-2T','سوم دبیرستان رشته تجربی کد دوم'),
        ('C3-1E','سوم دبیرستان رشته انسانی کد اول'),
        ('C3-2E','سوم دبیرستان رشته انسانی کد دوم'),
        ('C4-R','پیش دانشگاهی رشته ریاضی'),
        ('C4-T','پیش دانشگاهی رشته تجربی'),
        ('C4-E','پیش دانشگاهی رشته انسانی'),
    )
    user_special_situations=(
        ('normal','نرمال'),
        ('miltary_inj','فرزند جانباز'),
        ('miltary','فرزند نظامی'),
        ('teach_fal','فرزند فرهنگی'),
        ('illness','بیماری خاص'),
        ('intelligance','نخبه')
    )
    
    
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,verbose_name='کاربر',null=True,blank=True)
    user_class=models.CharField(max_length=20,verbose_name='مقطع تحصیلی',choices=user_classes,null=True,blank=True)
    name=models.CharField(max_length=50,blank=True,verbose_name='نام')
    family=models.CharField(max_length=50,blank=True,verbose_name='نام خانوادگی')
    father_name=models.CharField(max_length=50,blank=True,verbose_name='نام پدر')
    identity_number=models.CharField(max_length=50,blank=True,verbose_name='شماره شناسنامه')
    age=models.PositiveIntegerField(default=0,verbose_name='سن',null=True,blank=True)
    place_born=models.CharField(max_length=50,blank=True,verbose_name='محل تولد')
    born_date=models.DateField(null=True,blank=True,verbose_name='تاریخ تولد')
    previous_avg=models.DecimalField(max_digits=4,decimal_places=2,verbose_name='معدل مقطع قبل',null=True,blank=True)
    user_special_situation=models.CharField(max_length=50,choices=user_special_situations,verbose_name='شرایط خاص',null=True,blank=True,default='normal')
    email=models.EmailField(max_length=200,blank=True,verbose_name='ایمیل')
    image=models.ImageField(upload_to=file_upload.upload_to,verbose_name='عکس کاربر',null=True,blank=True)
    address=models.TextField(null=True,blank=True,verbose_name='ادرس')
    city=models.CharField(max_length=50,null=True,blank=True,verbose_name='شهر')
    province=models.CharField(max_length=50,null=True,blank=True,verbose_name='استان')
    postal_code=models.CharField(max_length=12,null=True,blank=True,verbose_name='کدپستی')
    register_date=models.DateField(default=timezone.now,verbose_name='تاریخ ثبت نام')
    update_date=models.DateField(auto_now=True,verbose_name='تاریخ آپدیت')

    class Meta:
        verbose_name='جدول اطلاعات دانش آموز'
        verbose_name_plural='جدول اطلاعات دانش آموزان'
#----------------------------------------------------------------------------------------------------------------- ok
class CustomUserVisitorDetail(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,verbose_name='کاربر',null=True,blank=True)
    name=models.CharField(max_length=50,blank=True,verbose_name='نام')
    family=models.CharField(max_length=50,blank=True,verbose_name='نام خانوادگی')
    email=models.EmailField(max_length=200,blank=True,verbose_name='ایمیل')
    register_date=models.DateField(default=timezone.now,verbose_name='تاریخ ثبت نام')
    update_date=models.DateField(auto_now=True,verbose_name='تاریخ آپدیت')

    class Meta:
        verbose_name='جدول اطلاعات کاربر عادی'
        verbose_name_plural='جدول اطلاعات کاربران عادی'

