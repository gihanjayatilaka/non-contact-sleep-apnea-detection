import json
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import generics, mixins
from django.http import JsonResponse
from django.core import serializers
from clients.models import  Client_buffer_recv, Devices
from.serializers import  Client_buffer_recv_serializer, Device_serializer, Device_Create_serializer
from.permissions import IsOwnerOrReadOnly

from django.shortcuts import redirect

class Client_buffer_data_recv_UView(generics.UpdateAPIView):

    lookup_field = 'timestamp'
    serializer_class = Client_buffer_recv_serializer



    def get_queryset(self):
        return Client_buffer_recv.objects.all()

class Client_buffer_data_recv_RView(generics.RetrieveAPIView):

    lookup_field = 'timestamp'
    serializer_class = Client_buffer_recv_serializer



    def get_queryset(self):
        return Client_buffer_recv.objects.all()


class Client_buffer_data_recv_APIView(generics.CreateAPIView):

    lookup_field = 'timestamp'
    serializer_class = Client_buffer_recv_serializer



    def get_queryset(self):
        return Client_buffer_recv.objects.all()

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)


class Client_buffer_data_recv_ListView(generics.ListAPIView):

    lookup_field = 'timestamp'
    serializer_class = Client_buffer_recv_serializer


    def get_queryset(self):
        return Client_buffer_recv.objects.all()

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)



def Last_n_Data(request, n, d):

    number = int(n)
    d_id = d

    obj = Client_buffer_recv.objects.filter(device_id = d_id ).filter(user=request.user).order_by('-timestamp')[:number]

    serializer_d = serializers.serialize('json', obj)
    return  JsonResponse(serializer_d, safe=False)





class Device_ListView(generics.ListAPIView):

    lookup_field = "device_id"
    serializer_class =  Device_serializer


    def get_queryset(self):
        return Devices.objects.all()

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

class Device_RetreieveView(generics.RetrieveAPIView):

    lookup_field = "device_id"
    serializer_class =  Device_serializer


    def get_queryset(self):
        return Devices.objects.all()




class Device_UpdateView(generics.UpdateAPIView):

    lookup_field = "device_id"
    serializer_class =  Device_serializer


    def get_queryset(self):
        return Devices.objects.all()


class Device_APIView(generics.CreateAPIView):

    lookup_field = "device_id"
    serializer_class =  Device_Create_serializer

    def get_queryset(self):
        return Devices.objects.all()

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)


class Device_Destroy_View(generics.DestroyAPIView):

    lookup_field = "device_id"
    serializer_class =  Device_serializer

    permission_classes = [IsOwnerOrReadOnly]
    def get_queryset(self):
        return Devices.objects.all()



def Destroy(request, device_id):
    d = Devices.objects.filter(device_id = device_id)
    d.delete()

    return redirect("/client/device_list/")


