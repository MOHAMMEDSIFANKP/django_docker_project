from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django import forms

class CustomAuthenticationForm(AuthenticationForm):
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        user = authenticate(username=username, password=password)
        
        if user is not None and not user.is_superuser:
            raise ValidationError('You are not authorized to access the dashboard.')
        return cleaned_data
    
class UserImportForm(forms.Form):
    file = forms.FileField()

    def clean_file(self):
        file = self.cleaned_data["file"]
        allowed_extensions = ('.csv', '.xlsx', '.xls')
        if not file:
            raise forms.ValidationError("Please upload a file")
        if not file.name.lower().endswith(allowed_extensions):
            raise forms.ValidationError("File must be a CSV or Excel file.")
        return file
    