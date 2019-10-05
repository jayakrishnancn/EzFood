from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    role = models.CharField(max_length=20,default="normal")

    def __str__(self):
        return self.role


class Restaurant(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 100)
    address1 = models.CharField(max_length=100,default='')
    address2 = models.CharField(max_length=100,default='')
    country = models.CharField(max_length=100,default='')
    state = models.CharField(max_length=100,default='')
    zip = models.CharField(max_length=100,default='')
    location = models.CharField(max_length = 100,default="India")
    tag = models.CharField(max_length=100,default='')
    
    def __str__(self):
        return self.name

    @classmethod
    def create(cls, name,location):
        restaurant = cls(name=name,location=location)
        # do something with the book

        return restaurant

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()