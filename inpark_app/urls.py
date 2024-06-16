from django.urls import path
from . import views

app_name = "In Park"

urlpatterns = [
    path("", views.home),
    path('signup/', views.Signup.as_view(), name='create_motorist'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='login'),
    path('create-vehicle/', views.VehicleCreate.as_view(), name='login'),
    path('process-parking/', views.ProcessParking.as_view(), name='login'),
    path('leave-parking/', views.LeaveParking.as_view(), name='login'),
    path('extend-parking/', views.ExtendParking.as_view(), name='login'),
    path('user-information/', views.UserDataView.as_view(), name='login'),
    path('parking-history/', views.ParkHistoryView.as_view(), name='login'),

]
