from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"consoles", views.ConsoleViewSet, basename="console")
router.register(r"rentals", views.RentalViewSet, basename="rental")

urlpatterns = [
    path("", include(router.urls)),
]
