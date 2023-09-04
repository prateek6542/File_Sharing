from django.db import models
from django.contrib.auth.models import User

class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    timestamp = models.DateTimeField(auto_now_add=True)

class ClientUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    encrypted_url = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)

class OpsUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)