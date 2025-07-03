
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView


urlpatterns = [
    path('', include('booking.urls')),
    path('admin/', admin.site.urls),
    path('booking/', include('booking.urls')),
    path('accounts/', include('booking.urls')),
    path('', RedirectView.as_view(url='/booking/login/', permanent=True)),
]
