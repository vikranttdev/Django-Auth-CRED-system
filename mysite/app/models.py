from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist


class Profile(models.Model):
    new_field = models.CharField(max_length=140, default='your_default_value')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    forget_password_token = models.CharField(max_length=100)
    created_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.username

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    # if created:
    #     Profile.objects.create(user=instance)
    # instance.profile.save()

    try:
        instance.profile.save()
    except ObjectDoesNotExist:
        Profile.objects.create(user=instance)


class Employees(models.Model):
    name= models.CharField(max_length=30)
    email= models.CharField(max_length=30)
    address= models.TextField()
    phone= models.IntegerField()

    def __str__(self):
        return self.name
