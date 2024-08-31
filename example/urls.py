from django.urls import path
from .views import index, signup, login_view, patient_dashboard, doctor_dashboard, create_blog, view_blogs, update_profile, profile_required

urlpatterns = [
    path('', index, name='index'),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('dashboard/patient/', patient_dashboard, name='patient_dashboard'),
    path('dashboard/doctor/', doctor_dashboard, name='doctor_dashboard'),
    path('blog/create/', create_blog, name='create_blog'),
    path('blogs/', view_blogs, name='view_blogs'),
    path('profile/update/', update_profile, name='update_profile'),
    path('profile/required/', profile_required, name='profile_required'),  # Add this line
]
