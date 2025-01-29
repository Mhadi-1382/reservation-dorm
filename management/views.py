from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib import messages
from .forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from reservation.models import Reservation
from django.http import JsonResponse
import jdatetime
from django.db.models import Q


User = get_user_model()

def change_password(request, username):
    if not request.user.is_authenticated:
        return redirect('login')
    if not request.user.is_staff:
        return redirect('home')
    user = get_object_or_404(User, username=username)

    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # بررسی کلمه عبور قدیمی
        if not user.check_password(old_password):
            messages.error(request, "کلمه عبور قدیمی اشتباه است.")
        elif new_password != confirm_password:
            messages.error(request, "کلمه عبور جدید و تأیید آن مطابقت ندارد.")
        else:
            user.set_password(new_password)  # هش کردن و تنظیم کلمه عبور جدید
            user.save()
            messages.success(request, "کلمه عبور با موفقیت تغییر یافت.")
            return redirect('manage_users')  # به صفحه مدیریت کاربران برگردید

    return render(request, 'change_password.html', {'user': user})


def management_home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if not request.user.is_staff:
        return redirect('home')
    return render(request, 'manage.html')  # صفحه اصلی مدیریت


def manage_users(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if not request.user.is_staff:
        return redirect('home')
    query = request.GET.get('query', '')  # دریافت ورودی جستجو از URL
    users = User.objects.all()  # دریافت تمام کاربران به صورت پیش‌فرض

    if query:
        users = users.filter(username__icontains=query) 

    return render(request, 'manage_users.html', {'users': users})

def search_users(request):
    query = request.GET.get('query', '')
    results = []

    if query:
       
        results = User.objects.filter(
            Q(national_id__icontains=query) |
            Q(name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(username__icontains=query) |
            Q(phone_number__icontains=query)
        ).values('name', 'last_name', 'username', 'phone_number', 'national_id')
    else:
        # اگر جستجو خالی باشد، تمام کاربران را برمی‌گردانیم
        results = User.objects.values('name', 'last_name', 'username', 'phone_number', 'national_id')

    return JsonResponse(list(results), safe=False)

def delete_user(request, username):
    if not request.user.is_authenticated:
        return redirect('login')
    if not request.user.is_staff:
        return redirect('home')

    user = get_object_or_404(User, username=username)

    user.delete()  

    messages.success(request, "کاربر با موفقیت حذف شد.")

    return redirect('manage_users')


def manage_reservations(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if not request.user.is_staff:
        return redirect('home')

    reservations = Reservation.objects.all()

    if not reservations:
        return render(request,'manage_reservations.html',{'reservations':reservations})
    
    for reservation in reservations:
        # تبدیل تاریخ ورود
        jalali_check_in = jdatetime.date.fromgregorian(date=reservation.check_in_date)
        reservation.check_in_date_shamsi = f"{jalali_check_in.year}/{jalali_check_in.month}/{jalali_check_in.day}"

        # تبدیل تاریخ خروج
        jalali_check_out = jdatetime.date.fromgregorian(date=reservation.check_out_date)
        reservation.check_out_date_shamsi = f"{jalali_check_out.year}/{jalali_check_out.month}/{jalali_check_out.day}"
   

    return render(request, 'manage_reservations.html', {
        'reservations': reservations,
        'check_in_date_shamsi':reservation.check_in_date_shamsi,
        'check_out_date_shamsi':reservation.check_out_date_shamsi
    })




    
def search_reservations(request):
    username = request.GET.get('query', '')
    
    # اگر کد پرسنلی وجود نداشته باشد، همه رزروها را برمی‌گردانیم
    if username:
        reservations = Reservation.objects.filter(user__username__icontains=username)
    else:
        reservations = Reservation.objects.all()  # همه رزروها

    results = []
    for reservation in reservations:
          # تبدیل تاریخ ورود
        jalali_check_in = jdatetime.date.fromgregorian(date=reservation.check_in_date)
        reservation.check_in_date_shamsi = f"{jalali_check_in.year}/{jalali_check_in.month}/{jalali_check_in.day}"

        # تبدیل تاریخ خروج
        jalali_check_out = jdatetime.date.fromgregorian(date=reservation.check_out_date)
        reservation.check_out_date_shamsi = f"{jalali_check_out.year}/{jalali_check_out.month}/{jalali_check_out.day}"
        results.append({
            'id': reservation.id,
            'user': {
                'username': reservation.user.username,
            },
            'room': {
                'room_type': reservation.room.get_room_type_display(),
                'dormitory_name': reservation.room.dormitory.name,
            },
            'check_out_date_shamsi': reservation.check_out_date_shamsi,  # فرض بر این است که شما این تاریخ را به فرمت شمسی تبدیل کرده‌اید
            'check_in_date_shamsi': reservation.check_in_date_shamsi,  # فرض بر این است که شما این تاریخ را به فرمت شمسی تبدیل کرده‌اید
        })

    return JsonResponse(results, safe=False)




def delete_reservation(request):
    if request.method == 'POST':
        reservation_id = request.POST.get('id')
        reservation = get_object_or_404(Reservation, id=reservation_id)
        reservation.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)
































