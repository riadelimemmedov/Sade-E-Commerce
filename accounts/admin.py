from django.contrib import admin
from .views import *
from .models import *
# Register your models here.
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Tag)