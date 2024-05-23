from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


# Create your models here.
class Motorist(AbstractUser):
    nationalID = models.CharField(max_length=13)
    phone_number = models.CharField(max_length=15)


class Vehicle(models.Model):
    owner = models.ForeignKey(
        Motorist,
        on_delete=models.CASCADE
    )
    car_reg = models.CharField(max_length=8, null=False)
    color = models.CharField(max_length=50, )
    type = models.CharField(max_length=50,)


class ParkingSpace(models.Model):
    type = models.CharField(max_length=10)
    address = models.TextField(max_length = 255)
    price = models.DecimalField(max_digits=1000000, decimal_places=2)
    occupied = models.BooleanField()
    timeOccupied = models.DateTimeField(auto_now_add=True)


class Parking(models.Model):
    owner = models.ForeignKey(
        Motorist,
        on_delete=models.CASCADE
    )
    address = models.TextField(max_length = 255)
    duriation = models.CharField(max_length = 20)
    parking_status = models.CharField(max_length = 25)
    parking_number = models.IntegerField(null=False)
    price = models.DecimalField(max_digits=1000000, decimal_places=2)
    entryTime = models.DateTimeField(auto_now_add=True)
    exitTime = models.DateTimeField(auto_now=True)

