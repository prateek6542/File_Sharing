from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from django.contrib.auth import authenticate, login
from rest_framework.permissions import IsAuthenticated
from .models import UploadedFile, ClientUser, OpsUser
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from .serializers import (
    ClientUserSerializer,
    UploadedFileSerializer,
    UserLoginSerializer,
    UserSignUpSerializer,
    ClientUserVerifySerializer,
    OpsUserSerializer 
)

class ClientUserSignUp(APIView):
    def post(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            email = serializer.validated_data['email']

            user = User.objects.create_user(username=username, password=password, email=email)
            encrypted_url = f"securelink-{user.id}"  # Generate encrypted URL here

            client_user = ClientUser.objects.create(user=user, encrypted_url=encrypted_url)
            return Response({'encrypted_url': encrypted_url}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClientUserEmailVerify(APIView):
    def post(self, request):
        serializer = ClientUserVerifySerializer(data=request.data)
        if serializer.is_valid():
            encrypted_url = serializer.validated_data['encrypted_url']
            try:
                client_user = ClientUser.objects.get(encrypted_url=encrypted_url)
                client_user.is_verified = True
                client_user.save()
                return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)
            except ClientUser.DoesNotExist:
                return Response({'message': 'Invalid encrypted URL'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClientUserLogin(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username, password=password)

            if user and user.is_active and not user.is_staff:
                login(request, user)
                return Response({'message': 'Client user login successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid credentials or user not authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
class ClientUserDownloadFile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, file_id):
        try:
            uploaded_file = UploadedFile.objects.get(id=file_id)
            download_link = f"https://yourdomain.com/download-file/{uploaded_file.id}"
            return Response({'download-link': download_link, 'message': 'success'}, status=status.HTTP_200_OK)
        except UploadedFile.DoesNotExist:
            return Response({'message': 'File not found'}, status=status.HTTP_404_NOT_FOUND)

class ClientUserListFiles(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        files = UploadedFile.objects.filter(user=user)
        serializer = UploadedFileSerializer(files, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class OpsUserRegistration(APIView):
    def post(self, request):

        serializer = OpsUserSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = User.objects.create_user(username=username, password=password)

            ops_user = OpsUser(user=user)
            ops_user.save()

            return Response({'message': 'Ops User registered successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@csrf_exempt
def OpsUserLogin(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

       
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return Response({'message': 'Ops User login successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'User account is not active'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)



@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
class OpsUserUploadFile(APIView):
    def post(self, request):
        uploaded_file = request.FILES.get('file')

        if not uploaded_file:
            return Response({'message': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        allowed_extensions = ['pptx', 'docx', 'xlsx']
        file_extension = uploaded_file.name.split('.')[-1]

        if file_extension not in allowed_extensions:
            return Response({'message': 'Invalid file type'}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        uploaded_file_instance = UploadedFile.objects.create(user=user, file=uploaded_file)
        return Response({'message': 'File uploaded successfully', 'file_id': uploaded_file_instance.id}, status=status.HTTP_201_CREATED)
