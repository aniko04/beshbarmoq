from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Result
import json

# Create your views here.
def home(request):
    """Platforma haqida sahifa."""
    return render(request, 'index.html')


def login_view(request):
    """Login sahifasi."""
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        else:
            return render(request, 'login.html', {'error': "Login yoki parol noto'g'ri!"})
    return render(request, 'login.html')


def register_view(request):
    """Ro'yxatdan o'tish sahifasi."""
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')

        if not username or not password:
            return render(request, 'register.html', {'error': "Barcha maydonlarni to'ldiring!"})
        if password != password2:
            return render(request, 'register.html', {'error': "Parollar mos kelmadi!"})
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': "Bu login allaqachon mavjud!"})

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        login(request, user)
        return redirect('/')
    return render(request, 'register.html')


def logout_view(request):
    """Chiqish."""
    logout(request)
    return redirect('/')


@require_POST
@login_required
def save_result(request):
    """Natijalarni saqlash API."""
    try:
        data = json.loads(request.body)
        mashq = data.get('mashq', '')
        score = int(data.get('score', 0))
        total = int(data.get('total', 0))

        Result.objects.create(
            user=request.user,
            mashq=mashq,
            score=score,
            total=total,
        )
        return JsonResponse({'status': 'ok'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

def mashq1(request):
    return render(request, 'mashq1.html')

def mashq2(request):
    return render(request, 'mashq2.html')

def mashq3(request):
    return render(request, 'mashq3.html')

def mashq4(request):
    return render(request, 'mashq4.html')

def mashq5(request):
    return render(request, 'mashq5.html')

def mashq6a(request):
    return render(request, 'mashq6a.html')

def mashq6b(request):
    return render(request, 'mashq6b.html')

def mashq6c(request):
    return render(request, 'mashq6c.html')

def mashq7a(request):
    return render(request, 'mashq7a.html')

def mashq7b(request):
    return render(request, 'mashq7b.html')

def mashq7c(request):
    return render(request, 'mashq7c.html')

def mashq8a(request):
    return render(request, 'mashq8a.html')

def mashq8b(request):
    return render(request, 'mashq8b.html')

def mashq8c(request):
    return render(request, 'mashq8c.html')

def mashq9a(request):
    return render(request, 'mashq9a.html')

def mashq9a2(request):
    return render(request, 'mashq9a2.html')

def mashq9b(request):
    return render(request, 'mashq9b.html')

def mashq9c(request):
    return render(request, 'mashq9c.html')

def mashq10a(request):
    return render(request, 'mashq10a.html')

def mashq10b(request):
    return render(request, 'mashq10b.html')

def mashq10c(request):
    return render(request, 'mashq10c.html')
