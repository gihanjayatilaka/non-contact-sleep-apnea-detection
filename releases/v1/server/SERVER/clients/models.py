from django.db import models
from django.conf import settings
from django.core.validators import int_list_validator
# Create your models here.


class Client_buffer_recv(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    device_id = models.CharField(max_length=255)

    data = models.CharField(validators= [int_list_validator(allow_negative=True)], max_length=10000)
    timestamp = models.DateTimeField()


    def __str__(self):
        return str(self.user.username)


class Patient(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Patient_id = models.CharField(max_length=500, primary_key=True)


    def __str__(self):
        return str(self.Patient_id)


class Devices(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    device_id = models.CharField(max_length=255, primary_key=True)
    last_connected = models.DateTimeField()

