from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model, authenticate, login, logout
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.forms import model_to_dict
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view


User = get_user_model()


@api_view(["GET"])
def home(request):
    context = [
        "AVAILABLE ENDPOINDS::",
    
        "https://inpark-api-331214075983.herokuapp.com/signup/",
        "https://inpark-api-331214075983.herokuapp.com/login/",
        "https://inpark-api-331214075983.herokuapp.com/logout/",
        "https://inpark-api-331214075983.herokuapp.com/create-vehicle/",
        "https://inpark-api-331214075983.herokuapp.com/process-parking/",
        "https://inpark-api-331214075983.herokuapp.com/leave-parking/",
        "https://inpark-api-331214075983.herokuapp.com/extend-parking/",
        "https://inpark-api-331214075983.herokuapp.com/user-information/",
        "https://inpark-api-331214075983.herokuapp.com/parking-history/",

        {"Information available for public disclosure 01": "API endpoints to only be consumed with the inparker android app and inpaker web."},
        {"Information available for public disclosure 02": "email <<macddeemanana@gmail.com>> for the API Docs"},

    ]

    return Response(context)

class Signup(APIView):
    def post(self, request):
        data = request.data
        user = User.objects.create_user(
            username=data.get('username'),
            password=data.get('password'),
            email=data.get('email'),
            first_name=data.get('first_name', "null"),
            last_name=data.get('last_name', "null"),
            nationalID=data.get('nationalID', "null"),
            phone_number=data.get('phone_number', "null")
        )
        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
    
class Login(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return Response({"message": "User logged in successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid username or password"}, status=status.HTTP_400_BAD_REQUEST)
        

class VehicleCreate(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        car_reg = request.data.get('car_reg')
        color = request.data.get('color')
        type = request.data.get('type')

        if request.user.is_authenticated:
            vehicle = Vehicle(car_reg=car_reg, color=color, type=type, owner=request.user)
            vehicle.save()
            vehicle_dict = model_to_dict(vehicle)
            return Response(vehicle_dict, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)


class ProcessParking(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        address = request.data.get('address')
        duriation = request.data.get('duriation')
        parking_number = request.data.get('parking_number')
        price = request.data.get('price'),
        account = Parking.objects.get()

        if request.user.is_authenticated:
            processed_parking = Parking(
                address=address,
                duriation=duriation,
                parking_status="Ongoing",
                parking_number=parking_number,
                price=price,
                owner=request.user
            )

            processed_parking.save()
            processed_parking_dict = model_to_dict(processed_parking)
            processed_parking_dict["entryTime"]= processed_parking.entryTime
            processed_parking_dict["exitTime"]=processed_parking.exitTime

            return Response([
                {"message": "Parking slot successifuly booked!"},
                {"response": processed_parking_dict}], 
                status=status.HTTP_201_CREATED
            )
        else:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)


class LeaveParking(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            current_parking = Parking.objects.get(
                id=request.data.get("id")
            )
        except:
            return Response({"message": "You are currently not parked"}, status=status.HTTP_400_BAD_REQUEST)

        if current_parking.parking_status != "Terminated":
            if request.user.is_authenticated:
                current_parking.exitTime= timezone.datetime.now()
                current_parking.parking_status= "Terminated"
                current_parking.save()
                return Response({"message": "Parking slot successfuly freed!"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"message": "Unable to leave parking. Your parking session has already been terminated"}, status=status.HTTP_400_BAD_REQUEST)


class ExtendParking(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        current_parking_dict = []
        current_parking = None

        try:
            current_parking = Parking.objects.get(
                id=request.data.get("id")
            )
        except ObjectDoesNotExist:
            return Response({"message": "You are currently not parked. Unable to extend parking."}, status=status.HTTP_400_BAD_REQUEST)


        if current_parking.parking_status != "Terminated":
            if request.user.is_authenticated:
                extended_parking = Parking(
                    address=current_parking.address,
                    duriation=request.data.get("duriation"),
                    parking_status="Extended",
                    parking_number=current_parking.parking_number,
                    price=request.data.get("price"),
                    owner=request.user
                )
                extended_parking.save()

                extended_parking.refresh_from_db()
                current_parking_dict = model_to_dict(extended_parking)
                current_parking_dict["entryTime"]= extended_parking.entryTime
                current_parking_dict["exitTime"]=extended_parking.exitTime


                return Response({"response_data": current_parking_dict, "message": "Parking period successfuly extended!"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"message": "Cannot extend a terminated parking session!"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class LogoutView(APIView):
    def get(self, request):
        logout(request)
        return Response({"message": "User logged out successfully"}, status=status.HTTP_200_OK)
    
class UserDataView(APIView):
    def get(self, request):
        user_info = get_object_or_404(
        Motorist,
        pk=request.user.id
        )
        user_info_serializer = MotoristSerializer(user_info,)
        responseData = [user_info_serializer.data]  
        return Response(responseData, status=status.HTTP_200_OK)


class ParkHistoryView(APIView):
    def get(self, request):
        history = Parking.objects.filter(owner_id=request.user.id)

        history_api = ParkingSerializer(history, many=True)

        if history_api.data:
            responseData = [history_api.data]
            return Response(responseData, status=status.HTTP_200_OK)
        else:
            return Response("No parking history data found.")