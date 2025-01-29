from django.urls import path
from . import views

urlpatterns = [  
    path('', views.management_home, name="management_home"),  
    path('manage_reservations/', views.manage_reservations, name='manage_reservations'),
    path('manage-users/', views.manage_users, name='manage_users'), 
    path('change-password/<str:username>/', views.change_password, name='change_password'), 
    path('delete-user/<str:username>/', views.delete_user, name='delete_user'),
    path('search-users/', views.search_users, name='search_users'),
    path('search-reservations/', views.search_reservations, name='search_reservations'),  
    path('delete-reservation/', views.delete_reservation, name='delete_reservation'), 
]





     

 