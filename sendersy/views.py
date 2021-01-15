from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegistrationForm
from .models import Message
from django.contrib.auth.models import User
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
        context = {
            'msgs':request.user.messages.all()[::-1],
            'link':'http://127.0.0.1:8000/newmessage/' + request.user.username
        }
        return render(request, 'dashboard.html',context=context)
    else:
        messages.error(request,'Please sign-in to access dashboard.')
        return redirect('signin')

def delMsg(request):
    msg_id = int(request.POST.get('msg_id'))
    Message.objects.get(pk=msg_id).delete()
    return redirect('dashboard')

def message(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = None

    if request.method=='GET':
        if user:
            context = {'name':user.first_name}
            return render(request, "newmessage.html", context=context)
        else:
            return HttpResponse(f"<center><h2>Sorry, {username} is not a registered user.</h2></center>")
    
    else:
        message = request.POST.get('message',None)
        by = request.POST.get('by','Anonymous')
        if message and by:
            Message.objects.create(content=message, to=user, by=by).save()
            messages.success(request,f'Your message for {user.first_name} was recorded.')
            return redirect(request.path_info)
