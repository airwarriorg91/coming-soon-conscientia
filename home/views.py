from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request,'index.html')

def register(request):
    return render(request,'register.html')

def events(request):
    return render(request,'fork.html')

def continueView(request):
    if request.user.is_active:
        return redirect('login')
    else:
        return render(request, 'register2.html')

def eventRegisterView(request):
    return HttpResponse(f"{request.POST['task1']}, {request.POST['task2']}, {request.POST['task3']}")

def register2(request):
    return HttpResponse('user = ' + str(request.user) + ' status = ' + str(request.user.is_active))
    #return render(request,'register2.html')

def verify(request):
    return render(request,'verification.html')