from django.shortcuts import render

# Create your views here.
def base(request):
    return render(request, 'users/base.html')

def home(request):
    return render(request, 'users/home.html')

def login(request):
    return render(request, 'users/login.html')

def signup(request):
    return render(request, 'users/signup.html')

def profile(request):
    return render(request, 'users/userprofile.html')