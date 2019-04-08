from django.urls import path
from . import views

app_name = 'web_cam'
urlpatterns = [
    path('cam_data/', views.Cam_data, name="cam_data"),
    path('cam_home/', views.CamHome, name="cam_home"),
]
