from rest_framework import serializers
from clients.models import Client_buffer_recv, Devices



class Client_buffer_recv_serializer(serializers.ModelSerializer):

    class Meta:
        model = Client_buffer_recv
        fields = [
            'pk',
            'user',
            'data',
            'timestamp',
            'device_id'
        ]

        read_only_fields = [
            "user",

        ]



class  Device_serializer(serializers.ModelSerializer):

    class Meta:

        model = Devices
        fields = [

            'user',
            'device_id',
            'last_connected'
        ]

        read_only_fields = [
            "user",
            'device_id'
        ]


class  Device_Create_serializer(serializers.ModelSerializer):

    class Meta:

        model = Devices
        fields = [

            'user',
            'device_id',
            'last_connected'
        ]

        read_only_fields = [
            'user '
        ]


        def validate_device_id(self, value):

            qs = Devices.objects.filter(device_id__iexac = value)
            if qs.exists():
                raise serializers.ValidationError("The device id is already taken")

            return value
