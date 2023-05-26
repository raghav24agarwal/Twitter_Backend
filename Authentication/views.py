from django.http import HttpResponse
from django.shortcuts import redirect, render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str


from Tweet import utils
from .tokens import generate_token
from Authentication import validation
from Twitter_Backend import settings

# Create your views here.
@api_view(['GET'])
def home(request):
    return Response('Please go to respective endpoints.')

@api_view(['POST'])
def signup(request):

    print("inside", request.data)
    username = request.data['username']
    fullname = request.data['fullname']
    email = request.data['email']
    password = request.data['password']


    a = validation.validate_signup(request, username, email)

    if a!= True:
        try:
            fname, lname = fullname.split(" ", 1)
        except:
            fname = fullname
            lname = ""
            
        print(fname, lname)
        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.full_name = fullname

        myuser.is_active = False

        myuser.save()

        newUser= utils.create_user(request.data)
        # print("sigup   ",newUser)

        messages.success(request, "Your Account Created Successfully")

            # Starting the welcome email logic

        subject = "Welcome to the world of Twitter 2.0"

        message = "Hello " + myuser.full_name + "\n\n" + "Welcome to the world of brilliant ideas and substantial thoughts. Presenting you the Twitter 2.0" + "\n\n" + "Thanks!"

        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]

        send_mail(subject, message, from_email, to_list, fail_silently=True)


        # Starting the logic for confirmation email

        current_site = get_current_site(request)
        email_subject = "You are one step away!"

        message1 = render_to_string('emailconfirm.html', {
                'name': myuser.full_name,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
                'token': generate_token.make_token(myuser)
            })

        email = EmailMessage(
            email_subject,
            message1,
            settings.EMAIL_HOST_USER,
            [myuser.email]
        )

        email.fail_silently = True
        email.send()

        return Response("Successful", status=status.HTTP_200_OK)

    else:
        return Response("Error", status=status.HTTP_404_NOT_FOUND)



@api_view(['POST'])
def signin(request):

    username = request.data['username']
    password = request.data['password']
    print("username",username)
    print("password",password)
    user = authenticate(username=username, password=password)
    print("user ", user)

    if user is not None:
        login(request, user)
        fname = user.first_name
        User = utils.find_user(username)
        responsedata = {
            'username': User['username'],
            'fullname': User['fullname'],
            'avatar' : None
        }
        if 'avatar' in User:
            avt = User['avatar']
            responsedata['avatar'] = avt

        messages.success(request, 'USER SUCCESSFULLY LOGGED IN')
        return Response(responsedata, status=status.HTTP_200_OK)

    else:
        messages.error(request, "Bad Credentials or something")
        return Response("Error", status=status.HTTP_404_NOT_FOUND)   
    


def signout(request):
    logout(request)
    messages.success(request, 'User Logged out Sucessfully')
    return redirect('home') 


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)

    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        # return redirect('home')
        return HttpResponse('Activation Successful. You can close this window now.')

    else:
        return HttpResponse('Activation Failed')




