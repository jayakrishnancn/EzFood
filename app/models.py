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

class MenuItem(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length = 100)
    price = models.IntegerField(default=100)
    image = models.ImageField(upload_to="upload",default='default.svg')
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username + " - " + self.name + " : " + str(self.price) + " : " + str(self.active)

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
class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    delivered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username + " ordered " + str(self.quantity) + " " + self.item.name + " with id" + str(self.item.id) + " and  is deleverted:" + str(self.delivered) 

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()