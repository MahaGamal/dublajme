
from django.db.models.signals import pre_save
from django.dispatch import receiver
from track.models import Track, Course


@receiver(post_save, sender=Track)
def my_handler(sender, instance, created, **kwargs):
    if created:
       course_obj= Course.objects.filter(base_url=get_base(instance.origin_url))
       print course_obj
       instance.course=course_obj.get()
       instance.Track.save()

    
    
def get_base(url):
    surl = url.split("/")[3]
    base_url = "https://www.udemy.com/" + surl
    return base_url