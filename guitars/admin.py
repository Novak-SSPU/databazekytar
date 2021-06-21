from django.contrib import admin

# Import všech modelů, které obsahuje models.py
from django.db.models import Count
from django.utils.html import format_html

from .models import *

# Registrace modelů v administraci aplikace
@admin.register(Type)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "guitar_count")

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _guitar_count=Count("guitar", distinct=True),
        )
        return queryset

    def guitar_count(self, obj):
        return obj._guitar_count

    guitar_count.admin_order_field = "_guitar_count"
    guitar_count.short_description = "Počet kytar"


@admin.register(Guitar)
class GuitarAdmin(admin.ModelAdmin):
    list_display = ("name", "rate_percent")

    def rate_percent(self, obj):
        return format_html("<b>{} %</b>", int(obj.rate * 10))

    rate_percent.short_description = "Hodnocení kytary"





@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("author", "guitar", "rate", "edit_date")