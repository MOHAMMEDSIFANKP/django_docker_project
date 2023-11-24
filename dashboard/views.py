from django.shortcuts import render,redirect
from django.views.generic import *
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.urls import reverse_lazy
from django.contrib import messages
import pandas as pd
from django.core.paginator import Paginator
from django.db.models import Q

from .forms import *
from authentication.models import *
# Create your views here.

class CustomLoginRequiredAdmin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not request.user.is_superuser:
                return redirect('Home')
        else:
            return redirect('DashboardLogin')
        return super().dispatch(request, *args, **kwargs)

class DashboardLogin(FormView):
    form_class = CustomAuthenticationForm
    template_name = 'dashboard/signin.html'
    success_url = reverse_lazy('DashboardHome')

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
        return reverse_lazy('DashboardLogin')
    
class DashboardHome(CustomLoginRequiredAdmin,ListView):
    template_name = 'dashboard/userslist.html'
    paginate_by = 5
    queryset = UserProfile.objects.all().exclude(user__is_superuser=True).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.queryset, self.paginate_by)
        page = self.request.GET.get('page')
        object_list = paginator.get_page(page)
        context['object_list'] = object_list
        return context
    
    def post(self,request):
        file = request.FILES.get('file')
        allowed_extensions = ('.csv', '.xlsx', '.xls')

        if not file:
            messages.error(request, 'Please upload a file')
            return redirect('DashboardHome')
        if not file.name.lower().endswith(allowed_extensions):
            messages.error(request, 'File must be a CSV or Excel file')
            return redirect('DashboardHome')
        else:
            try:
                df = pd.read_csv(file) 
                for index, row in df.iterrows():
                    user = User.objects.create_user(
                        username=row['username'],
                        first_name=row['first_name'],
                        last_name=row['last_name'],
                        password=str(row['password'])
                    )
                messages.success(request, 'Users imported successfully.')
            except Exception as e:
                messages.error(request, f'Error importing users: {e}')
        return redirect('DashboardHome')

class Search(View):
    template_name = 'dashboard/search_results.html'
    paginate_by = 6
    def get(self, request, *args, **kwargs):
        query = request.GET.get("query")
        results = UserProfile.objects.filter(Q(user__first_name__icontains=query) | Q(user__last_name__icontains=query) | Q(user__username__icontains=query)).order_by('-id')
        paginator = Paginator(results, self.paginate_by)
        page = self.request.GET.get('page')
        object_list = paginator.get_page(page)
        context = {"object_list": object_list}
        return render(request, self.template_name, context)
