from django.db.models.signals import  post_save
from django.contrib.auth.models import User
from.models import Customer
from django.contrib.auth.models import Group

#!Djangodaki signallar o ise yarayirki meselen biz register oldug he hemin register oldugumuz istifadecini hemde musteri modelinde yeni profilinde yaratmaliyig signallar bu isi gorur eyni 2-3 isi eyni vaxtdan biz etmeden edir
def customer_profile(sender,instance,created,**kwargs):#yeni register olanda avtomatik userprofile yaradilacag
    if created:#eger register olmusugsa
            group = Group.objects.get(name='customer')
            instance.groups.add(group)#regitser olan istifaedcinin elave edirsen customer groupuna
            Customer.objects.create(
                    user=instance,
                    name = instance.username,
            )
            print('Profile created')
post_save.connect(customer_profile,sender=User)