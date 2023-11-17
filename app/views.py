from django.shortcuts import render

# Create your views here.
import email
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from .models import *
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth  import authenticate,  login, logout

def handleLogin(request):
    if request.method=="POST":
        # Get the post parameters
        usernamelogin=request.POST['usernamelogin']
        passwordlogin=request.POST['passwordlogin']
        user=authenticate(username=usernamelogin, password=passwordlogin)
        print(user)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("services")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("/")
    else:
        return HttpResponse('404')
def handlelogout(request):
    logout(request)
    return redirect("/")

def home(request):
    # For signin form
    print(User.username)
    if request.method == 'POST':
        username = request.POST.get('username')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            if User.objects.filter(username=username).first():
                messages.success(request,'Username  is taken.')
                return redirect('/')
            if User.objects.filter(email = email).first():
                messages.success(request,'Email  is taken.')
                return redirect('/')
            user_obj = User.objects.create(username=username,email=email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user = user_obj, auth_token = auth_token,phone_number=phone_number)
            profile_obj.save()
            send_mail_after_registration(email,auth_token)
            return redirect('/')
        except Exception  as e:
            print(e)                  
    return render(request, 'SR_app/home.html')

def services(request):
    return render(request, 'SR_app/services.html')

def schedule(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        date = request.POST.get('date')
        phone_number = request.POST.get('phone_number')
        schedule_obj = schedule_info.objects.create(fname = fname, lname = lname, date = date, phone_number = phone_number)
        schedule_obj.save()
    return render(request, 'SR_app/scheduling.html')


def updates(request):
    comments= Comments.objects.order_by('-sno')[0:4]
    context={'comments': comments, 'user': request.user}
    return render(request, 'SR_app/updates.html',context)

def academy(request):
    return render(request, 'SR_app/academy.html')

# function  for sending mail while SWigning In to verify email.
def send_mail_after_registration(email,token):
    subject = 'your account  need to be verified'
    message = f'Hi click the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)

# function for verifying email after sending mail.
def verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()
        print(profile_obj)
        if profile_obj:
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request,'Your Email  is Verified.')
            return redirect('/')
        else:
            messages.success(request,'There is an error.')
            return redirect('/')
    except Exception as e:
        print(e)

def postComment(request):
    if request.method == "POST":
        comment=request.POST.get('comment')
        user=request.user
        parentSno= request.POST.get('parentSno')
        if parentSno=="":
            comment=Comments(comment= comment, user=user)
            comment.save()
            messages.success(request, "Your comment has been posted successfully")
        else:
            parent= Comments.objects.get(sno=parentSno)
            comment=Comments(comment= comment, user=user,parent=parent)
            comment.save()
            messages.success(request, "Your reply has been posted successfully")
        
    return redirect("/updates/")