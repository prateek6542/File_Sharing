from django.urls import path
from .views import *

urlpatterns = [
    path('client-user/sign-up/', ClientUserSignUp.as_view()),
    path('client-user/email-verify/', ClientUserEmailVerify.as_view()),
    path('client-user/login/', ClientUserLogin.as_view()),
    path('client-user/download-file/<int:file_id>/', ClientUserDownloadFile.as_view()),
    path('client-user/list-files/', ClientUserListFiles.as_view()),
    path('ops-user/register/', OpsUserRegistration.as_view(), name='ops-user-register'),
    path('ops-user/login/', OpsUserLogin, name='ops-user-login'),
    path('ops-user/upload-file/', OpsUserUploadFile.as_view()),
]
