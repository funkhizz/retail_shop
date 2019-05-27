from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from .signals import object_viewed_signal
from .utils import get_client_ip
from django.contrib.sessions.models import Session
from django.db.models.signals import pre_save, post_save
from accounts.signals import user_logged_in

User = settings.AUTH_USER_MODEL
FORCE_SESSION_TO_ONE = getattr(settings, 'FORCE_SESSION_TO_ONE', False)
FORCE_INNACTIVE_USER_ENDSESSION = getattr(settings, 'FORCE_INNACTIVE_USER_ENDSESSION', False)

class ObjectViewed(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE) # User instance
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE) # User, Product, Order, Cart, Address
    object_id = models.PositiveIntegerField() # User id, Product id, Order id
    content_object = GenericForeignKey('content_type', 'object_id') # Product instance
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.CharField(max_length=220, blank=True, null=True) # IP field

    def __str__(self):
        return "%s viewed %s" %(self.content_object, self.timestamp)

    class Meta:
        ordering = ['-timestamp'] # most recent saved first
        verbose_name = 'Object viewed'
        verbose_name_plural = 'Objects viewed'

def object_viewed_receiver(sender, instance, request, *args, **kwargs):
    c_type = ContentType.objects.get_for_model(sender) # instance.__class__
    # print(sender)
    # print(instance)
    # print(request)
    # print(request.user)
    new_view_obj = ObjectViewed.objects.create(user=request.user,
                                                object_id=instance.id,
                                                content_type=c_type,
                                                ip_address=get_client_ip(request)
    )

object_viewed_signal.connect(object_viewed_receiver)

class UserSession(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE) # User instance
    timestamp = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(max_length=100, blank=True, null=True)
    ip_address = models.CharField(max_length=220, blank=True, null=True) # IP field
    active = models.BooleanField(default=True)
    ended = models.BooleanField(default=False)

    def end_session(self):
        session_key = self.session_key
        ended = self.ended
        try:
            Session.objects.get(pk=session_key).delete()
            self.ended = True
            self.active = False
            self.save()
        except:
            pass
        return self.ended


def post_save_session_receiver(sender, instance, created, *args, **kwargs):
    if created:
        qs = UserSession.objects.filter(user=instance.user, ended=False, active=False).exclude(id=instance.id)
        for i in qs:
            i.end_session()
    if not instance.active and not instance. ended:
        instance.end_session()

if FORCE_SESSION_TO_ONE:
    post_save.connect(post_save_session_receiver, sender=UserSession)

def post_save_user_changer_receiver(sender, instance, created, *args, **kwargs):
    if not created:
        if instance.is_active == False:
            qs = UserSession.objects.filter(user=instance.user, ended=False, active=False)
            [i.end_session() for i in qs]

if FORCE_INNACTIVE_USER_ENDSESSION:
    post_save.connect(post_save_user_changer_receiver, sender=User)

def user_logged_in_receiver(sender, instance, request, *args, **kwargs):
    print(instance)
    session_key = request.session.session_key
    user = instance
    ip_address = get_client_ip(request)
    UserSession.objects.create(user=user, session_key=session_key, ip_address=ip_address)
user_logged_in.connect(user_logged_in_receiver)