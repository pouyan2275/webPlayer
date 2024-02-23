from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,logout
from django.contrib.auth import login
from django.contrib.auth.models import User
from video.models import Streamer

# Create your views here.

def signupandsignin(request):
    return render(request,'account/signupandsignin.html')

def loginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username , password = password)
        if user is None:
            return render(request,'account/signupandsignin.html',{'message':'username or password is incorrect'})
        login(request, user)
    return redirect('/')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            context = {
                'message':'Username is already in use',
                'register' : True
            }
            return render(request, 'account/signupandsignin.html',context)
    user = User.objects.create_user(username, 'lennon@thebeatles.com', password)
    user.save()
    Streamer(user = user, url ='').save()
    user = authenticate(username=username,password = password)
    login(request,user)
    return redirect('/')

def logoutView(request):
    logout(request)
    return redirect('/')