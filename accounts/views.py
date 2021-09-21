from django.shortcuts import render,HttpResponseRedirect,HttpResponse,get_object_or_404,redirect
from django.forms import inlineformset_factory
from .filters import OrderFilter#!filterts dosyasi form dosyalarini oxsayir
from django.db.models import F, Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from.decorators import *
from .models import *
from . forms import *

# Create your views here.
@login_required(login_url='login')
#@allowed_user(allowed_roles = ['admin'])#burda qeyd etmeyi unutma,yenin istifadeci icazeleri
@admin_only#yeni home seyfesinde admin olacag yalniz
def home(request):
    orders = Order.objects.all()#sifarisleri getirdik burda
    customers = Customer.objects.all()#burda ise musterileri getirdik
    
    total_customers = customers.count()
    
    total_orders = orders.count()
    delivered = orders.all().filter(status='Delivered').count()
    pending = orders.all().filter(status = 'Pending').count()
    
    
    context = {
        'orders': orders,
        'customers': customers,
        'total_customers': total_customers,
        'total_orders':total_orders,
        'delivered':delivered,
        'pending':pending
    }
    
    return render(request,'accounts/dashboard.html',context)#Htpp Redirrecdende istfiade ede bilersen problem yoxdur

    
@login_required(login_url = 'login')#yeniki UserPage seyfesine getmek isteyirsense mutleq login olmalisan
@allowed_user(allowed_roles=['customer'])#!yeniki UserPage seyfesine customerlert gire biler
def userPage(request):#?Bu seyfe musterilerin sifarislerinin cemlendiyi seyfedir    
    orders = Order.objects.filter(customer__user = request.user)
    #orders = request.user.customer.order_set.all()#belede yazmag olar ferq etmir
    total_order = orders.all().count()
    order_delivered = orders.filter(status = 'Delivered').count()#?delivered => catdirilmis
    order_pending = orders.filter(status = 'Pending').count()#?pending => gozleyen
    context = {
        'orders':orders,
        'total_order':total_order,
        'order_delivered':order_delivered,
        'order_pending':order_pending,
    }
    return render(request,'accounts/user.html',context)


@login_required(login_url='login')#*login required decoratoru vasitesile her hansi bir seyfeye gedenden giris etmemisense seni login seyfesine gonderirki get giris ele yeni login ele sonra yeniden gel
@allowed_user(allowed_roles = ['admin'])
def product(request):#render => yenilenmekdir
    products = Product.objects.all()

    
    context = {
        'products': products,
    }
    return render(request,'accounts/products.html',context)

@login_required(login_url='login')
@allowed_user(allowed_roles = ['admin'])
def customer(request,id):
    customer = get_object_or_404(Customer,id=id)
    #Indi ise hemin musteri yeni customerin sifarislerini almag lazimdir buna gorede sql e bir query gondermek lazimdir
    sifarisler = customer.order_set.all()#?Yeni hemin istifadeciye adi olan butun sifarisleri getirmek ucun yazilir customer.order_set.all() kodu
    total_order = customer.order_set.all().count()#burda customeri qeyd etmeyi unutma cunki her istifadecinin ayri bir sifarisi olur ona gore istifadecileri qeyd et sorgu gonderende yeni query gonderende sql e
    
    myFilter = OrderFilter(request.GET,queryset=sifarisler)#getden gelen butun sifarisler searchde hemise method.get yaz
    sifarisler = myFilter.qs#neticelerin gorunmesi ucun yeniden qs yeni query yazmaliyamki axtrisdan cixan neticeler gorunsun
    #?Burda qs bizim verdiyimiz sorgudur onu gonderirik butun sifarislerin icine OrderFilter vasitesile ytoxlayirig
    
    context = {
        'customer':customer,
        'sifarisler':sifarisler,
        'total_order':total_order,
        'myFilter':myFilter
    }
    return render(request,'accounts/customer.html',context)


#!Sifaris yaratma  ,sifaris update etme ve ,sifaris silme islemleri 
@login_required(login_url='login')
@allowed_user(allowed_roles = ['admin'])
def createOrder(request,id):
    OrderFormSet = inlineformset_factory(Customer,Order,fields=['product','status'])#inlineformset_factory vaistesile bir form icinde coxlu sayda Modeller istifade ede bilirsen
    customer = Customer.objects.get(id=id)#yeni hemin id li Istifadeciye get
    form = CreateOrder(request.POST or None,request.FILES or None,initial = {'customer':customer})#request.Post or None vasutesile yoxlandir zaten birde if request.method = 'POST' yazilmasindaki ehtitac yoxdur
    if form.is_valid():#initial bir dictionary deyer isteyir yeni form un input yerinde hazir sekilde deyerler gosteriler bilir default deyerler yeni initial vasitesile
        sifaris_istifadecisi = form.save(commit=False)
        sifaris_istifadecisi.customer__name = request.user#yeni deqiq olsunki hemin istifadeci verib sifarisi
        sifaris_istifadecisi.save()
        return redirect('home')        
    context = {
        'form':form,
    }
    return render(request,'accounts/order_form.html',context)

@login_required(login_url='login')

def sifarisgucelle(request,id):#cunki secilen bir sifarisi update edirsen yeni bu evvelceden movcud olubu databasede yeni bunun bir yeri var databasede yeni bir id si var
    sifaris = get_object_or_404(Order,id=id)
    form = CreateOrder(request.POST or None,request.FILES or None,instance=sifaris)
    #Yuxarida reuest.Post or None yazilsidigina gore birde if e girib request.method == 'POST' yazilmasina ehtiyac yoxdur
    if request.method == 'POST':
        form = CreateOrder(request.POST or None,request.FILES or None,instance=sifaris)
        if form.is_valid():
            sifaris_update = form.save(commit=False)
            sifaris_update.customer__name = request.user
            sifaris_update.save()
            return redirect('home')#Burdaki home deyeri url deki name = 'home' deyeridir
        
    context = {
        'form':form
    }
    return render(request,'accounts/order_update_form.html',context)

# def deleteOrder(request,id):#yeni hemin id li sifarisi sil unutma birde deletede return rendere ehtiyac yoxdur ,,,,bir dene return redirect yazmag lazimdir
#     verilen_sifaris = get_object_or_404(Order,id=id)
#     verilen_sifaris.delete()#Djangoda .delete seklinde yazilir
#     return redirect('home')


#*Ve ya bu curde yazmag olar delete funksiyasini
@login_required(login_url='login')
@allowed_user(allowed_roles = ['admin'])
def deleteOrder(request,id):
    silinen_sifaris = get_object_or_404(Order,id=id)
    if request.method == 'POST':
        silinen_sifaris.delete()
        return redirect('home')

    context = {
        'silinen_sifaris':silinen_sifaris
    }
    return render(request,'accounts/delete_order_form.html',context)

# def searchView(request):
#     query = request.GET.get('q')
    
#     if query:
#         post = Product.objects.filter(Q(name__icontains=query)|
#                                       Q(category__icontains=query)|
#                                       Q(tag__name__icontains=query)).order_by('-id').distinct()
#         return render(request,'accounts/search.html',{'post':post})
    
#     else:
#         post = Product.objects.all()
#         return render(request,'accounts/search.html',{'post':post})#else in icinde yaz return ni yazmasan islemez gonderilen sorgu

def detailPage(request):
    post = Product.objects.all()
    context = {
        'post':post
    }
    return render(request,'accounts/mallar.html',context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])#yeni ancag musterile gele bilsin bu seyfeye
def accountSettings(request):
    customer = request.user.customer#yeni giris eden isitfadecinin yeni musterinin Customer modulunden melumatlari gelsin bura
    form = CustomerForm(instance=customer)
    
    if request.method == 'POST':
        form = CustomerForm(request.POST or None,request.FILES or None,instance=customer)#burda instanceye hal hazirdaki musteri bilgilerini gonderdik,request.files or none yazilmasindaki sebeb ise forms vasitesile sekil yukleiryik htmlden ona gore
        if form.is_valid():
            form.save()
    
    context = {
        'form':form
    }
    return render(request,'accounts/account.html',context)


#!Account Proses
@unauthenticated
def registerPage(request):
    # if request.user.is_authenticated:#eger istifadeci giris eleyibse demeli bir hesabi varki giris edib
    #     return redirect('home')
    
    
    
    if request.method == 'POST':#method = POST olanda islencek kodlar
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            
            ad = form.cleaned_data.get('username')
            mail = form.cleaned_data.get('email')
            sifre = form.cleaned_data.get('password1')
            sifre2 = form.cleaned_data.get('password2')
            
            if sifre == sifre2:#yeni girilen sifreler bir birine beraberidirse
                if User.objects.filter(username = ad).exists():
                    messages.add_message(request,messages.WARNING,'This UserName Avaible This Site')
                    return redirect('register')
                else:
                    if User.objects.filter(email = mail).exists():#exists yeni bele bir mail varsa eger
                        messages.add_message(request,messages.WARNING,'This Email Avaible This Site')
                        return redirect('register')
                    
                    else:
                        form.save()
                        username = form.cleaned_data.get('username')
        
                        
                        messages.add_message(request,messages.SUCCESS,'Account has been created ' + ad)
                        return redirect('login')
            else:#eger sifreeler beraber deyilse yeni dogru deyilse
                messages.add_message(request,messages.INFO,'Passsword False')
                return redirect('register')
    else:
        form = RegisterForm()
        
    context = {
        'form':form
    }
    
    return render(request,'accounts/register.html',context)

@unauthenticated
def loginPage(request):
    # if request.user.is_authenticated:#eger giris elemisemse home qayit name=home olan url e qayit
    #     return redirect('home')
    
    if request.method == 'POST':
        ad = request.POST.get("username")
        sifre = request.POST.get("password")
        
        user = authenticate(request,username=ad,password=sifre)#authecticate bele bir istifadecnin olub olmadigini yoxlayir
        if user is not None:#eger bele bir istifadeci varsa
            login(request,user)
            messages.add_message(request,messages.SUCCESS,'Create Account')
            return redirect('home')
        else:#yox egeer bele bir istifadeci yoxdursa ve ya basqa bir problem varsa else gir cunki else hemise isleyir
            messages.add_message(request,messages.ERROR,'Error username or password')
    
    return render(request,'accounts/login.html')

def logOutPage(request):
    logout(request)
    return redirect('home')
