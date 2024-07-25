from . import views
from django.urls import path

urlpatterns = [
   
    path('send/', views.send_otp, name='send_otp'),
    path('verify/', views.verify_otp, name='verify_otp'),
    # path('create_password/',views.create_password, name='create_password')

]
