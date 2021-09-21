from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save #!pre_save ile post_save eyni isi gorur ferq etmir
# Create your models here.

#!Customer yeni musteri haqindaki melumatlar Customer modelinde olacag

class Customer(models.Model):
    user = models.OneToOneField(User,null=True, blank=True,on_delete=models.CASCADE)#*Burda oneToOneField yazilmasindaki sebeb yeni her bir musterinin yalniz bir hesabi ola biler 1 adnan 2 hesab acmag mumkun deyil
    name = models.CharField(max_length=200,null=True)#yeni databasede goruncek
    phone = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200,null=True)
    profile_pic = models.ImageField(null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    
    def __str__(self):
        return self.name or '' #burda bunu yazmasag Customert yaradilandan sonra id deyeri gosterilir onun gorunmeyen kodu beledir return str(self.id)

class Tag(models.Model):#taglar cox olur yeni coxa coxa bele deyim yeni manytomanyfield kimi olur
    name = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.name

#!Burdaki Product classi yeni modeli icinde ise mal haqinda melumat verilir
class Product(models.Model):
    CATEGORY = (
        ('Indoor','Indoor'),#Burdaki birincvi deyerler key deyerleridir ikinci deyerler ise Value deyerleridiri
        ('Out Door','Out Door')
    )#amma bu cur kategoriya yaradanda admin panelde elave etmek olmur yeni yeni bir kategoriya amma foreign key vasitesile yaradanda olur bu
    
    name = models.CharField(max_length=200,null=True)
    price = models.FloatField(default=0,null=True)  
    category = models.CharField(max_length=200,null=True,choices=CATEGORY)#Burda scroollbar kimi acilir ve secim  edirsen Indoor ve YA Outdoor seklinde
    description = models.TextField(max_length=500,null=True,blank=True)#blank = true o demekdirki yeni bos kecirilie biler bu alan
    image = models.ImageField(blank=False,null=True,verbose_name='Add Picture')
    date_created = models.DateTimeField(auto_now_add=True)
    tag = models.ManyToManyField(Tag)
    
    def __str__(self):
        return self.name

#!Bu Order modeli ise Sifaris haqqinda melumat verir
class Order(models.Model):  
    STATUS = (
        ('Pending','Pending'),#pending => bitmemis yeni catmayan mal bele deyimm
        ('Out for delivery','Out for delivery'),
        ('Delivered','Delivered'),
    )
    
    customer = models.ForeignKey(Customer,null=True,on_delete=models.SET_NULL)#Foreign key yeni teke cox iliski Yeni bir Customer coxlu sayda sifaris vere biler meselen men ,,,kitab,rucka,karandaas sifaris verirem
    product = models.ForeignKey(Product,null=True,on_delete=models.SET_NULL)#SET_NULL o demekdirki yeni bir modeldeki Product silinse bele onun haqqinrdaki melumatlat databaseye enull sekilnde oturulurku hata vermesin sonra
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200,null=True,choices = STATUS)#Burdaki choices butun mallar ucun istifade olunan bir islev gorur ele bil yuxarda yazilan STATUS butun mallar uzerinden istfiade olunacag ona gore Foreign key vaistesile yazmagdig
    
    def __str__(self):
        return self.product.name or ''
    
    
