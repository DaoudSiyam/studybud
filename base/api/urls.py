# we need a urls file for apis
from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('rooms', views.getRooms),
    path('rooms/<str:pk>/', views.getRoom),
]
# now we need to connect this urls file to the main project
# so we go to the main file where we can find the admin path
# and add the path of this file here