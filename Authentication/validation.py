from django.contrib.auth.models import User
from django.contrib import messages

def validate_form(request, username, email, pass1, pass2):
    a = False
   
    if User.objects.filter(username = username):
        messages.error(request, 'Username already taken')
        a = True

    if User.objects.filter(email = email).exists():
        messages.error(request, 'Email already registered')
        a = True
    
    if(pass1 != pass2):
        messages.error(request, 'Confirm password did not match')
        a = True
    
    return a


def validate_signup(request, username, email):
    a = False
   
    if User.objects.filter(username = username):
        print("ins username")
        messages.error(request, 'Username already taken')
        a = True

    if User.objects.filter(email = email).exists():
        print("ins email")
        messages.error(request, 'Email already registered')
        a = True
    
    return a