#this urls file will be for a specific app
from django.urls import path
#because the views will be in their own files
#we will be doing the following 
from . import views

urlpatterns = [
    path( 'login/', views.loginPage, name = "login"),
    path( 'logout/', views.logoutUser, name = "logout"),
    path( 'register/', views.registerPage, name = "register"),

    #the path function can take 3 paramerters
    path('', views.home, name="home"),
    path('room/<str:pk>/', views.room, name="room"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    
    path( 'create-room/', views.createRoom, name = "create-room"),

    # the updateRoom class needs an id, so we need to create it
    path( 'update-room/<str:pk>', views.updateRoom, name = "update-room"),    
    path( 'delete-room/<str:pk>', views.deleteRoom, name = "delete-room"),
    path( 'update-message/<str:pk>', views.updateMessage, name = "update-message"),
    path( 'delete-message/<str:pk>', views.deleteMessage, name = "delete-message"),
    
    path( 'update-user/', views.updateUser, name = "update-user"),

    path( 'topics/', views.topicsPage, name = "topics"),
    path( 'activity/', views.activityPage, name = "activity"),
]   