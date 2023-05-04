"""practice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# this will give us access to settings.py
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    # this means for every url that matches an empty string
    # go ahead and use the include function
    # and send the user to base.url
    
    path('api/', include('base.api.urls'))
    # this means that any route that starts with api
    # send them to this file
    # and it will take care of everything for you
]

# instead of adding we will be appending the static path
# for the user uploaded file, in our case images
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
# basically what happens here is we are setting the url
# and the file path will be MEDIA_URL from settings
# in short we tell it set the url and get the url
# from media root, so this is how we connect both of these things

#this will be the root directories urls file