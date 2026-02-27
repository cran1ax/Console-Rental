"""Corner Console — project URLs."""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # All API endpoints live under /api/
    path('api/', include('core.urls')),

    # DRF browsable-API login button (handy during the demo)
    path('api-auth/', include('rest_framework.urls')),
]
