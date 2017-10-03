# myapp/api.py
from tastypie.resources import ModelResource
from track.models import Track, Course
from tastypie.authorization import DjangoAuthorization


class TrackResource(ModelResource):
    class Meta:
        queryset = Track.objects.all()
        resource_name = 'track'
        authorization = DjangoAuthorization()
        authentication = ApiAuthentication()


class CourseResource(ModelResource):
    class Meta:
        queryset = Track.objects.all()
        resource_name = 'course'
        authorization = DjangoAuthorization()
        authentication = ApiAuthentication()

        