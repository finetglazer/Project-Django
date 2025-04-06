from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from .forms import RegistrationForm
from .models import UserAccount
from django.views.decorators.csrf import csrf_exempt
import logging
from django.contrib.auth.hashers import check_password
from .services.auth_service import AuthService

logger = logging.getLogger('accounts')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = UserAccount.objects.get(username=username)
        except UserAccount.DoesNotExist:
            messages.error(request, "Invalid username or password.")
            return redirect('accounts:login')

        if check_password(password, user.password):
            # Manually set the backend attribute so that Django knows how to handle the session
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            messages.success(request, "Logged in successfully!")
            # Redirect to index or any other page
            return redirect('accounts:index')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('accounts:login')
    return render(request, 'accounts/login.html')


# Logout view
def logout_view(request):
    logout(request)
    return redirect('accounts:login')


@csrf_exempt
def register(request):
    if request.method == 'POST':
        logger.debug('Register POST request received.')  # Debug before form processing

        form = RegistrationForm(request.POST)
        if form.is_valid():
            logger.debug('Registration form is valid.')

            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            messages.success(request, 'Account created successfully. Redirecting to login...')
            logger.debug(f'User {user.username} registered successfully.')

            return redirect('accounts:login')
        else:
            logger.warning('Invalid registration form data.')
            messages.error(request, 'Invalid form data')

        return redirect('accounts:register')

    logger.debug('Rendering registration page.')
    return render(request, 'accounts/register.html')


# index, now just display the html, no logic code
def index(request):
    return render(request, 'accounts/index.html')


# index, now just display the html, no logic code
def indexStaff(request):
    return render(request, 'accounts/indexStaff.html')