from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from .forms import UserRegistrationForm
# from __future__ import unicode_literals

def home(request):
    return render(request, 'account/home.html')

def signup(request):
    user_exists_error = ""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            userObj = form.cleaned_data
            username = userObj['username']
            email =  userObj['email']
            password =  userObj['password']
            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                User.objects.create_user(username, email, password)
                user = authenticate(username = username, password = password)
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                user_exists_error = "Looks like a username with that email or password already exists"
                # raise forms.ValidationError('Looks like a username with that email or password already exists')
    else:
        form = UserRegistrationForm()

    return render(request, 'account/signup.html', {'form' : form, 'user_exists_error' : user_exists_error})
