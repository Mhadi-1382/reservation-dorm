from django.shortcuts import render, redirect, get_object_or_404
from .models import Room, Reservation
from django.db.models import Q
from django.contrib import messages
import jdatetime
from django.db import transaction
from datetime import date, timedelta
from django.http import JsonResponse
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from decimal import Decimal, InvalidOperation






def convert_persian_to_english_number(persian_number):
    persian_digits = '۰۱۲۳۴۵۶۷۸۹'
    english_digits = '0123456789'
    translation_table = str.maketrans(persian_digits, english_digits)
    return persian_number.translate(translation_table) 


def search_availability(request, dormitory_id):
    if not request.user.is_authenticated:
        return redirect('login')

    available_rooms = []

    if request.method == 'POST':
        room_type = request.POST.get('room_type')  # دریافت نوع اتاق
        check_in_date = request.POST.get('check_in_date')
        check_out_date = request.POST.get('check_out_date')

        # بررسی اینکه آیا نوع اتاق انتخاب شده است
        if not room_type:
            messages.error(request, "لطفاً ابتدا نوع اتاق را انتخاب کنید.")  # نمایش پیام خطا
            return render(request, 'search_availability.html', {'available_rooms': available_rooms})

        # تبدیل تاریخ‌ها از شمسی به میلادی
        check_in_date = convert_persian_to_english_number(check_in_date)
        check_out_date = convert_persian_to_english_number(check_out_date)

        check_in_date_miladi = jdatetime.datetime.strptime(check_in_date, '%Y/%m/%d').togregorian()
        check_out_date_miladi = jdatetime.datetime.strptime(check_out_date, '%Y/%m/%d').togregorian()

        duration = (check_out_date_miladi - check_in_date_miladi).days

        # بررسی اینکه آیا مدت زمان اقامت بیشتر از 3 روز است
        if duration > 2:
            messages.error(request, "مدت زمان رزرو نمی‌تواند بیشتر از ۳ روز باشد.")
            return redirect('search_availability', dormitory_id=dormitory_id)  # تغییر مسیر به فرم رزرو

        # پیدا کردن اتاق‌های خالی بر اساس تاریخ و نوع اتاق و خوابگاه مشخص شده
        available_rooms = Room.objects.filter(
            dormitory_id=dormitory_id,  # فیلتر بر اساس شناسه خوابگاه
            capacity=4
        ).exclude(
            Q(reservation__check_in_date__lt=check_out_date_miladi) & 
            Q(reservation__check_out_date__gt=check_in_date_miladi)
        )

        # اگر نوع اتاق مشخص شده باشد، فیلتر کنید
        if room_type:
            available_rooms = available_rooms.filter(room_type=room_type)
    
    return render(request, 'search_availability.html', {'available_rooms': available_rooms})

def room_details(request, room_id):
    if not request.user.is_authenticated:
        return redirect('login')

    room = get_object_or_404(Room, id=room_id)

    # دریافت تاریخ‌ها و تعداد نفرات از GET
    check_in_date = request.GET.get('check_in_date')
    check_out_date = request.GET.get('check_out_date')

    # تبدیل اعداد فارسی به انگلیسی
    check_in_date = convert_persian_to_english_number(check_in_date)
    check_out_date = convert_persian_to_english_number(check_out_date)

    # تبدیل تاریخ شمسی به میلادی
    check_in_date_miladi = jdatetime.datetime.strptime(check_in_date, '%Y/%m/%d').togregorian()
    check_out_date_miladi = jdatetime.datetime.strptime(check_out_date, '%Y/%m/%d').togregorian()

    room = Room.objects.get(id=room_id)
    number_of_days = (check_out_date_miladi - check_in_date_miladi).days
    total_price = number_of_days * room.price  # 
    # محاسبه مدت زمان اقامت


    # بررسی ظرفیت انتخابی


    if request.method == 'POST':
        capacity = request.POST.get('capacity', 4)  # مقدار پیش‌فرض 4
        total_price_str = request.POST.get('totalest_price')  # دریافت قیمت کل
        if capacity==4:
            total_price_str=total_price

        # تبدیل total_price به Decimal
        try:
            totalest_price = Decimal(total_price_str)
        except (InvalidOperation, ValueError):
            return render(request, 'make_reservation.html', {'error': 'قیمت کل نامعتبر است.'})


        # بررسی اینکه آیا اتاق در تاریخ‌های مشخص شده قبلاً رزرو شده است یا خیر
        existing_reservations = Reservation.objects.filter(
            room_id=room_id,
            check_in_date=check_in_date_miladi,
            check_out_date=check_out_date_miladi
        )

        if existing_reservations.exists():
            messages.error(request, 'متاسفانه این اتاق قبل شما رزرو شد.')
            return redirect('search_availability')  # تغییر مسیر به صفحه اصلی

        # اگر اتاق خالی باشد، یک شیء جدید از مدل Reservation ایجاد کنید
        reservation = Reservation(
            room_id=room_id,
            check_in_date=check_in_date_miladi,
            check_out_date=check_out_date_miladi,
            user=request.user,  # فرض بر این است که کاربر در حال حاضر وارد شده است
            number_of_people=capacity,
            total_price=totalest_price
        )
        reservation.save() 
        room.save()
        request.session['reservation_id'] = reservation.id
        request.session['reservation_success'] = True  # ذخیره وضعیت
        return redirect('reservation_success')

    return render(request, 'room_details.html', {
        'room': room,
        'check_in_date': check_in_date,
        'check_out_date': check_out_date,
        'total_price':total_price
   })

def reservation_success(request):
    if not request.user.is_authenticated:
        return redirect('login')
    reservation_id = request.session.get('reservation_id')
    reservation = get_object_or_404(Reservation, id=reservation_id)
    check_in_date_shamsi = jdatetime.date.fromgregorian(date=reservation.check_in_date).strftime('%Y/%m/%d')
    check_out_date_shamsi = jdatetime.date.fromgregorian(date=reservation.check_out_date).strftime('%Y/%m/%d')

    
    return render(request, 'reservation_success.html', {
        'reservation': reservation,
        'check_in_date':check_in_date_shamsi,
        'check_out_date':check_out_date_shamsi
    })




def download_pdf(request, reservation_id):
    # دریافت اطلاعات رزرو
    reservation = get_object_or_404(Reservation, id=reservation_id)

    # تبدیل تاریخ‌ها به شمسی
    check_in_date_shamsi = jdatetime.date.fromgregorian(date=reservation.check_in_date).strftime('%Y/%m/%d')
    check_out_date_shamsi = jdatetime.date.fromgregorian(date=reservation.check_out_date).strftime('%Y/%m/%d')

    # رندر کردن قالب HTML با تاریخ‌های شمسی
    html_string = render_to_string('reservation_pdf.html', {
        'reservation': reservation,
        'check_in_date': check_in_date_shamsi,
        'check_out_date': check_out_date_shamsi,
    })

    # تولید PDF از HTML
    pdf_file = HTML(string=html_string).write_pdf()

    # بازگشت PDF به عنوان پاسخ HTTP
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reservation_{reservation.id}.pdf"'
    
    return response

    
   

 