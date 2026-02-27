from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Console, Rental
from .serializers import ConsoleSerializer, RentalSerializer


class ConsoleViewSet(viewsets.ReadOnlyModelViewSet):
    """Public, read-only list of consoles available for rent."""
    queryset = Console.objects.all()
    serializer_class = ConsoleSerializer
    permission_classes = [permissions.AllowAny]


class RentalViewSet(viewsets.ModelViewSet):
    """
    Authenticated users can create rentals and view **only their own**.
    """
    serializer_class = RentalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Each user sees only their own rentals
        return Rental.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        console = serializer.validated_data["console"]
        start = serializer.validated_data["start_date"]
        end = serializer.validated_data["end_date"]
        days = (end - start).days or 1  # at least 1 day
        total = console.daily_price * days
        serializer.save(user=self.request.user, total_price=total)

    # ---- Mock Payment endpoint ------------------------------------------
    @action(detail=True, methods=["post"], url_path="mock-pay")
    def mock_pay(self, request, pk=None):
        """Fake payment: just flips the status to 'Paid'."""
        rental = self.get_object()

        if rental.status == "Paid":
            return Response(
                {"detail": "This rental is already paid."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        rental.status = "Paid"
        rental.save()
        return Response(
            {"detail": "Payment successful (mock).", "status": rental.status}
        )
