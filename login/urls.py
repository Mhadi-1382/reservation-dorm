from django.urls import path
from . import views

urlpatterns = [  
     path('',views.login_page,name='login'),
     path('sign-up/',views.signup_view,name='signup'),
     path('forgotpass/',views.forgotpass,name='forgotpass'),
     path('logout/', views.logout_page, name='logout'), 
     path('profile/', views.user_profile, name='user_profile'),
     path('cancel_reservation/<int:reservation_id>/', views.cancel_reservation, name='cancel_reservation'),
     path('update-profile/', views.update_profile, name='update_profile'),

]
     
     
 