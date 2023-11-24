from django.shortcuts import render,redirect
from django.views.generic import *
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import login,authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import hashlib
from django.conf import settings
from .forms import *
from .models import UserProfile
# Create your views here.

class Signup(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'authentication/signup.html'
    success_url = reverse_lazy('Home')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:            
            return redirect('Home')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(self.request, user)
            
        return response
    
class Signin(FormView):
    form_class = AuthenticationForm
    template_name = 'authentication/signin.html'
    success_url = reverse_lazy('Home')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:            
            return redirect('Home')
        return super().get(request, *args, **kwargs)
    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(self.request, user)
            
        return response

class CustomLogoutView(LogoutView):
    def get_next_page(self):
        return reverse_lazy('Signin')

class Home(LoginRequiredMixin, TemplateView):
    login_url = 'signin/'
    template_name = 'user/Home.html'

class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'user/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = UserProfile.objects.filter(user_id=self.request.user.id).first()
        context["user_profile"] = user_profile
        return context
    
# /////////////////////////////////////////




    
from .models import *
class QrProfileView(View):
    template_name = 'qrprofileview.html'
    def get(self, request, token, user_id):
        try:
            user = User.objects.get(id=user_id)
            expected_hash = hashlib.sha256(f"{user.id}:{user.date_joined.timestamp()}:{settings.SECRET_KEY}".encode()).hexdigest()
            user_profile = get_object_or_404(UserProfile, user = user)
            if token == expected_hash:
                return render(request,self.template_name,{'user_profile' : user_profile})
            else:
                return HttpResponse("Invalid token")
        except User.DoesNotExist:
            return HttpResponse("User not found")
        except ValueError:
            return HttpResponse("Invalid token format")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return HttpResponse("An error occurred")
       
    
class not_fount(TemplateView):
    template_name = '404_page/404_page.html'