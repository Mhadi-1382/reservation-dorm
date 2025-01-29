from django.urls import path
from . import views

urlpatterns = [  
    path('home/', views.home, name='home'),
    path('get-items/', views.get_items, name='get_items'),
    path('city/<int:city_id>/dormitories/', views.city_dormitories_view, name='city_dormitories'),
    path('province/<int:province_id>/', views.province_view, name='province_view'),

]
