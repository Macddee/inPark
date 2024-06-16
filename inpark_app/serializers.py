from rest_framework import serializers
from .models import Vehicle, Parking, ParkingSpace, Motorist

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['car_reg', 'color', 'type', 'owner_id']
    

class ParkingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parking
        fields = "__all__"

class ParkingSpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingSpace
        fields = "__all__"


class MotoristSerializer(serializers.ModelSerializer):
    class Meta:
        model = Motorist
        fields = ["id", "username", "first_name", "last_name", "email", "nationalID", "phone_number"]
