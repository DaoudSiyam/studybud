from django.forms import ModelForm
from .models import Room, Message, User
from django.contrib.auth.forms import UserCreationForm


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']
        # password1 is password
        # password2 is psawword confirmation

# this class inherit attributes from ModelForm
class RoomForm(ModelForm):
    # now we need 2 minimum values
    # firstly specify the model that we want to create a form for
    # and then specify the field
    class Meta:
        model = Room
        fields = '__all__'
        # what this does is it will create the form based on 
        # the meta data of the Room class
        # which means that it will create a dropdown list, a topic value
        # a text field for a name, description etc...
        # __all__ means return all the fields of the specified class
        # but we can design it as a list to return speific values
        # such as : fields = ['name', 'description'] etc...
        exclude = ['host','participants',]
        # exclude basically excludes the attributes we do not want

# after we are done, we will be exporting
# this file to the views file

class MessageForm( ModelForm ):
    class Meta:
        model = Message
        fields = ['body',]


class UserForm (ModelForm):
    class Meta:
        model = User
        fields = ['avatar','name','username', 'email', 'bio']
