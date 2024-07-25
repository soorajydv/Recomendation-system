import datetime
from email.message import EmailMessage
from smtplib import SMTPDataError, SMTPException, SMTPRecipientsRefused
from django.http import BadHeaderError, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.core.mail import send_mail
import secrets, json
from recomendation.models import User
from .models import Otp



def send_otp(request):
    email = request.GET.get('email',None)

    #verify user existance
    user = User.objects.filter(email=email).exists()

    if not user:
        return JsonResponse({'message':f'User with email, {email} doesn\'t exist'}, status=400)

    user = User.objects.get(email=email)
    #Send Otp as email, if failed send invalid email
    otp = secrets.token_hex(3)
    
    # email variables
    subject="Password Reset"
    message = f"""
                        Hi {user.fullname}, here is your OTP {otp} 
                        it expires in 5 minute, use the url below to redirect back to the website
                        http://127.0.0.1:8000/verify-email/Sooraj
                        
                        """
    sender = "rajukarki467@gmail.com"
    receiver = [email]


    # send email
    result = send_mail(
            subject,
            message,
            sender,
            receiver,
            fail_silently=False,

        )
    if(result):
        # Save OTP
        Otp.objects.create(token=otp, userid=user, createdat=datetime.datetime.now())
        return JsonResponse({'message':'Email sent'})

    
    return JsonResponse({'message':'OTP not Sent'},status=500)


    
    

def verify_otp(request):
    otp = request.GET.get('otp',None)
    email = request.GET.get('email',None)


    #get user id
    user = User.objects.get(email=email)

    otp_in_db = Otp.objects.get(userid=user)
    if otp_in_db.token==otp:
        return JsonResponse({'message':f'OTP Verified. Now, you can create a new password'})
    
    return JsonResponse({'message':'Invalid OTP'}, status=400)



  
    
        
       
      
    
