from django.test import TestCase
from django.contrib.auth.models import User
from.models import Client_buffer_recv, Devices
from django.utils import timezone
# Create your tests here.



class ClientTest(TestCase):

    def create_client(self, username = "test", password = "test", email = "test@gmail.com"):

        return User.objects.create_user(username=username, password=password, email=email)

    def test_client_creation(self):
        c = self.create_client()
        self.assertTrue(isinstance(c, User))

    def test_URL(self):
        c = self.create_client()
        self.assertTrue(isinstance(c, User))

    def test_VIEW(self):
        c = self.create_client()
        self.assertTrue(isinstance(c, User))

    def test_HTML(self):
        c = self.create_client()
        self.assertTrue(isinstance(c, User))

    def test_DEVICE(self):
        c = self.create_client()
        self.assertTrue(isinstance(c, User))

