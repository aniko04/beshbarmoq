from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings
from functools import wraps
from .models import Result, Profile, Material
from . import rasmli_test
from . import diktant
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
    """6–10 mashq sahifalari faqat talaba uchun; aks holda Multimediya bo'limiga qaytaradi."""
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not is_talaba(request.user):
            return redirect('/multimediya')
        return view_func(request, *args, **kwargs)
    return _wrapped


def _safe_next(request):
    """Login/ro'yxatdan keyin qaytariladigan xavfsiz ichki URL (ochiq-redirectdan himoya)."""
    nxt = request.GET.get('next', '')
    if nxt and url_has_allowed_host_and_scheme(
        nxt, allowed_hosts={request.get_host()}, require_https=request.is_secure()
    ):
        return nxt
    return '/'


# ===== Platforma bo'limlari =====
def home(request):
    """Bosh sahifa: platforma haqida va yetti bo'lim."""
    return render(request, 'index.html', {'active': 'home'})


def haqida(request):
    """1-bo'lim — muallif va platforma haqida."""
    muallif_foto = (settings.MEDIA_ROOT / 'muallif.jpg').exists()
    return render(request, 'haqida.html', {
        'active': 'haqida',
        'muallif_foto': muallif_foto,
    })


def multimediya(request):
    """4-bo'lim — 10 ta interaktiv topshiriq (avvalgi bosh sahifa)."""
    return render(request, 'multimediya.html', {
        'active': 'multimediya',
        'show_advanced': is_talaba(request.user),
    })


def _bolim(request, section, nomi, lede, sarlavha, guruhlash=None, ilova=None):
    """Admin orqali to'ldiriladigan material bo'limlarining umumiy ko'rinishi.

    `guruhlash` berilsa (masalan Topshiriq bo'limida), materiallar kichik
    bo'limlarga ajratiladi va sahifada har biri ochiladigan ro'yxat bo'lib
    chiqadi. Kichik bo'limi belgilanmagan materiallar guruhlardan tashqarida,
    ro'yxat boshida oddiy karta bo'lib qoladi.

    `ilova` — kichik bo'lim kaliti bo'yicha interaktiv sahifaga havola
    (masalan «Rasmli test» guruhidagi onlayn test): {kalit: {...}}.
    """
    hammasi = list(Material.objects.filter(section=section, is_published=True))
    guruhlar = []
    guruhsiz = hammasi
    if guruhlash:
        kalitlar = [kalit for kalit, _ in guruhlash]
        guruhlar = [
            {
                'kalit': kalit,
                'nomi': guruh_nomi,
                'materiallar': [m for m in hammasi if m.kichik_bolim == kalit],
                'ilova': (ilova or {}).get(kalit),
            }
            for kalit, guruh_nomi in guruhlash
        ]
        guruhsiz = [m for m in hammasi if m.kichik_bolim not in kalitlar]

    return render(request, 'bolim.html', {
        'active': section,
        'bolim_nomi': nomi,
        'bolim_lede': lede,
        'bolim_sarlavha': sarlavha,
        'materiallar': guruhsiz,
        'guruhlar': guruhlar,
        'jami': len(hammasi),
    })


def metodika(request):
    """2-bo'lim — metodik tavsiyalar."""
    return _bolim(
        request, Material.SECTION_METODIKA, "Metodika",
        "Inkorporatsion yondashuv, fanlararo integratsiya va interfaol metodlar bo'yicha "
        "metodik tavsiyalar hamda zamonaviy pedagogik yondashuvlar.",
        "Metodik tavsiyalar",
    )


def maqola(request):
    """3-bo'lim — ilmiy maqolalar."""
    return _bolim(
        request, Material.SECTION_MAQOLA, "Maqola",
        "Tadqiqot doirasida chop etilgan ilmiy va ilmiy-metodik maqolalar, "
        "konferensiya tezislari va nashrlar.",
        "Nashr etilgan maqolalar",
    )


def topshiriq(request):
    """5-bo'lim — amaliy topshiriqlar; ikki kichik bo'limga ajratilgan."""
    return _bolim(
        request, Material.SECTION_TOPSHIRIQ, "Topshiriq",
        "Sinfda va uyda bajarish uchun amaliy topshiriqlar to'plami hamda "
        "ularni baholash mezonlari.",
        "Amaliy topshiriqlar",
        guruhlash=Material.KICHIK_BOLIM_CHOICES,
        ilova={
            Material.KICHIK_RASMLI_TEST: {
                'url': '/topshiriq/rasmli-test',
                'sarlavha': "Onlayn rasmli test",
                'tavsif': "2–4-sinf o'quvchilari uchun {} ta topshiriq, {} ball, "
                          "{} daqiqa. Javoblar shu yerda tekshiriladi.".format(
                              len(rasmli_test.savollar()), rasmli_test.jami_ball(),
                              rasmli_test.DAQIQA),
                'tugma': "Testni boshlash",
            },
            Material.KICHIK_DIKTANT: {
                'url': '/topshiriq/diktantlar',
                'sarlavha': "Onlayn texnologik diktant",
                'tavsif': "{} bosqich, har birida {} ta topshiriq va {} daqiqa. "
                          "Bosqichlar ketma-ket ochiladi.".format(
                              diktant.BOSQICH_SONI,
                              len(diktant.bosqichlar()[0]['savollar']),
                              diktant.BOSQICH_DAQIQA),
                'tugma': "Diktantni boshlash",
            },
        },
    )


def rasmli_test_sahifa(request):
    """Topshiriq bo'limining «Rasmli test» kichik bo'limi — interaktiv test.

    Savollar va javob kaliti `home/rasmli_test.py` da; sahifa o'sha ma'lumotdan
    yig'iladi, tekshirish esa brauzerda bo'ladi (natija login qilganlarda
    `/api/save-result` orqali saqlanadi).
    """
    return render(request, 'rasmli_test.html', {
        'active': 'topshiriq',
        'savollar': rasmli_test.savollar(),
        # json_script shablonda o'zi JSON qiladi — bu yerda lug'atning o'zi beriladi.
        'javoblar': rasmli_test.javob_kaliti(),
        'jami_ball': rasmli_test.jami_ball(),
        'jami_qator': rasmli_test.jami_qator(),
        'qator_ball': rasmli_test.QATOR_BALL,
        'daqiqa': rasmli_test.DAQIQA,
    })


def diktant_sahifa(request):
    """Topshiriq bo'limining «Texnologik diktantlar» kichik bo'limi.

    Worddagi to'rt variant — to'rt bosqich. Sahifa hammasini bir marta
    yuboradi, lekin bir vaqtda bittasi ko'rinadi: bosqich tekshirilgandan
    keyin keyingisi ochiladi (JS, sahifa yangilanmaydi). Har bosqich
    natijasi `dikt1`…`dikt4` kaliti bilan alohida saqlanadi.
    """
    return render(request, 'diktant.html', {
        'active': 'topshiriq',
        'bosqichlar': diktant.bosqichlar(),
        # json_script shablonda o'zi JSON qiladi — bu yerda lug'atning o'zi beriladi.
        'javoblar': diktant.javob_kaliti(),
        'raqamlar': diktant.RAQAMLAR,
        'qator_ball': diktant.QATOR_BALL,
        'bosqich_ball': diktant.bosqich_ball(),
        'jami_ball': diktant.jami_ball(),
        'daqiqa': diktant.BOSQICH_DAQIQA,
    })


def xarita(request):
    """6-bo'lim — instruksion texnologik xaritalar."""
    return _bolim(
        request, Material.SECTION_XARITA, "Instruksion texnologik xarita",
        "Amaliy mavzular bo'yicha bosqichma-bosqich texnologik xaritalar: "
        "ish ketma-ketligi, kerakli jihozlar va xavfsizlik qoidalari.",
        "Texnologik xaritalar",
    )


def ishlanma(request):
    """7-bo'lim — namunaviy dars ishlanmalari."""
    return _bolim(
        request, Material.SECTION_ISHLANMA, "Dars ishlanmalar",
        "Namunaviy dars ishlanmalari: dars maqsadi, kerakli jihozlar, dars bosqichlari "
        "va kutilayotgan natijalar.",
        "Namunaviy dars ishlanmalari",
    )


def login_view(request):
    """Login sahifasi."""
    if request.user.is_authenticated:
        return redirect(_safe_next(request))
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(_safe_next(request))
        else:
            return render(request, 'login.html', {'error': "Login yoki parol noto'g'ri!"})
    return render(request, 'login.html')


def register_view(request):
    """Ro'yxatdan o'tish sahifasi."""
    if request.user.is_authenticated:
        return redirect(_safe_next(request))
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
        return redirect(_safe_next(request))
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


# ===== 1–5 mashqlar (barcha rollar uchun; login shart) =====
@login_required
def mashq1(request):
    return render(request, 'mashq1.html')

@login_required
def mashq2(request):
    return render(request, 'mashq2.html')

@login_required
def mashq3(request):
    return render(request, 'mashq3.html')

@login_required
def mashq4(request):
    return render(request, 'mashq4.html')

@login_required
def mashq5(request):
    return render(request, 'mashq5.html')


# ===== O'quvchi uchun 6-mashq (talaba formati bilan bir xil; login shart) =====
@login_required
def oquvchi_m6a(request):
    return render(request, 'oquvchi/m6a.html')

@login_required
def oquvchi_m6b(request):
    return render(request, 'oquvchi/m6b.html')

@login_required
def oquvchi_m6c(request):
    return render(request, 'oquvchi/m6c.html')


# ===== O'quvchi uchun 7-mashq (Origami) =====
@login_required
def oquvchi_m7a(request):
    return render(request, 'oquvchi/m7a.html')

@login_required
def oquvchi_m7b(request):
    return render(request, 'oquvchi/m7b.html')

@login_required
def oquvchi_m7c(request):
    return render(request, 'oquvchi/m7c.html')


# ===== O'quvchi uchun 8-mashq (Fetr) — to'liq =====
@login_required
def oquvchi_m8a(request):
    return render(request, 'oquvchi/m8a.html')

@login_required
def oquvchi_m8b(request):
    return render(request, 'oquvchi/m8b.html')

@login_required
def oquvchi_m8c(request):
    return render(request, 'oquvchi/m8c.html')


# ===== O'quvchi uchun 9-mashq (Kvilling) — to'liq =====
@login_required
def oquvchi_m9a(request):
    return render(request, 'oquvchi/m9a.html')

@login_required
def oquvchi_m9a2(request):
    return render(request, 'oquvchi/m9a2.html')

@login_required
def oquvchi_m9b(request):
    return render(request, 'oquvchi/m9b.html')

@login_required
def oquvchi_m9c(request):
    return render(request, 'oquvchi/m9c.html')


# ===== O'quvchi uchun 10-mashq (Loy/plastilin) — to'liq =====
@login_required
def oquvchi_m10a(request):
    return render(request, 'oquvchi/m10a.html')

@login_required
def oquvchi_m10b(request):
    return render(request, 'oquvchi/m10b.html')

@login_required
def oquvchi_m10c(request):
    return render(request, 'oquvchi/m10c.html')


# ===== 6–10 mashqlar (faqat talaba; login ham shart) =====
@login_required
@talaba_required
def mashq6a(request):
    return render(request, 'mashq6a.html')

@login_required
@talaba_required
def mashq6b(request):
    return render(request, 'mashq6b.html')

@login_required
@talaba_required
def mashq6c(request):
    return render(request, 'mashq6c.html')

@login_required
@talaba_required
def mashq7a(request):
    return render(request, 'mashq7a.html')

@login_required
@talaba_required
def mashq7b(request):
    return render(request, 'mashq7b.html')

@login_required
@talaba_required
def mashq7c(request):
    return render(request, 'mashq7c.html')

@login_required
@talaba_required
def mashq8a(request):
    return render(request, 'mashq8a.html')

@login_required
@talaba_required
def mashq8b(request):
    return render(request, 'mashq8b.html')

@login_required
@talaba_required
def mashq8c(request):
    return render(request, 'mashq8c.html')

@login_required
@talaba_required
def mashq9a(request):
    return render(request, 'mashq9a.html')

@login_required
@talaba_required
def mashq9a2(request):
    return render(request, 'mashq9a2.html')

@login_required
@talaba_required
def mashq9b(request):
    return render(request, 'mashq9b.html')

@login_required
@talaba_required
def mashq9c(request):
    return render(request, 'mashq9c.html')

@login_required
@talaba_required
def mashq10a(request):
    return render(request, 'mashq10a.html')

@login_required
@talaba_required
def mashq10b(request):
    return render(request, 'mashq10b.html')

@login_required
@talaba_required
def mashq10c(request):
    return render(request, 'mashq10c.html')
