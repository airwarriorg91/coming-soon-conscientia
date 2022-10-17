from django.shortcuts import render
from collections import UserList
from email.message import EmailMessage
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login

from django.core.mail import EmailMessage

from django.contrib.auth import login
from django.utils.encoding import force_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site

from django.views.generic import View

from .tokens import token_generator

from django.views.decorators.csrf import csrf_protect

@csrf_protect
def createEmail(request, user):
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    domain = get_current_site(request).domain
    link = reverse('activate', kwargs={'uidb64':uidb64, 'token':token_generator.make_token(user)})
    activate_url = 'https://' + domain + link
    email_subject = 'Activate your account'

    email_body = f"Hi there, {user.first_name}!\n" \
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
        [user.username],
    )
    return email_msg


# Create your views here.
@csrf_protect
def saveAccount(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        college = request.POST['college']
        context = {'status' : 'True', 'user_name': name}
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
                #user = authenticate(request, username=email, password=password)
                #login(request, user)
                #user.save()
                #return redirect('login')
                email_msg = createEmail(request, user)
                email_msg.send()
                context['status'] = 'True'
                context['user_name'] = name
                return render(request,'verification.html', context=context)
        return render(request,"verification.html", context=context)


@csrf_protect
def loginView(request):
    context = {'title':None}
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)
        login(request, user)
        user.save()
    else:
        context['title'] = 'Oops! Something went wrong.'
        return render(request, 'login.html', context=context)
    user = request.user
    print('is_active: ',user.is_active)
    if user is not None:
        if user.is_active:
            return redirect('continue')
        else:
            return redirect('verify')
    return redirect('index')

def logout_defined(request):
    request.user.logout()
    redirect('index')


class VerificationView(View):
    def get(self, request, uidb64, token):
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.all().filter(pk=uid)[0]
        user.is_active = True
        user.save()
        #login(request, user)
        return redirect('login')

def continueView(request):
    if request.user.is_active:
        return render(request, 'register2.html')
    else:
        return redirect('verification')

@csrf_protect
def eventRegisterView(request):
    event_name = {'event1':'War of Bots','event2':'Dronetrix','event3':'RC Plane','event4':'Amphibot',
    'event5': 'RC Car', 'event6':'Line Follower', 'event7':'Space Habitat Challenge', 'event8':'Water Rocket','event9':'Panchmantra','event10':'Arduino 2.0','event11':'Vyomverse'
    ,'event12':'Valorant','event13':'Machinist','event14':'Hangover','event15':'TechGlide','event16':'PhyKnight','event17':'CAD','event18':'Logic Circuit Design','event19':'Circuiter'
    ,'event20':'Tarang','event21':'Night Sky Hunt','event22':'How Adam Did It','event23':'Techwiz','event24':'Bletchley Park','event25':'C Cubed','event26':'Cosmic Clash','event27':'Astroreflection'
    ,'event28':'FIFA', 'event29':'Mathematrix', 'event30':'3-MPT'
    ,'event31':'Fusion360', 'event32':'Simulations','event33':'Rocketry Workshop','event34':'MATLAB Workshop'}
    eventnames = ''
    if request.method == 'POST':
        events = request.POST.getlist('event[]')
        for event in events:
            group = Group.objects.get(name=event)
            request.user.groups.add(group)
            eventnames += event_name[event] + ', '

    email_body = f"Hello {request.user.first_name}!\n"\
"Thank you for registering in the events/workshops. You have registered for the following workshops,\n"\
f"Selected Events :- {eventnames[:-2]}\n"\
"Workshop Registration Fees: Rs.1000 (War of Bots), Rs.500 (Dronetrix - RC Car), Rs.200 (Line Follower - FIFA), Rs.100 (Mathematrix)\n"\
"To confirm your participation, kindly deposit your Workshop Fees to this UPI ID: akash629001@okhdfcbank. "\
"Please share a screenshot of your payment to 6369312390 through Whatsapp to accelerate the verification."\
"Allow us to confirm your payment and we will get back to you within 24 hours. For any queries, consider contacting us through the phone numbers or email us at contact@conscientia.co.in (Please try to reach us after 5 PM on weekdays).\n"\
"If you interested in staying in our campus during the events, kindly fill the attached Google Form,"\
"\n"\
"Thanks and Regards\n"\
"Team Conscientia\n"\
"Indian Institute of Space Science and Technology\n"\
"Thiruvanthapuram\n"\
"contact@conscientia.co.in\n"\
"Phone: 6369312390/9083722796\n"

    email_subject="Payment and finalization of event/workshop registration"
    email_msg = EmailMessage(
        email_subject,
        email_body,
        None,
        [request.user.username],
    )
    email_msg.send()
    context={"title":"Confirmation email sent","message":"Registration successful, kindly complete the payment."}
    return render(request, 'events.html',context=context)
