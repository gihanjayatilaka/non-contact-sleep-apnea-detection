from .views import Client_buffer_data_recv_UView, Client_buffer_data_recv_APIView, Client_buffer_data_recv_RView
from .views import Client_buffer_data_recv_ListView, Last_n_Data
from.views import Device_ListView, Device_RetreieveView, Device_UpdateView, Device_APIView, Device_Destroy_View
from django.contrib import admin
from django.urls import path, include
from .views import Destroy
urlpatterns = [
    path('client_buffer_data_recv/', Client_buffer_data_recv_APIView.as_view(), name = "client-buffer-data-recv-api"),
    path('client_buffer_data_recv/list/', Client_buffer_data_recv_ListView.as_view(), name = "client-buffer-data-recv-list"),
    path('client_buffer_data_recv/update/<timestamp>/', Client_buffer_data_recv_UView.as_view(), name="client-buffer-data-recv-rud"),
    path('client_buffer_data_recv/retrieve/<timestamp>/', Client_buffer_data_recv_RView.as_view(), name="client-buffer-data-recv-rud"),
    path('client_buffer_data_recv/retrieve/<n>/<d>/', Last_n_Data),

    path('device/', Device_APIView.as_view(), name = 'Device_Create_View'),
    path('device/retrieve/<device_id>/', Device_RetreieveView.as_view(), name= "Device_Retrieve_View" ),
    path('device/list/', Device_ListView.as_view(), name = "Device_List_View"),
    path('device/update/<device_id>/', Device_UpdateView.as_view(), name = "Device_Update_View"),
    path('device/destroy/<device_id>', Destroy, name = "Device_destroy_view")


]
