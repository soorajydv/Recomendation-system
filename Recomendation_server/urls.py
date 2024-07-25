
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('recomendation.urls')),
    path('otp/',include('reset_password.urls'))
]
