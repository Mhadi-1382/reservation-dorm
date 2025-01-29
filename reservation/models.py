from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
import pytz

def get_current_time():
    return timezone.now().astimezone(pytz.timezone('Asia/Tehran'))


class Province(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

    def get_cities(self):
        return self.city_set.all()  # دسترسی به شهرهای مرتبط با این استان
        
class City(models.Model):
    name = models.CharField(max_length=100)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_dormitories(self):
        return self.dormitories.all()  # دسترسی به خوابگاه‌های مرتبط با این شهر


class Dormitory(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='dormitories')

    def __str__(self):
        return self.name

class Room(models.Model):
    ROOM_TYPE_CHOICES = [
        ('suite', 'سوییت'),
        ('student_room', 'اتاق دانشجویی'),
    ]
    
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES)
    capacity = models.IntegerField(default=4)  # ظرفیت پیش‌فرض ۴ نفر
    dormitory = models.ForeignKey(Dormitory, on_delete=models.CASCADE, related_name='rooms')  # ارتباط با خوابگاه
    description = models.TextField(blank=True, null=True)  # توضیحات اتاق
    price = models.DecimalField(max_digits=10, decimal_places=0) # قیمت به ازای هر شب
    name = models.CharField(max_length=100,null=True)
    
    def __str__(self):
        return f"{self.name} - ظرفیت: {self.capacity} - خوابگاه: {self.dormitory.name}"

class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)
    number_of_people = models.IntegerField(default=4)  # تعداد نفرات
    created_at = models.DateTimeField(default=get_current_time)
    total_price = models.DecimalField(max_digits=10, decimal_places=0,null=True)

    def __str__(self):
        return f"رزرو: {self.room.name} از {self.check_in_date} تا {self.check_out_date}"