from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from .models import Result, Profile, Material


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'mashq', 'score_display', 'percentage_display', 'status_display', 'created_at']
    list_filter = ['mashq', 'is_passed', 'created_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
    readonly_fields = ['user', 'mashq', 'score', 'total', 'is_passed', 'created_at']
    list_per_page = 25

    def score_display(self, obj):
        return f"{obj.score} / {obj.total}"
    score_display.short_description = "Natija"

    def percentage_display(self, obj):
        p = obj.percentage
        if p == 100:
            color = '#22c55e'
        elif p >= 50:
            color = '#f59e0b'
        else:
            color = '#ef4444'
        return mark_safe(f'<span style="color:{color};font-weight:bold;">{p}%</span>')
    percentage_display.short_description = "Foiz"

    def status_display(self, obj):
        if obj.is_passed:
            return mark_safe('<span style="color:#22c55e;font-weight:bold;">✅ O\'tdi</span>')
        return mark_safe('<span style="color:#ef4444;font-weight:bold;">❌ O\'tmadi</span>')
    status_display.short_description = "Holat"


# ===== Foydalanuvchi rolini boshqarish =====
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Rol"


class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline]
    list_display = ['username', 'first_name', 'last_name', 'role_display', 'is_staff']

    def role_display(self, obj):
        try:
            return obj.profile.get_role_display()
        except Profile.DoesNotExist:
            return '—'
    role_display.short_description = "Rol"


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']
    list_filter = ['role']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']


# ===== Bo'lim materiallari =====
@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['title', 'section', 'fayl_display', 'order', 'is_published', 'created_at']
    list_filter = ['section', 'is_published']
    search_fields = ['title', 'summary', 'manba']
    list_editable = ['order', 'is_published']
    list_per_page = 30
    fieldsets = (
        ("Asosiy", {
            'fields': ('section', 'title', 'summary'),
        }),
        ("Mazmun", {
            'fields': ('body', 'file', 'link', 'manba'),
            'description': "Matn, fayl yoki havola — kamida bittasini to'ldiring.",
        }),
        ("Ko'rsatish", {
            'fields': ('order', 'is_published'),
        }),
    )

    def fayl_display(self, obj):
        if obj.file:
            return mark_safe(f'<b>{obj.file_ext}</b>')
        if obj.link:
            return "Havola"
        return '—'
    fayl_display.short_description = "Fayl"
