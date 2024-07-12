from .views import fetchEnrollment,recomendationFromSearch
from django.urls import path

urlpatterns = [
    path('recommend/<int:userid>/', fetchEnrollment, name='recommend'),
    path('recommendfromsearch/<int:userid>/', recomendationFromSearch, name='recommendfromsearch')
]