# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django.core.exceptions import ValidationError
from .models import UploadedFile
from .models import Student
from .models import DynamicColumn, DynamicValue
from django.contrib.auth import authenticate
from .models import SchoolClass

class SchoolClassForm(forms.ModelForm):
    class Meta:
        model = SchoolClass
        fields = '__all__'
        widgets = {
            'teacher': forms.Select(attrs={'class': 'form-control'}),
            'students': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'teaching_assistants': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
        

class DynamicValueForm(forms.ModelForm):
    class Meta:
        model = DynamicValue
        fields = ['value_char', 'value_int', 'value_date', 'value_bool']

    def __init__(self, *args, **kwargs):
        column = kwargs.pop('column', None)
        super().__init__(*args, **kwargs)
        if column:
            if column.data_type == 'char':
                self.fields['value_char'].widget = forms.TextInput()
                self.fields['value_char'].label = column.name
                self.fields['value_int'].widget = forms.HiddenInput()
                self.fields['value_date'].widget = forms.HiddenInput()
                self.fields['value_bool'].widget = forms.HiddenInput()
            elif column.data_type == 'int':
                self.fields['value_int'].widget = forms.NumberInput()
                self.fields['value_int'].label = column.name
                self.fields['value_char'].widget = forms.HiddenInput()
                self.fields['value_date'].widget = forms.HiddenInput()
                self.fields['value_bool'].widget = forms.HiddenInput()
            elif column.data_type == 'date':
                self.fields['value_date'].widget = forms.DateInput(attrs={'type': 'date'})
                self.fields['value_date'].label = column.name
                self.fields['value_char'].widget = forms.HiddenInput()
                self.fields['value_int'].widget = forms.HiddenInput()
                self.fields['value_bool'].widget = forms.HiddenInput()
            elif column.data_type == 'bool':
                self.fields['value_bool'].widget = forms.CheckboxInput()
                self.fields['value_bool'].label = column.name
                self.fields['value_char'].widget = forms.HiddenInput()
                self.fields['value_int'].widget = forms.HiddenInput()
                self.fields['value_date'].widget = forms.HiddenInput()

class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email", "phone_number", "address"]

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )
    user_type = forms.ChoiceField(choices=CustomUser.USER_TYPE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2", "user_type"]

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input-box', 'placeholder': 'نام کاربری یا کد ملی'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input-box', 'placeholder': 'رمز عبور'})
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            # اگر کاربر با کد ملی وارد شده باشد
            user = CustomUser.objects.filter(national_code=username).first()
            if user:
                username = user.username  # نام کاربری را برای احراز هویت تنظیم کنید

            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("نام کاربری یا رمز عبور اشتباه است!")
            elif not self.user_cache.is_active:
                raise forms.ValidationError("این حساب غیرفعال است!")

        return self.cleaned_data

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "input-box", "placeholder": "Enter your email"}))

class OTPVerificationForm(forms.Form):
    otp = forms.CharField(widget=forms.TextInput(attrs={"class": "input-box", "placeholder": "Enter your OTP"}))

class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "input-box", "placeholder": "Enter new password"}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "input-box", "placeholder": "Confirm new password"}))


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']




class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }


