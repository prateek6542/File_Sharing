from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import UploadedFile, ClientUser, OpsUser

class FileSharingTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.ops_user = User.objects.create_user(username='opsuser', password='opspassword')
        self.client_user = User.objects.create_user(username='clientuser', password='clientpassword')

    def test_client_user_signup(self):
        url = reverse('client-user-signup')
        data = {'username': 'newclientuser', 'password': 'newclientpassword', 'email': 'test@example.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_client_user_email_verify(self):
        client_user = ClientUser.objects.create(user=self.user, encrypted_url='some_encrypted_url')
        url = reverse('client-user-email-verify')
        data = {'encrypted_url': 'some_encrypted_url'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_client_user_login(self):
        url = reverse('client-user-login')
        data = {'username': 'clientuser', 'password': 'clientpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_client_user_download_file(self):
        uploaded_file = UploadedFile.objects.create(user=self.client_user, file=None)
        url = reverse('client-user-download-file', kwargs={'file_id': uploaded_file.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_client_user_list_files(self):
        url = reverse('client-user-list-files')
        self.client.login(username='clientuser', password='clientpassword')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ops_user_registration(self):
        url = reverse('ops-user-registration')
        data = {'username': 'newopsuser', 'password': 'newopspassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_ops_user_login(self):
        url = reverse('ops-user-login')
        data = {'username': 'opsuser', 'password': 'opspassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ops_user_upload_file(self):
        url = reverse('ops-user-upload-file')
        data = {'file': 'some_file_content'}
        self.client.login(username='opsuser', password='opspassword')
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
