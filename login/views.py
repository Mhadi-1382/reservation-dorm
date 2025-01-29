from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from reservation.models import Reservation
from datetime import date
import jdatetime
from django.utils import timezone
from .models import User
from django.contrib.auth import update_session_auth_hash
from django.core.files.storage import FileSystemStorage
from django.conf import settings



    
def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        name = request.POST.get('name')
        last_name = request.POST.get('last_name')
        national_id = request.POST.get('national_id')    
        phone_number = request.POST.get('phone_number')

        if User.objects.filter(username=username,national_id=national_id).exists():
            messages.error(request, 'این کد پرسنلی یا کد ملی قبلاً استفاده شده است.')
            return redirect('signup')
        elif len(national_id) != 10:
            messages.error(request, "کد ملی باید 10 رقم باشد.")
            return redirect('signup')
        elif not username.isdigit():
            messages.error(request, "کد پرسنلی باید عدد باشد.")
            return redirect('signup')
        elif not national_id.isdigit():
            messages.error(request, "کد ملی باید عدد باشد.")
            return redirect('signup')    
        elif len(phone_number)!=11:
            messages.error(request, " شماره تماس باید 11 رقم باشد.")
            return redirect('signup')
        elif not phone_number.isdigit():
             messages.error(request, "شماره تماس باید از نوع عدد باشد.")
             return redirect('signup')
        else:  
            user = User.objects.create_user(username=username, password=password,
            name=name,last_name=last_name,national_id=national_id,phone_number=phone_number)
            user.save()
            messages.success(request, "ثبت نام با موفقیت انجام شد برای ورود میتوانید اقدام کنید.")
            return redirect('login') 

    return render(request, 'signup.html')


def convert_persian_to_english_number(persian_number):
    persian_digits = '۰۱۲۳۴۵۶۷۸۹'
    english_digits = '0123456789'
    translation_table = str.maketrans(persian_digits, english_digits)
    return persian_number.translate(translation_table)

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # استفاده از مدل کاربر سفارشی
        User = get_user_model()

        # ابتدا تلاش برای دریافت کاربر بر اساس نام کاربری
        try:
            user = User.objects.get(username=username)
            # حالا بررسی می‌کنیم که آیا کاربر غیرفعال است یا خیر
            if user.is_active:
                # اگر کاربر فعال باشد، سعی می‌کنیم وارد شویم
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.error(request, "کد ملی یا کلمه عبور اشتباه است.")
            else:
                # اگر کاربر غیرفعال باشد
                messages.error(request, 'اکانت شما غیرفعال است. لطفاً با پشتیبانی تماس بگیرید.')
        except User.DoesNotExist:
            messages.error(request, "کاربری با این نام وجود ندارد.")

    return render(request, 'login.html')
    
def forgotpass(request):
    return render(request,'forgotpass.html')

def logout_page(request):
    logout(request)
    return redirect('login')



def user_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user = request.user
    reservations = Reservation.objects.filter(user=user)

    # تبدیل تاریخ عضویت به شمسی
    jalali_date_joined = jdatetime.date.fromgregorian(date=user.date_joined)
    user.date_joined_shamsi = f"{jalali_date_joined.year}/{jalali_date_joined.month}/{jalali_date_joined.day}"

    for reservation in reservations:
        # تبدیل تاریخ ورود و خروج
        jalali_check_in = jdatetime.date.fromgregorian(date=reservation.check_in_date)
        reservation.check_in_date_shamsi = f"{jalali_check_in.year}/{jalali_check_in.month}/{jalali_check_in.day}"

        jalali_check_out = jdatetime.date.fromgregorian(date=reservation.check_out_date)
        reservation.check_out_date_shamsi = f"{jalali_check_out.year}/{jalali_check_out.month}/{jalali_check_out.day}"

    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # بررسی رمز عبور قدیمی
        if request.user.check_password(old_password):
            if new_password == confirm_password:
                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request, request.user)  # حفظ نشست کاربر
                messages.success(request, 'رمز عبور با موفقیت تغییر یافت.')
                return redirect('user_profile')
            else:
                messages.error(request, 'رمز عبور جدید و تأیید آن برابر نیستند.')
        else:
            messages.error(request, 'رمز عبور قدیمی صحیح نیست.')


    return render(request, 'user_profile.html', {
        'user': user,
        'reservations': reservations,
        'MEDIA_URL': settings.MEDIA_URL, 
    })


def update_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user = request.user  # تعریف کاربر

    # مدیریت بارگذاری عکس پروفایل
    if request.method == 'POST':
        if request.FILES.get('image'):
            user.profile_picture = request.FILES['image']
            user.save()  # ذخیره تغییرات در مدل کاربر
            messages.success(request, 'عکس پروفایل با موفقیت تغییر یافت.')
            return redirect('user_profile')  # بازگشت به صفحه پروفایل

    # اگر متد POST نیست یا هیچ چیز دیگری وجود ندارد، صفحه پروفایل را دوباره بارگذاری کنید
    return render(request, 'user_profile.html', {
        'user': user,
        'MEDIA_URL': settings.MEDIA_URL, 
    })





def cancel_reservation(request, reservation_id):
    if not request.user.is_authenticated:
        return redirect('login')
    # ابتدا تلاش برای دریافت رزرو با شناسه مشخص
    reservation = get_object_or_404(Reservation, id=reservation_id)

    # بررسی اینکه آیا کاربر مجاز به لغو این رزرو است یا خیر
    if request.user == reservation.user:    
        # تبدیل created_at به تاریخ
        created_at_date = reservation.created_at.date()  # تبدیل به date
        
        # بررسی اینکه آیا کمتر از 48 ساعت گذشته است
        reservation.delete()  # حذف رزرو
        reservation.room.is_reserved = False  # تغییر وضعیت اتاق
        reservation.room.save()  # ذخیره تغییرات اتاق
    else:
        messages.error(request, "شما مجاز به لغو این رزرو نیستید.")

    return redirect('user_profile')  # بازگشت به صفحه حساب کاربری

def password_change(request):
 
    
    return render(request, 'user_profile.html')




















