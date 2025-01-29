from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.utils import timezone
from django.conf import settings

class CustomUserManager(UserManager):
    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError("You have not provided a valid username")
        
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_user(self, username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)
    
    def create_superuser(self, username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, null=True)  # نام کاربری جدید
    email = models.EmailField(blank=True, default='', null=True)  # فیلد ایمیل (اختیاری)
    name = models.CharField(max_length=255, blank=True, default='')  # نام
    last_name = models.CharField(max_length=255, blank=True, default='')  # نام خانوادگی
    phone_number = models.CharField(max_length=15, blank=True, default='')  # شماره تلفن
    national_id = models.CharField(max_length=10, blank=True, default='')  # کد ملی
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True,default='profile_pics/default.png')  # فیلد عکس پروفایل
    
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'  # تعیین نام کاربری به عنوان فیلد اصلی
    REQUIRED_FIELDS = ['name', 'last_name']  # فیلدهای مورد نیاز برای ایجاد کاربر
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def get_full_name(self):
        return f"{self.name} {self.last_name}"
    
    def get_short_name(self):
        return self.name or self.username

    def __str__(self):
        return f"{self.name} {self.last_name}" if self.name or self.last_name else self.username or "کاربر بدون نام"
