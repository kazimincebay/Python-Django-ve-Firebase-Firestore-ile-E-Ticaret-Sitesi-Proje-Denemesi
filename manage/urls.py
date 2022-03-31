
from django.urls import path,include
from . import views 

urlpatterns=[
    path('',views.signin,name="signinn"),
    path('index/',views.index,name="manage/index"),
    path('companyinfo/',views.companyinfo,name="companyinfo"),
    path('addcategory/',views.addcategory,name="addcategory"),
    path('addCategory/',views.addCategory),
    path('addproduce/',views.addproduce,name="addproduce"),
    path('addProduce/',views.addProduce),
    path('checkproduce/',views.checkproduce,name="checkproduceadmin"),
    path('updateproduce/',views.updateproduce),
    path('updateProduce/',views.updateProduce),
    path('contactforms/',views.contactforms,name="contactforms"),
    path('checkcategory/',views.checkcategory,name="checkcategory"),
    path('updatecategory/',views.updatecategory),
    path('updateCategory/',views.updateCategory),
    path('deletecategory/',views.deletecategory),
    path('deleteCategory/',views.deleteCategory),
    path('checkuser/',views.checkuser,name="checkuser"),
    path('logincontrol/',views.logincontrol,name="logincontrol"),

]