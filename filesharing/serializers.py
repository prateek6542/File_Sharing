from rest_framework import serializers
from .models import UploadedFile, ClientUser, OpsUser

class ClientUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientUser
        fields = '__all__'

class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = '__all__'

class OpsUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = OpsUser
        fields = ('username', 'password',)

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class UserSignUpSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()

class ClientUserVerifySerializer(serializers.Serializer):
    encrypted_url = serializers.CharField()
