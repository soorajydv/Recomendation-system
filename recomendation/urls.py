from .views import course_list, fetchEnrollment
from django.urls import path

urlpatterns = [
    path('enrollment/<int:userid>/', fetchEnrollment, name='search'),
    path('courses/', course_list, name='course_list'),
    # path('roadmap/<int:userid>/', generate_roadmap, name='roadmap'),
    
]