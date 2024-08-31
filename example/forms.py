from django import forms
from django.contrib.auth.forms import UserCreationForm
from example.models import User, PatientProfile, DoctorProfile, BlogPost

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Provide a valid email address.')
    user_type = forms.ChoiceField(choices=[('patient', 'Patient'), ('doctor', 'Doctor')], required=True)
    profile_picture = forms.ImageField(required=False, help_text='Optional. Upload a profile picture.')

    address_line1 = forms.CharField(max_length=255, required=False, help_text='Required for patients.')
    city = forms.CharField(max_length=100, required=False, help_text='Required for patients.')
    state = forms.CharField(max_length=100, required=False, help_text='Required for patients.')
    pincode = forms.CharField(max_length=10, required=False, help_text='Required for patients.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'user_type', 
                  'profile_picture', 'address_line1', 'city', 'state', 'pincode')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.user_type = self.cleaned_data['user_type']
        
        if commit:
            user.save()
            if user.user_type == 'patient':
                PatientProfile.objects.create(
                    user=user,
                    address_line1=self.cleaned_data['address_line1'],
                    city=self.cleaned_data['city'],
                    state=self.cleaned_data['state'],
                    pincode=self.cleaned_data['pincode'],
                    profile_picture=self.cleaned_data['profile_picture']
                )
            elif user.user_type == 'doctor':
                DoctorProfile.objects.create(
                    user=user,
                    profile_picture=self.cleaned_data['profile_picture']
                )
        return user

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        
        if password1 != password2:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=128, required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class PatientSignupForm(UserCreationForm):
    address_line1 = forms.CharField(max_length=255, required=True, help_text='Required.')
    city = forms.CharField(max_length=100, required=True, help_text='Required.')
    state = forms.CharField(max_length=100, required=True, help_text='Required.')
    pincode = forms.CharField(max_length=10, required=True, help_text='Required.')
    profile_picture = forms.ImageField(required=True, help_text='Required. Upload a profile picture.')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'address_line1', 'city', 'state', 'pincode', 'profile_picture']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'patient'
        if commit:
            user.save()
            PatientProfile.objects.create(
                user=user,
                address_line1=self.cleaned_data['address_line1'],
                city=self.cleaned_data['city'],
                state=self.cleaned_data['state'],
                pincode=self.cleaned_data['pincode'],
                profile_picture=self.cleaned_data['profile_picture']
            )
        return user


class DoctorSignupForm(UserCreationForm):
    profile_picture = forms.ImageField(required=True, help_text='Required. Upload a profile picture.')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'profile_picture']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'doctor'
        if commit:
            user.save()
            DoctorProfile.objects.create(
                user=user,
                profile_picture=self.cleaned_data['profile_picture']
            )
        return user

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'image', 'category', 'summary', 'content', 'is_draft']
