from django.shortcuts import render,redirect
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core.signing import BadSignature, Signer
import qrcode
from io import BytesIO
from decouple import config
from .forms import *
# Create your views here.

class Signup(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'authentication/signup.html'
    success_url = reverse_lazy('Profile')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:            
            return redirect('Profile')
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
    success_url = reverse_lazy('Profile')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:            
            return redirect('Profile')
        return super().get(request, *args, **kwargs)
    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(self.request, user)
            
        return response

class Signout(LoginRequiredMixin,View):
    login_url = 'signin/'
    def get(self,request):
        logout(request)
        return redirect('Signin')

class Profile(LoginRequiredMixin, TemplateView):
    login_url = 'signin/'
    template_name = 'profile.html'

class qrcode_generator(LoginRequiredMixin,View):
    def get(self, request):
        user_token = str(request.user.id)
        signer = Signer()
        signed_user_token = signer.sign(user_token)
        request.session['user_token'] = user_token
        base_url = config('base_url')
        redirect_url = f'{base_url}MobileAuthenticationView/{signed_user_token}/'

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(redirect_url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img_buffer = BytesIO()
        img.save(img_buffer)
        img_buffer.seek(0)

        response = HttpResponse(img_buffer, content_type='image/png')
        return response
    

class MobileAuthenticationView(View):
    def get(self, request, user_identifier):
        signer = Signer()
        user_id = signer.unsign(user_identifier)
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            user = None

        if user is not None:
            # User is authenticated, log them in.
            login(request, user)
            return redirect(Profile)

        return HttpResponse('Authentication failed. Please try again.')