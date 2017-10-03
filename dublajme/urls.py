"""dublajme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from track.api import TrackResource, CourseResource

track_resource = TrackResource()
course_resource = CourseResource()

# v1_api = Api(api_name='v1')
# v1_api.register(TrackResource())
# v1_api.register(CourseResource())

urlpatterns = [
    url(r'^api/', include(course_resource.urls)),
    url(r'^api/', include(track_resource.urls)),

    url(r'^admin/', admin.site.urls),
]

