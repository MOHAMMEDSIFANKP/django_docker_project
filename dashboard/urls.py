from django.urls import path,include
from .views import *
urlpatterns = [
    path('', DashbaordHome.as_view(), name='DashbaordHome'),
    path('signin/', DashbardLogin.as_view(), name='DashbardLogin'),
    path('signout/', CustomLogoutView.as_view(), name='CustomLogoutView'),
    path('userslist/', UsersList.as_view(), name='UsersList'),
]