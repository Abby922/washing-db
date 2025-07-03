from django.urls import path
from .views import book_appointment, success
from . import views
from .views import register
from django.contrib.auth import views as auth_views
from .views import delete_appointment

urlpatterns = [
    path('', views.book_appointment, name='book_appointment'),
    path('success/', views.success, name='success'),
    path('get_reserved_slots/', views.get_reserved_slots, name='get_reserved_slots'),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='booking/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/booking/login/'), name='logout'),
    path('delete_appointment/<int:appointment_id>/', delete_appointment, name='delete_appointment'),
]
