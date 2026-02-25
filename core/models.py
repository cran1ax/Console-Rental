from django.db import models
from django.contrib.auth.models import User


class Console(models.Model):
    """A PlayStation console available for rent."""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    daily_price = models.DecimalField(max_digits=8, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=1)
    image_url = models.URLField(blank=True)  # simple URL — no media uploads needed

    def __str__(self):
        return self.name


class Rental(models.Model):
    """Tracks a user renting a console for a date range."""

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Paid", "Paid"),
        ("Returned", "Returned"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rentals")
    console = models.ForeignKey(Console, on_delete=models.CASCADE, related_name="rentals")
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Pending")

    def __str__(self):
        return f"{self.user.username} — {self.console.name} ({self.status})"
