from django.contrib import admin
from .models import Province,City, Dormitory, Room, Reservation


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('name',)

class RoomInline(admin.TabularInline):
    model = Room
    extra = 1  # تعداد اتاق‌های اضافی که می‌توان اضافه کرد
# نمایش فیلدهای مربوط به City
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'province')  # فیلدهای نمایش داده شده
    search_fields = ('name', 'province')  # جستجو بر اساس این فیلدها
    list_filter = ('province',)  # فیلتر بر اساس استان

# نمایش فیلدهای مربوط به Dormitory
class DormitoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'city')  # نمایش نام خوابگاه و شهر مرتبط
    search_fields = ('name',)  # جستجو بر اساس نام خوابگاه
    list_filter = ('city',)  # فیلتر بر اساس شهر
    list_select_related = ('city',)  # بهینه‌سازی بارگذاری ارتباط‌ها
    inlines = [RoomInline]

# نمایش فیلدهای مربوط به Room
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'room_type', 'capacity', 'dormitory', 'price')  # نمایش فیلدهای مهم اتاق
    search_fields = ('name', 'room_type', 'dormitory__name')  # جستجو بر اساس نام اتاق و خوابگاه
    list_filter = ('room_type', 'dormitory__city',)  # فیلتر بر اساس نوع اتاق و شهر خوابگاه
    list_select_related = ('dormitory',)  # بهینه‌سازی بارگذاری ارتباط‌های خارجی

# نمایش فیلدهای مربوط به Reservation
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('room', 'check_in_date', 'check_out_date', 'user', 'number_of_people', 'total_price')  # نمایش فیلدهای مربوط به رزرو
    search_fields = ('room__name', 'user__username')  # جستجو بر اساس نام اتاق و نام کاربر
    list_filter = ('check_in_date', 'check_out_date', 'room__dormitory__city')  # فیلتر بر اساس تاریخ ورود و خروج و شهر خوابگاه
    list_editable = ('total_price',)  # اجازه ویرایش قیمت رزرو از پنل مدیریت

# ثبت مدل‌ها با تنظیمات مناسب برای هر مدل
admin.site.register(City, CityAdmin)
admin.site.register(Dormitory, DormitoryAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Reservation, ReservationAdmin)
