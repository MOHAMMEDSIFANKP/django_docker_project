from django.urls import path,include
from django.contrib.auth.views import LogoutView
from .views import *
urlpatterns = [
    path('signup/', Signup.as_view(), name='Signup'),
    path('signin/', Signin.as_view(), name='Signin'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('signout/', LogoutView.as_view(), name='Signout'),

    path('', Profile.as_view(), name='Profile'),
    path('qrcode_generator/', qrcode_generator.as_view(), name='qrcode_generator'),
    path('MobileAuthenticationView/<str:user_identifier>/', MobileAuthenticationView.as_view(), name='MobileAuthenticationView'),

]