from .views import fetchEnrollment,recomendationFromSearch
from django.urls import path

urlpatterns = [
    path('enrollment/<int:userid>/', fetchEnrollment, name='search'),
    path('searchrecomendation/<int:userid>/', recomendationFromSearch, name='searchrecomendation')
]