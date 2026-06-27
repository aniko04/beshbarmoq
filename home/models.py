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


class Profile(models.Model):
    """Foydalanuvchi roli — o'quvchi yoki talaba.

    O'quvchi faqat 1–5 mashqlarni ko'radi; talaba 6–10 ni ham ko'radi.
    """
    ROLE_OQUVCHI = 'oquvchi'
    ROLE_TALABA = 'talaba'
    ROLE_CHOICES = [
        (ROLE_OQUVCHI, "O'quvchi"),
        (ROLE_TALABA, 'Talaba'),
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
