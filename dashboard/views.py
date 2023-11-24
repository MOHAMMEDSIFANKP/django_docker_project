from django.shortcuts import render,redirect
from django.views.generic import *
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.urls import reverse_lazy
from .forms import *
from authentication.models import *
# Create your views here.


class CustomLoginRequiredAdmin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not request.user.is_superuser:
                return redirect('Home')
        else:
            return redirect('DashbardLogin')
        return super().dispatch(request, *args, **kwargs)

class DashbardLogin(FormView):
    form_class = CustomAuthenticationForm
    template_name = 'dashboard/signin.html'
    success_url = reverse_lazy('DashbaordHome')

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        
        if user is not None and user.is_superuser:
            login(self.request, user)
            return response 

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            return redirect(self.success_url)
        return super().get(request, *args, **kwargs)

class CustomLogoutView(CustomLoginRequiredAdmin,LogoutView):
    login_url = 'dashboard/signin/'
    def get_next_page(self):
        return reverse_lazy('DashbardLogin')
    
class DashbaordHome(CustomLoginRequiredAdmin,ListView):
    template_name = 'dashboard/userslist.html'
    queryset = UserProfile.objects.all().exclude(user__is_superuser=True)
