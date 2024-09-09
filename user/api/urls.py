from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from user.api import views

urlpatterns = [
    path('register/', views.registration, name='register'),
    path('login/', obtain_auth_token, name='login'),
    path('logout/', views.logout, name='logout'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
