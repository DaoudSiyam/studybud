# Response class in the django rest framework
# cannot return back python objects 
# so because what we get is a queryset
# it needs to be serialize the data that we get

# lists can be automatically converted
# but objects cannot
# so python objects need to be serialized
# before being passed in the Response class

# so serializers are going to be classes
# that take a certain model that we
# want to serialize and then turn
# it into JSON data 
# so in short, take the python object
# and turns it in javascript object
# so it can be easier to be dealt with

# the serializer works alot like a model
# so keep that in mind
from rest_framework.serializers import ModelSerializer
from base.models import Room

class RoomSerializer(ModelSerializer):
    class Meta:
        # we need to specify 2 fields at a minimum
        model = Room
        fields = '__all__'
        # take this model and serialize it
        # return back all it's fields
        # and turn them into a JSON object