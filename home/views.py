from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request,'index.html')

def workshops(request):
    return render(request,'register.html')