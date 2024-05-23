from django.urls import path
from . import views

app_name = "In Park"

urlpatterns = [
    # path("home", views.home),
    path('signup/', views.Signup.as_view(), name='create_motorist'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='login'),
    path('create-vehicle/', views.VehicleCreate.as_view(), name='login'),
    path('process-parking/', views.ProcessParking.as_view(), name='login'),
    path('leave-parking/', views.LeaveParking.as_view(), name='login'),
    path('extend-parking/', views.ExtendParking.as_view(), name='login'),

]


# a = {
# "username": "user1",
# "password": "user1234",
# "email": "user@gmail.com",
# "first_name": "mac",
# "last_name": "dee",
# "nationalID": "42-0772004H42",
# "phone_number": "0783773993"
# }

# b = {
    # "address": "abc Street",
    # "duriation": 2,
    # "parking_status": "True",
    # "parking_number": "#P0123",
    # "price": 1

# }