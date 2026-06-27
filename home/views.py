from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from functools import wraps
from .models import Result, Profile
import json


# ===== Rol yordamchilari =====
def is_talaba(user):
    """6–10 mashqlarni ko'rish huquqi: talaba roli yoki xodim (admin/o'qituvchi)."""
    if not user.is_authenticated:
        return False
    if user.is_staff:
        return True
    return Profile.objects.filter(user=user, role=Profile.ROLE_TALABA).exists()


def talaba_required(view_func):
    """6–10 mashq sahifalari faqat talaba uchun; aks holda bosh sahifaga qaytaradi."""
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not is_talaba(request.user):
            return redirect('/')
        return view_func(request, *args, **kwargs)
    return _wrapped


# Create your views here.
def home(request):
    """Platforma haqida sahifa."""
    return render(request, 'index.html', {'show_advanced': is_talaba(request.user)})


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
        role = request.POST.get('role', Profile.ROLE_OQUVCHI)
        if role not in (Profile.ROLE_OQUVCHI, Profile.ROLE_TALABA):
            role = Profile.ROLE_OQUVCHI

        if not username or not password:
            return render(request, 'register.html', {'error': "Barcha maydonlarni to'ldiring!", 'role': role})
        if password != password2:
            return render(request, 'register.html', {'error': "Parollar mos kelmadi!", 'role': role})
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': "Bu login allaqachon mavjud!", 'role': role})

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        Profile.objects.create(user=user, role=role)
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


# ===== 1–5 mashqlar (barcha rollar uchun) =====
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


# ===== O'quvchi uchun 6-mashq (talaba formati bilan bir xil; ochiq) =====
def oquvchi_m6a(request):
    return render(request, 'oquvchi/m6a.html')

def oquvchi_m6b(request):
    return render(request, 'oquvchi/m6b.html')

def oquvchi_m6c(request):
    return render(request, 'oquvchi/m6c.html')


# ===== O'quvchi uchun 7-mashq (talaba formati bilan bir xil; ochiq) =====
def oquvchi_m7a(request):
    return render(request, 'oquvchi/m7a.html')

def oquvchi_m7b(request):
    return render(request, 'oquvchi/m7b.html')

def oquvchi_m7c(request):
    return render(request, 'oquvchi/m7c.html')


# ===== O'quvchi uchun 8-mashq (Fetr) — to'liq =====
def oquvchi_m8a(request):
    return render(request, 'oquvchi/m8a.html')

def oquvchi_m8b(request):
    return render(request, 'oquvchi/m8b.html')

def oquvchi_m8c(request):
    return render(request, 'oquvchi/m8c.html')


# ===== O'quvchi uchun 9-mashq (Kvilling) — hozircha faqat video =====
def oquvchi_m9a(request):
    return render(request, 'oquvchi/m9a.html')

def oquvchi_m9a2(request):
    return render(request, 'oquvchi/m9a2.html')


# ===== O'quvchi uchun 10-mashq (Loy/plastilin) — to'liq =====
def oquvchi_m10a(request):
    return render(request, 'oquvchi/m10a.html')

def oquvchi_m10b(request):
    return render(request, 'oquvchi/m10b.html')

def oquvchi_m10c(request):
    return render(request, 'oquvchi/m10c.html')


# ===== 6–10 mashqlar (hozircha faqat talaba uchun) =====
@talaba_required
def mashq6a(request):
    return render(request, 'mashq6a.html')

@talaba_required
def mashq6b(request):
    return render(request, 'mashq6b.html')

@talaba_required
def mashq6c(request):
    return render(request, 'mashq6c.html')

@talaba_required
def mashq7a(request):
    return render(request, 'mashq7a.html')

@talaba_required
def mashq7b(request):
    return render(request, 'mashq7b.html')

@talaba_required
def mashq7c(request):
    return render(request, 'mashq7c.html')

@talaba_required
def mashq8a(request):
    return render(request, 'mashq8a.html')

@talaba_required
def mashq8b(request):
    return render(request, 'mashq8b.html')

@talaba_required
def mashq8c(request):
    return render(request, 'mashq8c.html')

@talaba_required
def mashq9a(request):
    return render(request, 'mashq9a.html')

@talaba_required
def mashq9a2(request):
    return render(request, 'mashq9a2.html')

@talaba_required
def mashq9b(request):
    return render(request, 'mashq9b.html')

@talaba_required
def mashq9c(request):
    return render(request, 'mashq9c.html')

@talaba_required
def mashq10a(request):
    return render(request, 'mashq10a.html')

@talaba_required
def mashq10b(request):
    return render(request, 'mashq10b.html')

@talaba_required
def mashq10c(request):
    return render(request, 'mashq10c.html')
