from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect

from assignments.models import About
from .forms import RegisterForm
from blogs.models import Category, Blog


def home(request):
    featured_posts = Blog.objects.filter(is_featured=True, status='published').order_by('updated_at')
    posts = Blog.objects.filter(is_featured=False, status='published')


    #Fetch about us
    try:
        about = About.objects.get()
    except:
        about = None



    context = {
               'featured_posts': featured_posts,
               'posts': posts,
               'about': about,

               }

    return render(request,'home.html',context)



def register(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('register')
        else:
            print(form.errors)
    else:
        form = RegisterForm()

    context = {
        'form': form,
    }

    return render(request,'register.html')

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
            return redirect('dashboard')
    form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request,'login.html')

def logout(request):
    auth.logout(request)
    return redirect('home')