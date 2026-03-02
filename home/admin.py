from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Result


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
