from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseNotFound,HttpResponse
from .forms import SignUpForm, LoginForm, PatientSignupForm, DoctorSignupForm, BlogPostForm , DoctorProfile , PatientSignupForm
from .models import User, DoctorProfile, BlogPost

def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        if user_type == 'patient':
            form = PatientSignupForm(request.POST, request.FILES)
        else:
            form = DoctorSignupForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = user_type
            user.save()
            login(request, user)
            messages.success(request, 'Signup successful!')
            if user.user_type == 'patient':
                return redirect('patient_dashboard')
            elif user.user_type == 'doctor':
                return redirect('doctor_dashboard')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
                if user.user_type == 'patient':
                    return redirect('patient_dashboard')
                elif user.user_type == 'doctor':
                    return redirect('doctor_dashboard')
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Logout successful!')
    return redirect('index')

@login_required
def patient_dashboard(request):
    return render(request, 'patient_dashboard.html')

@login_required
def doctor_dashboard(request):
    return render(request, 'doctor_dashboard.html')

def view_blogs(request):
    blogs = BlogPost.objects.all()
    return render(request, 'view_blogs.html', {'blogs': blogs})

def profile_required(request):
    return render(request, 'profile_required.html')




@login_required
def create_blog(request):
    if not request.user.is_doctor():
        return HttpResponseNotFound("Only doctors can create blog posts.")

    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Check if user has an associated DoctorProfile
                doctor_profile = request.user.doctorprofile
                
                # Save the blog post with the doctor profile as the author
                blog_post = form.save(commit=False)
                blog_post.author = doctor_profile
                blog_post.save()

                return redirect('view_blogs')
            except DoctorProfile.DoesNotExist:
                # Handle the case where there is no DoctorProfile
                return HttpResponse("Doctor profile does not exist. Please complete your profile.", status=400)
    else:
        form = BlogPostForm()

    return render(request, 'create_blog.html', {'form': form})






def error_page(request):
    return render(request, 'error_page.html', {})

@login_required
def update_profile(request):
    try:
        doctor_profile = DoctorProfile.objects.get(user=request.user)
    except DoctorProfile.DoesNotExist:
        return HttpResponseNotFound("Doctor profile not found for the user.")
    
    if request.method == 'POST':
        form = DoctorProfile(request.POST, request.FILES, instance=doctor_profile)
        if form.is_valid():
            form.save()
            return redirect('doctor_dashboard')  # Redirect to a relevant page after update
    else:
        form = DoctorProfile(instance=doctor_profile)
    
    return render(request, 'update_profile.html', {'form': form})