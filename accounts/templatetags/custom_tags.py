from django import template
from django.contrib import messages
from django.shortcuts import render,HttpResponseRedirect,HttpResponse,get_object_or_404,redirect
from django.db.models import F, Q
from accounts.models import *
#!templatetaglardan databaseye sorgun gonderib hemin sorgunu hansi templatede gostermek isteyirsen gostere bilersen
#!Birde viewdaki kimi url filan qeyd etrmeye ehtiyac yoxdur amma name qeyd etmelisen

register = template.Library()

@register.simple_tag(name='sonsifaris')#burdaki name i hansi template de istesek istifade ede bilerik
def last_order():
    return Order.objects.order_by('-date_created')[:5]


def axtaris(request):
    query = request.GET.get('q')
    
    if query:
        netice = Product.objects.filter(Q(name__icontains=query)|
                                        Q(category__icontains=query)).order_by('-id').distinct()
        return render(request,'accounts/mallar.html',{'netice':netice})
    else:
        messages.add_message(request,messages.ERROR,'Not Found Goods')
        return redirect('home')

