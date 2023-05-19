from django.urls import path,include
from . import views

urlpatterns = [
    path('userregister/',views.Register,name="userregister"),
    path('usersignin/',views.SignIn,name="usersignin"),
    path('verify/',views.verify_code,name='verify'),
    path('logout/',views.logoutpage,name='logout'),

    
]
