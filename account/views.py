from django.shortcuts import render
from collections import UserList
from email.message import EmailMessage
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from django.core.mail import EmailMessage

from django.contrib.auth import login
from django.utils.encoding import force_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site

from django.views.generic import View

from .tokens import token_generator

from django.views.decorators.csrf import csrf_protect

# Create your views here.
@csrf_protect
def saveAccount(request):
#     return render(request, 'noop.html')

# def temp(request):
    name = request.POST['name']
    email = request.POST['email']
    password = request.POST['password']
    college = request.POST['college']
    context = {'status' : 'False', 'user_name': 'No User Found'}
    if not User.objects.filter(username=email).exists():
        if True: #not User.objects.filter(email=email).exists():
            # Note :- 
                # Name :- First Name
                # Email :- email, username
                # password :- password
                # school :- Second Name
            user = User.objects.create_user(username=email, email=email, first_name=name, last_name=college)
            user.set_password(password)
            user.is_active = False
            user.save()

            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))


            domain = get_current_site(request).domain
            link = reverse('activate', kwargs={'uidb64':uidb64, 'token':token_generator.make_token(user)})
            activate_url = 'https://' + domain + link
            email_subject = 'Activate your account'

            email_body = f"Hi there, {name}!\n" \
            f"Please use this link to verify your account. \n Link:{activate_url}\n"\
            "\n"\
            "Regards,\n"\
            "Team Conscientia\n"\
            "Indian Institute of Space Science and Technology\n"\
            "Thiruvanthapuram\n"\
            "contact@conscientia.co.in"
            
            email_msg = EmailMessage(
                email_subject,
                email_body,
                None,
                [email],
            )
            email_msg.send()
            print('sent successfully')
            context['status'] = 'True'
            context['user_name'] = name
            return render(request,'verification.html', context=context)
    return render(request,"verification.html", context=context)

def authenticate_defined(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
    redirect('home')

def logout_defined(request):
    request.user.logout()
    redirect('home')


class VerificationView(View):
    def get(self, request, uidb64, token):
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.all().filter(pk=uid)[0]
        user.is_active = True
        user.save()
        return redirect('register2')
