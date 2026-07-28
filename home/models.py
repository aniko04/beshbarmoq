from django.db import models
from django.contrib.auth.models import User


class Result(models.Model):
    """Foydalanuvchi mashq natijalari."""
    MASHQ_CHOICES = [
        ('m1', 'Mashq 1 – Applikatsiya turlari'),
        ('m2', 'Mashq 2 – Origami shakllari'),
        ('m3', 'Mashq 3 – Kasblar'),
        ('m4', 'Mashq 4 – Hunarlar'),
        ('m5', 'Mashq 5 – Ish qurollari'),
        ('m6b', 'Mashq 6 – Applikatsiya bilan ishlash test'),
        ('m7b', 'Mashq 7 – Origami bilan ishlash test'),
        ('m8b', 'Mashq 8 – Fetr test'),
        ('m9b', 'Mashq 9 – Kvilling bilan ishlash test'),
        ('m10b', 'Mashq 10 – Loy va plastilin bilan ishlash test'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Foydalanuvchi")
    mashq = models.CharField(max_length=10, choices=MASHQ_CHOICES, verbose_name="Mashq")
    score = models.IntegerField(default=0, verbose_name="To'g'ri javoblar")
    total = models.IntegerField(default=0, verbose_name="Jami savollar")
    is_passed = models.BooleanField(default=False, verbose_name="O'tdimi?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Sana")

    class Meta:
        verbose_name = "Natija"
        verbose_name_plural = "Natijalar"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        # 100% bo'lsagina o'tdi
        self.is_passed = self.percentage == 100
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} — {self.get_mashq_display()} — {self.score}/{self.total} ({self.percentage}%)"

    @property
    def percentage(self):
        if self.total == 0:
            return 0
        return round(self.score / self.total * 100)


class Material(models.Model):
    """Bo'limlarga joylanadigan metodik material.

    Metodika, maqola, topshiriq, instruksion xarita va dars ishlanmalari —
    hammasi shu modelda saqlanadi; bo'lim `section` maydoni bilan ajratiladi.
    Materialni admin panel orqali qo'shish/tahrirlash mumkin.
    """
    SECTION_METODIKA = 'metodika'
    SECTION_MAQOLA = 'maqola'
    SECTION_TOPSHIRIQ = 'topshiriq'
    SECTION_XARITA = 'xarita'
    SECTION_ISHLANMA = 'ishlanma'
    SECTION_CHOICES = [
        (SECTION_METODIKA, "Metodika"),
        (SECTION_MAQOLA, "Maqola"),
        (SECTION_TOPSHIRIQ, "Topshiriq"),
        (SECTION_XARITA, "Instruksion texnologik xarita"),
        (SECTION_ISHLANMA, "Dars ishlanmalar"),
    ]

    section = models.CharField(
        max_length=20, choices=SECTION_CHOICES, verbose_name="Bo'lim",
    )
    title = models.CharField(max_length=250, verbose_name="Sarlavha")
    summary = models.TextField(
        blank=True, verbose_name="Qisqacha tavsif",
        help_text="Ro'yxatda sarlavha ostida ko'rinadi. 1–3 gap yetarli.",
    )
    body = models.TextField(
        blank=True, verbose_name="To'liq matn",
        help_text="Ixtiyoriy. Har bir bo'sh qator yangi xatboshi bo'ladi.",
    )
    file = models.FileField(
        upload_to='materiallar/', blank=True, null=True, verbose_name="Fayl",
        help_text="PDF, Word yoki taqdimot. Yuklansa, 'Yuklab olish' tugmasi chiqadi.",
    )
    # ImageField emas, FileField: ImageField Pillow talab qiladi, u esa
    # loyiha muhitiga o'rnatilmagan (o'rnatilsa `manage.py check` yiqiladi).
    muqova = models.FileField(
        upload_to='materiallar/muqova/', blank=True, null=True, verbose_name="Muqova rasmi",
        help_text="Ixtiyoriy (JPG yoki PNG). Ro'yxatda kitob muqovasi bo'lib ko'rinadi. "
                  "Bo'sh qoldirilsa, o'rniga fayl turi nishoni chiqadi.",
    )
    link = models.URLField(
        blank=True, verbose_name="Havola",
        help_text="Ixtiyoriy: tashqi manba (masalan, jurnal sayti) havolasi.",
    )
    manba = models.CharField(
        max_length=250, blank=True, verbose_name="Manba",
        help_text="Masalan: jurnal nomi, nashr yili, sinf yoki mavzu.",
    )
    order = models.IntegerField(
        default=0, verbose_name="Tartib",
        help_text="Kichik raqam yuqorida turadi.",
    )
    is_published = models.BooleanField(default=True, verbose_name="Chop etilgan")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Qo'shilgan sana")

    class Meta:
        verbose_name = "Material"
        verbose_name_plural = "Materiallar"
        ordering = ['order', '-created_at']

    def __str__(self):
        return f"{self.get_section_display()} — {self.title}"

    @property
    def file_ext(self):
        """Fayl kengaytmasi — ro'yxatda nishon sifatida ko'rsatiladi."""
        if not self.file:
            return ''
        return self.file.name.rsplit('.', 1)[-1].upper() if '.' in self.file.name else ''

    @property
    def is_pdf(self):
        """PDF bo'lsa sahifada ichki ko'ruvchi ochish mumkin."""
        return self.file_ext == 'PDF'


class Profile(models.Model):
    """Foydalanuvchi roli — o'quvchi yoki talaba.

    O'quvchi faqat 1–5 mashqlarni ko'radi; talaba 6–10 ni ham ko'radi.
    """
    ROLE_OQUVCHI = 'oquvchi'
    ROLE_TALABA = 'talaba'
    ROLE_CHOICES = [
        (ROLE_OQUVCHI, "O'quvchi"),
        (ROLE_TALABA, "O'qituvchi"),
    ]

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile',
        verbose_name="Foydalanuvchi",
    )
    role = models.CharField(
        max_length=10, choices=ROLE_CHOICES, default=ROLE_OQUVCHI,
        verbose_name="Rol",
    )

    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profillar"

    def __str__(self):
        return f"{self.user.username} — {self.get_role_display()}"

    @property
    def is_talaba(self):
        return self.role == self.ROLE_TALABA
