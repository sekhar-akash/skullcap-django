from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.Home,name="home"),
    path('loggedhome/',views.LoggedHome,name="loggedhome"),
]
