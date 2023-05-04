from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# what this does is restrict access to some pages
# that can only be accessed if the user is logged in

from django.db.models import Q
# Q is what will allow us to do multiple and complex queries
# so that we can be allowed to do dynamic searches


from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, Message, User
from .forms import RoomForm, MessageForm, UserForm, MyUserCreationForm


# for rendering rooms
# a python list that has dictionaries
# each room has an id
# rooms = [
#     { 'id':1,  'name': 'Lets Learn Python!'},
#     { 'id':2,  'name': 'Design with me'},
#     { 'id':3,  'name': 'Frontend developers'},
# ]
# we want to be able to render this data
# out inside of a template


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get( 'email' ).lower()
        password = request.POST.get( 'password' )
        # these 2 values will be sent from the fr++ont end

        # then i'll make sure if this user exists
        # through try and catch blocks
        try:
            user = User.objects.get( email = email )
            # this is what we write to check if user exists
        except:
            messages.error( request, 'User does not exist' )

        user = authenticate( request, email = email, password = password)
        # this will eitgher give us an error or
        # a user that matches these credentails        

        if user is not None:
            login( request, user )
            # login method will add a session in the database
            # and then also add the session for the user in the browser
            return redirect( 'home' )
        else:
            messages.error( request, 'Username OR Password does not exist' ) 
        # if we remove session id from the browser
        # it directly logs the user out

            
    context = { 'page': page}
    return render( request, 'base/login_register.html', context )


def logoutUser(request):
    logout(request)
    # what this does is delete that web token
    # thus means logging out the user
    return redirect('home')


def registerPage(request):   
    # a predefined regestration form that is provided by django 
    form = MyUserCreationForm()

    if request.method == 'POST':
        # POST is the password and username
        # and all the user's credentials
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user =  form.save( commit = False )
            # what this does is saving the form
            # and freezing it in time because
            # we want to access the user that was created right away
            # so this is why we add commit = False
            # this allows us to access the user directly after creation
            user.username = user.username.lower()
            # this is a form of cleaning the data
            # we don't want all the data to be different
            # if the user wrote his username in upper case
            # this automatically changes his name to lower case
            user.save()
            login( request, user)
            return redirect('home')
        else:
            messages.error( request, 'An error occured during regestration')

    
    return render( request, 'base/login_register.html', { 'form': form} )


def home( request ):
    q = request.GET.get( 'q' ) if request.GET.get( 'q' ) != None else ''

    rooms = Room.objects.filter(
        Q ( topic__name__icontains = q ) |
        Q ( name__icontains = q ) |
        Q ( description__icontains = q)
        )[0:10]
    # now we are allowed to search by 3 different values
    # first parameteres is responsible for rendering the page
    # upon inputing topic name, we retrieve the topic
    # we want to make this more dynamic
    # by applying the search function to multiple parameters
    # there is a method called q look up
    # it will allow to add (and) / (or) statements
    # so that we can get allowed to search dynamically
    # and means that the url must contain both parameters
    # or means that one is enough
    # & represents and .... | represents or

    topics = Topic.objects.all()[0:5] # limits the topic count in the home page
    # or in other words render the first 5 topics in the home page
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(
        room__topic__name__icontains = q
    ))[0:11] # limits message count to be viewed to 11 elements
    # it's called the Q lookup method
    # what we have done now is just filter down 
    # the messages by the room name 

    context = { 'rooms' : rooms, 'topics': topics ,
                'room_count': room_count, 'room_messages': room_messages }
    return render( request, 'base/home.html', context )


def room( request, pk ):
    room = Room.objects.get( id = pk )
    room_messages = room.message_set.all()
    # using the _set.all method we specify 
    # the model name in a small letter
    # the _set.all is the many to one method
    participants = room.participants.all()
    # we can directly call the all method
    # if the relationship was many to many
    # we can also filter these down if we want
    if request.method == 'POST':
        Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body'),
        )
        room.participants.add(request.user)
        # this is how we add the user to the participants
        return redirect('room' , pk = room.id )

    context = { 'room': room, 'room_messages': room_messages,
               'participants': participants, }
    return render( request, 'base/room.html', context )
    

def userProfile(request, pk):
    user = User.objects.get(id = pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    # through this move, i can get all the children
    # for a specific object
    context = {'user': user, 'rooms': rooms, 
               'room_messages': room_messages, 'topics': topics }    
    return render(request, 'base/profile.html', context)


# this annotation is required if we don't want to show
# a certain view in our application
# unless the user is logged in
# aka provides protected routes
# but instead called protected views
# or restricted pages

# what will happen is if a user is not logged in
# they will be redirected to the login page
@login_required(login_url = 'login')
def createRoom( request ):
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == 'POST':    
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create( name = topic_name )
        # what get_of_create is it differes if the object is created or not
        # so if it is already created it gets it
        # and if it's not, it creates it
        # this is done to minimize boilerplate code

        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            # name will be passed in from the form values
            description = request.POST.get('description'),
        )
        return redirect( 'home' )            

    context = { 'form' : form, 'topics': topics} 
    return render( request, 'base/room_form.html', context )


# now to update, we need to create a view
# for updating existing data, we will use the same form template
# we need to pass in a primary key to differ what item to be updated


@login_required(login_url = 'login')
def updateRoom( request, pk ):
    room = Room.objects.get( id = pk )
    form = RoomForm( instance = room )
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create( name = topic_name )        
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect( 'home' )
    context = { 'form' : form, 'topics': topics,
                'room' : room }
    return render( request, 'base/room_form.html', context )


@login_required(login_url = 'login')
def updateMessage( request, pk ):
    message = Message.objects.get( id = pk )
    form = MessageForm( instance = message )
    
    if request.user != message.user:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        form = MessageForm ( request.POST, instance = message )        
        if form.is_valid():
            form.save()
            return redirect( 'home' )
    context = { 'form' : form }
    return render( request, 'base/room_form.html', context )


@login_required(login_url = 'login')
def deleteRoom( request, pk ):
    room = Room.objects.get( id = pk )

    if request.user != room.host:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        room.delete()
        # delete is remove item from database and delete it
        return redirect( 'home' )
    # you pass this in as what you have specified it in the template
    return render( request, 'base/delete.html', { 'obj' : room } )
    # what we want to do is specify the room we want to delete

@login_required(login_url = 'login')
def deleteMessage( request, pk ):
    message = Message.objects.get( id = pk )

    if request.user != message.user:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        message.delete()
        # delete is remove item from database and delete it
        return redirect( 'home' )
    # you pass this in as what you have specified it in the template
    return render( request, 'base/delete.html', { 'obj' : message } )
    # what we want to do is specify the room we want to delete
    # obj is the same entity that is present in the delete.html file
    # so we pass in the object value which is a message

@login_required(login_url = 'login')
def updateUser(request):
    user = request.user
    form = UserForm( instance = user )
    # this is what makes sure to get the initial user value

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance = user)
        # request.FILES is what is going to tell django 
        # that there will be files on submission
        if form.is_valid():
            form.save()
            return redirect('user-profile' , pk = user.id)

    return render(request, 'base/update-user.html', { 'form' : form } )
    # we don't need a primary key because
    # we will perform everything on the logged in user


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request,'base/topics.html',{ 'topics' : topics })

def activityPage( request ):
    room_messages = Message.objects.all()

    return render( request, 'base/activity.html', {'room_messages' : room_messages})