from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True, label='First Name')
    last_name = forms.CharField(max_length=100, required=True, label='Last Name')
    phone = forms.CharField(max_length=20, required=False, label='Work Phone Number')
    department = forms.CharField(max_length=100, required=False, label='Department')
    office_location = forms.CharField(max_length=200, required=False, label='Office Location', widget=forms.TextInput(attrs={'placeholder': 'e.g. Building A, Room 122'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']
        help_texts = {
            'username': 'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = 'Must contain at least one uppercase letter, one number, and be 8+ characters.'
        self.fields['password2'].label = 'Confirm Password'

    def save(self, commit=True):
        user = super().save(commit=True)
        profile = user.profile
        profile.department = self.cleaned_data.get('department', '')
        profile.office_location = self.cleaned_data.get('office_location', '')
        profile.phone = self.cleaned_data.get('phone', '')
        profile.save()
        return user

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = UserProfile
        fields = ['department', 'office_location', 'phone']
        widgets = {
            'office_location': forms.TextInput(attrs={'placeholder': 'e.g. Building A, Room 122'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email

    def save(self, user=None, commit=True):
        profile = super().save(commit=False)
        if user:
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            if commit:
                user.save()
        if commit:
            profile.save()
        return profile
