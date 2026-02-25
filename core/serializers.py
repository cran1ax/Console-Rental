from rest_framework import serializers
from .models import Console, Rental


class ConsoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Console
        fields = ["id", "name", "description", "daily_price", "stock_quantity", "image_url"]


class RentalSerializer(serializers.ModelSerializer):
    # Read-only field so the frontend can show the console name directly
    console_name = serializers.CharField(source="console.name", read_only=True)

    class Meta:
        model = Rental
        fields = [
            "id",
            "user",
            "console",
            "console_name",
            "start_date",
            "end_date",
            "total_price",
            "status",
        ]
        read_only_fields = ["user", "total_price", "status"]
