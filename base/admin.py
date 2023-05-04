from django.contrib import admin

# Register your models here.
from .models import Room, Topic, Message, User
# we want to be able to view this item in the admin panel
# and work with it in the built in admin panel

admin.site.register( User )
admin.site.register( Room )
admin.site.register( Topic )
admin.site.register( Message )
# after this line of code
# we will be able to view the registerd item in the admin panel
