# we need our own views for apis
# usually when dealing with apis
# we respond with JSON data to other applications, frameworks, etc...
# so we want to usually respond with some JSON data
# when someone goes to our url

#from django.http import JsonResponse
# JSON is a form of data that stands for
# javascript object notation
# and it's a format of how we can provide data
# with the django rest framework we can
# either use class based views for function based views
# but we will be using function based views for now

from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSerializer

# a view that shows us all the routes in our api
# we pass inside a list of the http methods 
# that are allowed to access this view
@api_view(['GET']) # this is used for function based views
# class based views has a different way
def getRoutes(request):
    # these urls(routes will be 2 GET methods here)
    routes = [
        # we can also write PUT,POST or DELETE methods to our api
        'GET /api',
        'GET /api/rooms', # gets all the rooms to show for users
        'GET /api/rooms/:id', # gets one room using room id if requested
    ]
    return Response(routes)

    # safe means that we can use more than 
    # python dictionaries inside of this response
    # the json response converts the list into json data

@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many = True)
    # pass in the object/s that we want to serialize
    # many means that there will be multiple objects to be serliazed
    # so it means are there going to be many or only 
    # one object that will be serialized
    
    # in this case we are serializing a queryset
    # so many will be set to true
    
    # serializer is an object
    # but we don't want to return the object itsself
    # but the data inside it
    # it will give us rooms in a serialized format
    return Response(serializer.data)


@api_view(['GET'])
def getRoom( request, pk):
    room = Room.objects.get( id = pk)
    serializer = RoomSerializer( room, many = False)
    # returns a single object
    return Response(serializer.data)

# for further notice, we can nest serializers


'''
# to install the djangorest framework
# we need to type in the terminal
# python -m pip install djangorestframework
# dont forget your venv
# and after installing it
# dont forget to code it inside install apps in the settings file

# and also in order to let the different resources coommunicate
# with eachother, we need to install something the djnago-cors-headers
'''

