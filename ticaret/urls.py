"""ticaret URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('manage/admin/', admin.site.urls),
    path('manage/',include("manage.urls")),
    path('',views.home,name="home"),
    path('signin/',views.signin,name="signin"),
    path('signup/',views.signup,name="signup"),
    path('signUp/',views.signUp),
    path('about/',views.about,name="about"),
    path('logincontrol/',views.logincontrol),
    path('checkproduce/',views.checkproduce,name="checkproduce"),
    path('detailproduce/',views.detailproduce),
    path('addcomment/',views.addcomment),
    path('contact/',views.contact,name="contact"),
    path('addContact/',views.addContact,name="addContact"),
    path('search/',views.search,name="search"),
    path('checkout/',views.checkout,name="checkout"),
    path('privacypolicy/',views.privacypolicy,name="privacypolicy"),
    path('listcategory/',views.listcategory),
    path('basket/',views.basket,name="basket"),
    path('addBasket/',views.addBasket),
    path('uponequantity/',views.uponequantity),
    path('downonequantity/',views.downonequantity),
    path('removeBasket/',views.removeBasket),
    path('baskett/',views.baskett,name="baskett"),
    #path('baskettt/',views.baskett,name="baskettt"),
    path('clearBasket/',views.clearBasket,name="clearBasket"),
    path('logout/',views.logout,name="logout"),

   
]   


urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)