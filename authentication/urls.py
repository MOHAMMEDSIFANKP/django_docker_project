from django.urls import path,include
from .views import *
urlpatterns = [
    path('signup/', Signup.as_view(), name='Signup'),
    path('signin/', Signin.as_view(), name='Signin'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('signout/', CustomLogoutView.as_view(), name='Signout'),

    path('', Home.as_view(), name='Home'),
    path('profile/', UserProfileView.as_view(), name='UserProfiles'),    
    path('QrProfileView/<str:token>/<str:user_id>/', QrProfileView.as_view(), name='QrProfileView'),
    path('not_fount/', not_fount.as_view(), name='not_fount'),

]