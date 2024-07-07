from .views import fetchEnrollment
from django.urls import path

urlpatterns = [
    path('enrollment/<int:userid>/', fetchEnrollment, name='search')
]