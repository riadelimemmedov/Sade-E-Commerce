from django.contrib import admin
from django.urls import path,include
from accounts.templatetags import custom_tags
from django.contrib.auth import views as auth_views
from . views import *


urlpatterns = [
    path('',home,name='home'),
    path('product/',product,name='product'),
    path('customer/<int:id>',customer,name='customer'),
    path('create_order/<str:id>',createOrder,name='create_order'),
    path('update_order/<int:id>',sifarisgucelle,name='update_order'),
    path('delete_order/<int:id>',deleteOrder,name='delete_order'),
    path('search/',custom_tags.axtaris,name='search'),
    path('register/',registerPage,name='register'),
    path('login/',loginPage,name='login'),
    path('logout/',logOutPage,name='logout'),
    path('detail/',detailPage,name='detail'),
    path('user/',userPage,name='user-page'),
    path('account/',accountSettings,name='account'),
    
    
    path('reset_password/',auth_views.PasswordResetView.as_view(),name='reset_password'),#Bir kullanıcının, parolayı sıfırlamak için kullanılabilecek bir kerelik kullanım bağlantısı oluşturarak ve bu bağlantıyı kullanıcının kayıtlı e-posta adresine göndererek parolasını sıfırlamasına izin verir.
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),#return redirect kimidir PassswordResetDovieew email gonderilenden sonra qayidir her hansisa bir seyfeye,yalniz email amma hele biz o emaile girib linke tiklamamisig
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),#Burda PasswordResetConfirm view ise yeni sifremizi girmek ucun bize form gonderer
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete')#Kullanicinn sifresini basarilis bir sekilde deyisdini mesajini verer Passwordresetcompleteview

]   