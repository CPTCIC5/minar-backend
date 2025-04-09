from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')

urlpatterns = [
    # Authentication endpoints
    path('login/send-otp/', views.SendOTPView.as_view(), name='send-otp'),
    path('login/verify-otp/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    
    # User information
    path('', include(router.urls)),
]
