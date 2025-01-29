from django.urls import path
from . import views

urlpatterns = [  
    path('search/<int:dormitory_id>/', views.search_availability, name='search_availability'),
    path('room/<int:room_id>/', views.room_details, name='room_details'),
    path('reservation_success/', views.reservation_success, name='reservation_success'),
    path('download/pdf/<int:reservation_id>/', views.download_pdf, name='download_pdf'),
    
]
