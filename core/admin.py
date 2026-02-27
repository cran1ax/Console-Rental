from django.contrib import admin
from .models import Console, Rental


@admin.register(Console)
class ConsoleAdmin(admin.ModelAdmin):
    list_display = ("name", "daily_price", "stock_quantity")


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ("user", "console", "start_date", "end_date", "total_price", "status")
