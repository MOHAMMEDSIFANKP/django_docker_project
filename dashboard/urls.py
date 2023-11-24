from django.urls import path,include
from .views import *
urlpatterns = [
    path('', DashboardHome.as_view(), name='DashboardHome'),
    path('signin/', DashboardLogin.as_view(), name='DashboardLogin'),
    path('signout/', CustomLogoutView.as_view(), name='CustomLogoutView'),
    path('search/', Search.as_view(), name='Search'),
]