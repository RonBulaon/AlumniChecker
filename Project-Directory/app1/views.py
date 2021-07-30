# from typing_extensions import Required
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .decorators import allowed_users, unauthenticated_user
from .models import SiteWide


def logoutUser(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "You've been logged out!")
    else:
        messages.error(request, "You are NOT logged in!")

    return redirect('login')


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Welcome! You are now logged in!")
            return redirect('scanner')
        else:
            messages.error(request, 'The Username or Password is incorrect')
    
    context = {}
    return render(request, 'app1/login.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['adminGroup'])
def adminpanel(request):
    sitewide = SiteWide.objects.all().first()
    return render(request, 'app1/adminpanel.html', { 'sitewide':sitewide })
