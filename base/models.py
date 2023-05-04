from django.db import models
from django.contrib.auth.models import AbstractUser

# make sure you delete the sqllite database file
# when you are trying to add new stuff
# to you database

# we will be integrating our own custom user model now
# which would require to stop the server from running
# and then deleting the sqllite database so we can startover
# and also delete all the migrations that we made before



class User( AbstractUser ):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField( unique=True ,null=True)
    bio = models.TextField(null=True)

    # ImageField relies on a third party package
    # called pillow that need to be installed
    # run python -m pip install pillow
    avatar =models.ImageField(null=True, default="avatar.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  

'''
    each room should have some type of category
'''

class Topic( models.Model):
    name = models.CharField( max_length = 200)

    def __str__(self):
        return self.name


class Room( models.Model ):    
    host = models.ForeignKey( User, on_delete = models.SET_NULL ,  null = True)
    # this means that a user must host a room
    # and cannot be any other way

    topic = models.ForeignKey( Topic, on_delete = models.SET_NULL, null = True )

    name = models.CharField( max_length = 200 )    
    description = models.TextField( null = True, blank = True )    
    # null is for the db and blank is for the forms
    
    # this one requires a many to many field
    # and there is a special way to do that
    participants = models.ManyToManyField(User , related_name = 'participants', blank = True )
    # we need to use a related name field
    # because we can't use the same user name twice
    # and reference it twice in the same model
    #stores all users currenlty active in a room
    
    updated = models.DateTimeField( auto_now = True )
    created = models.DateTimeField( auto_now_add = True )

    # now we will create a class that makes sure
    # that the new rooms get shown first on the page
    class Meta:
        ordering = ['-updated', '-created']
        # what this does is it orders room by latest creation date
        # the dash means order in descending order

    def __str__ (self):
        return self.name
        # has to be a string value
        # so if you do a date or try to concatenate values or numbers
        # makes sure you wrap the value around with str()

# we need then to create a superuser so we can access admin panel
# through the createsuperuser command in the terminal

# each room should have a message
class Message( models.Model ):
    # specify the user that is sending the message
    # django provides us with a default user method
    # the default user model is a class
    # that has a username, first_name, last_name, email
    # different permissions, such as staff, active user, superuser
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    # then we need to specify the room
    # thus the first relationship is built this way
    room = models.ForeignKey( Room, on_delete = models.CASCADE)
    # inside we need to define the parent class
    # so we can define the forgeinkey 
    # cascade means that when a room is deleated
    # delete all the messages

    body = models.TextField()
    # body is the actual message

    updated = models.DateTimeField( auto_now = True)
    created = models.DateTimeField( auto_now_add = True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]
        # the list means trim it down to 50 characters
        # so that not to make the message too long
        # and clutter the admin panel

'''
dave
dave@email.com
1!2@3#4$5%6^
'''