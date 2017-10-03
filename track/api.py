# myapp/api.py
from tastypie.resources import ModelResource
from track.models import Track, Course
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication

class TrackResource(ModelResource):
    class Meta:
        queryset = Track.objects.all()
        resource_name = 'track'
        allowed_methods = ['get', 'post', 'put']
        authentication = Authentication()
        authorization = Authorization()

class CourseResource(ModelResource):
    class Meta:
        queryset = Course.objects.all()
        resource_name = 'course'
        allowed_methods = ['get', 'post', 'put']
        authentication = Authentication()
        authorization = Authorization()

        