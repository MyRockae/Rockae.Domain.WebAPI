from django.urls import path
from .views import login_view,register_view,MyTokenObtainPairView,MyTokenRefreshView,send_verification_email_view,reset_password_view,send_password_reset_email_view,verify_account_view

urlpatterns = [
    path('auth/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', register_view, name='register'),
    path('auth/login/', login_view, name='login'),
    path("send-verification-email/", send_verification_email_view, name="send-verification-email"),
    path("verify/<str:verification_token>/", verify_account_view, name="verify-account"),
    path("send-password-reset-email/", send_password_reset_email_view, name="send-password-reset-email"),
    path("reset-password/<str:reset_token>/", reset_password_view, name="reset-password"),
]

