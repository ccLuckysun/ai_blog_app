from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return render(request, 'dashboard.html')

    return render(request, 'index.html')


def index_redirect(request):
    return redirect('index')


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


def user_login(request):
    next_url = request.POST.get('next') or request.GET.get('next') or ''

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if next_url and url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                return redirect(next_url)
            return redirect('index')

        return render(request, 'login.html', {
            'error': 'Invalid username or password.',
            'username': username,
            'next': next_url,
        })

    return render(request, 'login.html', {'next': next_url})


def user_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        errors = []

        if not username:
            errors.append('Username is required.')
        if not email:
            errors.append('Email is required.')
        if not password:
            errors.append('Password is required.')
        if username and User.objects.filter(username=username).exists():
            errors.append('Username already exists.')
        if email and User.objects.filter(email=email).exists():
            errors.append('Email already exists.')
        if password and password != confirm_password:
            errors.append('Passwords do not match.')

        if errors:
            return render(request, 'signup.html', {
                'errors': errors,
                'username': username,
                'email': email,
            })

        User.objects.create_user(username=username, email=email, password=password)
        return redirect('login')

    return render(request, 'signup.html')


def user_logout(request):
    logout(request)
    return redirect('index')


@login_required
def all_blogs(request):
    return render(request, 'all-blogs.html')


@login_required
def blog_details(request):
    return render(request, 'blogs-details.html')
