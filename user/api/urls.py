from django.urls import path
from user.api import views

app_name = 'user'


urlpatterns = [
    path('login/' ,views.UserLoginAPIView.as_view() ,name='login'), #verified 
    path("register/" , views.RegisterApiView.as_view() , name="register"), #verified
    path("forgot/", views.ForgotPasswordView.as_view() , name="forgot"), #verified
    path("otp_verify/", views.OtpVerifyView.as_view() , name="otp_verify"), #verified
    path("reset_password/",views.ResetPasswordView.as_view() , name="reset-password"), #verified
    path("force_verify/<int:pk>/" , views.ForcedVerifyView.as_view() , name="force-verify"), #verify
    path("re_verify/<int:pk>/" , views.ReSendVerificationView.as_view() , name="reverify-user"), #verify
    path("verify_account/", views.verify_account , name="verify-account"), #verified
    path('password/change/', views.PasswordChangeView.as_view(), name='password_change'), #verified
    path('download-apk/', views.DownloadAPKView.as_view(), name='download_apk'),
]
