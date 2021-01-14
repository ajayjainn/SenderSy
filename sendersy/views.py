from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegistrationForm
from .models import Message
# Create your views here.
def home(request):
    return render(request,'index.html')

def signin(request):
    if request.method == "GET":
        return render(request, 'signin.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else: 
            messages.error(request,'Invalid username or password.')
            return redirect('signin')

def signup(request):
    if request.method=='GET':
        return render(request,'signup.html')

    if request.method=='POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Account created successfully.')
            return redirect('dashboard')
        else:
            errors = ''
            for error_type in form.errors.values():
                for error in error_type:
                    errors += error + '\n'
            messages.error(request,errors)
            return redirect('signup')

def logout_(request):
    logout(request)
    messages.info(request, 'Logged out successfully.')  
    return redirect('/') 

def dashboard(request):
    if request.user.is_authenticated:   
        context = {'msgs':request.user.messages.all()[::-1]}
        return render(request, 'dashboard.html',context=context)
    else:
        messages.error(request,'Please sign-in to access dashboard.')
        return redirect('signin')

def delMsg(request):
    msg_id = int(request.POST.get('msg_id'))
    Message.objects.get(pk=msg_id).delete()
    return redirect('dashboard')