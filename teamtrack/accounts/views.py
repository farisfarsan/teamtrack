from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User
from teamtrack.core.utils import PermissionMixin

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email"); pwd = request.POST.get("password")
        user = authenticate(request, email=email, password=pwd)
        if user:
            login(request, user)
            return redirect("dashboard:home")
        messages.error(request, "Invalid credentials")
    return render(request, "accounts/login.html")

def logout_view(request):
    logout(request)
    return redirect("accounts:login")

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'user': request.user})

@login_required
def profile_update(request):
    if request.method == 'POST':
        user = request.user
        user.name = request.POST.get('name', user.name)
        user.email = request.POST.get('email', user.email)
        
        # Only allow team change for Project Managers
        if PermissionMixin.is_project_manager(request.user):
            user.team = request.POST.get('team', user.team)
        
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('accounts:profile')
    
    return render(request, 'accounts/profile_update.html', {'user': request.user})
