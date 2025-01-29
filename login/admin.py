from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'last_name', 'email', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'name')
    list_filter = ('is_active', 'is_staff')  # اضافه کردن فیلتر بر اساس وضعیت‌های مختلف
    ordering = ('-date_joined',)  # مرتب‌سازی بر اساس تاریخ پیوستن

    # این متد به شما اجازه می‌دهد تا گزینه تغییر کلمه عبور را داشته باشید
    def get_readonly_fields(self, request, obj=None):
        return []  # هیچ فیلدی فقط خواندنی نیست

    def save_model(self, request, obj, form, change):
        if change:  # اگر شیء موجود است (ویرایش)
            if User.objects.filter(username=obj.username).exclude(pk=obj.pk).exists():
                raise ValueError("این نام کاربری قبلاً استفاده شده است.")
        super().save_model(request, obj, form, change)
