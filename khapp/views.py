from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from reservation.models import City,Province,Dormitory


def home(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        query = request.POST.get('query')  # دریافت ورودی کاربر

        # بررسی اینکه آیا ورودی یک استان است یا شهر
        province = Province.objects.filter(name__icontains=query).first()
        city = City.objects.filter(name__icontains=query).first()

        if province:
            return redirect('province_view', province_id=province.id)  # هدایت به صفحه استان
        elif city:
            return redirect('city_dormitories', city_id=city.id)  # هدایت به صفحه شهر
        else:
            # اگر هیچ نتیجه‌ای پیدا نشد
            messages.error(request, "استان یا شهری با این نام پیدا نشد.")

    return render(request, 'index.html')  # نمایش فرم جستجو

def get_items(request):
    if not request.user.is_authenticated:
        return redirect('login')

    category = request.GET.get('category')
    items = City.objects.filter(province=category).values('id', 'name')
    return JsonResponse(list(items), safe=False)


def city_dormitories_view(request, city_id):
    city = get_object_or_404(City, id=city_id)
    dormitories = city.get_dormitories()  # دریافت همه خوابگاه‌های مرتبط با این شهر

    return render(request, 'dormitories.html', {
        'city': city,
        'dormitories': dormitories,
    })


def province_view(request, province_id):
    province = get_object_or_404(Province, id=province_id)
    cities = province.get_cities()  # دریافت همه شهرهای مرتبط با این استان

    return render(request, 'province.html', {
        'province': province,
        'cities': cities,
    })



