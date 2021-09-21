from django.http import HttpResponse
from django.shortcuts import render,redirect

#!Burda login_required decoratorunu ozumuz  yazirig
def unauthenticated(view_func):#burdaki view_func gelen funisylari oxuyur @decorator kimi istifade edirik uncuatnticade_user funksiysni
    def wrapper_func(request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request,*args,**kwargs)#yeni giris etmeyibse gonderdiyim funksiya islesin
    return wrapper_func

#!Hasni istifadeciler icaze verilibse onlara olar
def allowed_user(allowed_roles = []):
    def decorator(view_func):#burda decoratora gelen funksiyalar olur
        def wrapper(request,*args,**kwargs):#burda ise funksiyanin aldigi parametrler yazilir
            group = None
            if request.user.groups.exists():#yeni hal hazirdaki istifadeci qrupda varsa
                group = request.user.groups.all()[0].name
            if group in allowed_roles:#eger group allowed_userda varsa,decotaror gonderilen seyfeler islecej burda esasen admini qeyd edeciyikki yeni admin getsin ancag bu seyfelere
                return view_func(request,*args,**kwargs)
            else:
                return HttpResponse('You are not authorized to view this page')
        return wrapper
    return decorator

#!Yalniz adminin edeceyi seyler
def admin_only(view_func):#yalniz adminin gedeceyi url ler
    def wrapper(request,*args,**kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        
        if group == 'customer':#yeni hal hazirdaki istifadeci musteri grupuna daxildirse
            return redirect('user-page')
        if group == 'admin':#eger giren istifadeci admin categoriyasina daxildirse
                return view_func(request,*args,**kwargs)
    return wrapper