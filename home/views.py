from django.shortcuts import render, redirect
from django.http import HttpResponse

def index(request):
    return render(request,'index.html')

def register(request):
    return redirect('https://forms.gle/ZPRw3oyiMpKcZdU37')

def events(request):
    return render(request,'events.html')

def verify(request):
    return render(request,'verification.html')
