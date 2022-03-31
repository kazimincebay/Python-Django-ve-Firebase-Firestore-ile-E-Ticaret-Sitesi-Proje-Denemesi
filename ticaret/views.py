from django.shortcuts import render,redirect
import pyrebase
import requests
import datetime
from requests.sessions import session
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import JsonResponse
import json
import uuid
import firebase_admin
from firebase_admin import credentials,firestore


cred=credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

config = {
  
}

firebase=pyrebase.initialize_app(config)
authe=firebase.auth()
database = firestore.client()
storage = firebase.storage() 

def signin(request):
    if request.method=="POST":
        userid = request.POST.get('userid')
        context={
            'userid':userid
        }
        return render(request,"signin.html",context)
    return render(request,"signin.html")

def logincontrol(request):
    if request.method=="POST":
        userid=request.POST.get('userid')
        email = request.POST.get('email')
        username=email
        password = request.POST.get('password')

        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request, user)
            print("login başarılı")
            if userid != "":
                baskets=database.collection("Baskets").where("useremail","==",userid).get()

                for basket in baskets:
                    if basket.to_dict()["useremail"]==userid:
                        key=basket.id
                        print(key)
                        database.collection("Baskets").document(key).update({"useremail":email})
            return redirect("home")
        else:
            print("kullanıcı adı veya parola yanlış")
            return redirect("signin")
    return redirect("signin")

def signup(request):
    return render(request,"signup.html")

def signUp(request):
    name=request.POST.get("name")
    surname=request.POST.get("surname")
    email=request.POST.get("email")
    username=email
    reemail=request.POST.get("email")
    userid=str(uuid.uuid1())
    password=request.POST.get("password")
    repassword=request.POST.get("repassword")
    phonenumber=request.POST.get("phonenumber")
    data={
        'userid':userid,
        'name':name,
        'surname':surname,
        'email':email,
        'phonenumber':phonenumber
        }
    if password==repassword:
        if User.objects.filter(username=username).exists():
            print("bu kullanıcı adı daha önce alınmış")
        else:
            if User.objects.filter(email=reemail).exists():
                print("bu mail daha önce alınmış")
            else:
                user = User.objects.create_user(username=username,password=password,email=email,first_name=name,last_name=surname)
                user.save()
                
                
                return redirect("signin")
    
    

    message="Kayıt işlemi başarı ile tamamlandı"
    return redirect("signin")

def home(request):
    categorylist = []
    categories=database.collection("Categories").get()
    companyinfolist= []
    companyinfo=database.collection("Companyinfos").get()
        
    for company in companyinfo:
        data = company.to_dict()
        companyinfolist.append(data)
        
    for category in categories:
        data = category.to_dict()
        categorylist.append(data)
    print(categorylist)
        
   

    context = {
        'categorylist':categorylist,
        'companyinfolist':companyinfolist
        

        }
    return render(request,"index.html",context)

def companyinfo(request):
    companyinfolist= []
    companyinfo=database.collection("Companyinfos").get()
        
    for company in companyinfo:
        data = company.to_dict()
        companyinfolist.append(data)

    context = {
        'companyinfolist':companyinfolist
        }


    return render(request,"fix-parts/footer.html",context)


def about(request):
    return render(request,"about.html")


def privacypolicy(request):
    return render(request,"privacypolicy.html")

def contact(request):
    companyinfolist= []
    companyinfo=database.collection("Companyinfos").get()
        
    for company in companyinfo:
        data = company.to_dict()
        companyinfolist.append(data)

    context = {
        'companyinfolist':companyinfolist
        }
    return render(request,"contact.html",context)

def addContact(request):
    adsoyad=request.POST.get("namesurname")
    email=request.POST.get("email")
    subject=request.POST.get("subject")
    message=request.POST.get("message")

    data={
        'adsoyad':adsoyad,
        'email':email,
        'subject':subject,
        'message':message
    }

    database.collection("Contact").add(data)
    return redirect("contact")

def checkproduce(request):    
        productlist=[]
        produces=database.collection("Products").get()
        categorylist = []
        categories=database.collection("Categories").get()
        companyinfolist= []
        companyinfo=database.collection("Companyinfos").get()
        
        for company in companyinfo:
            data = company.to_dict()
            companyinfolist.append(data)

    
        for category in categories:
            data = category.to_dict()
            categorylist.append(data)

        for produce in produces:
            if produce.to_dict()["produceStatus"]=="Yayında":
                data=produce.to_dict()
                productlist.append(data)
        
        context = {
        'productlist':productlist,
        'categorylist':categorylist,
        'companyinfolist':companyinfolist

        }
        return render(request,"checkproduce.html",context)

def detailproduce(request):
    productuid=request.GET.get("p")
    
    producelist=[]
    produces=database.collection("Products").where("produceCode","==",productuid).get()
    companyinfolist= []
    companyinfo=database.collection("Companyinfos").get()
        
    for company in companyinfo:
        data = company.to_dict()
        companyinfolist.append(data)

    
    for produce in produces:
        data=produce.to_dict()
        producelist.append(data)


    context = {
        'producelist':producelist,
        'companyinfolist':companyinfolist
    }


    return render(request,"detailproduce.html",context)

dictionary={}
basketlist=[]
dictionary["list"]=basketlist

def addcomment(request):
    producecode=request.POST.get("producecode")
    useremail=request.POST.get("useremail")
    comment=request.POST.get("comment")
    print(producecode)
    print(useremail)
    print(comment)
    return redirect("checkproduce")

def listcategory(request):
    productcategory=request.GET.get("c")
    categories=database.collection("Categories").get()
    produces=database.collection("Products").where("produceCategory","==",productcategory).get()
    companyinfolist= []
    producelist=[]
    companyinfo=database.collection("Companyinfos").get()
    categorylist = []

       

    
    for category in categories:
        data = category.to_dict()
        categorylist.append(data)
        
          
    for company in companyinfo:
        data = company.to_dict()
        companyinfolist.append(data)

    for produce in produces:
        if produce.to_dict()["produceStatus"]=="Yayında":
            data=produce.to_dict()
            producelist.append(data)
    

    
    context = {
        'producelist':producelist,
        'categorylist':categorylist,
        'companyinfolist':companyinfolist
    }

    return render(request,"listcategory.html",context)

def checkout(request):
    return render(request,"checkout.html")


def addBasket(request):
    useremail=request.POST.get("useremail")
    produceCode=request.POST.get("produceCode")
    baskets=database.collection("Baskets").where("useremail","==",useremail).get()
    produces=database.collection("Products").where("produceCode","==",produceCode).get()
    bskttlist=[]
    
    for basket in baskets:
        data=basket.to_dict()
        produces=database.collection("Products").where("produceCode","==",data["produceCode"]).get()
        for produce in produces:
            data2=produce.to_dict()
            producecode=data["produceCode"]
            bskttlist.append(producecode)
    
     
    if(produceCode in bskttlist):
        bskts=database.collection("Baskets").where("useremail","==",useremail).get()

        for bskt in bskts:
            if bskt.to_dict()["produceCode"]==produceCode:
                bs=database.collection("Baskets").where("produceCode","==",produceCode).get()
                for b in bs:
                    if b.to_dict()["useremail"]==useremail:
                        data6=b.to_dict()
                        quantity=data6["quantity"]
                        newquantity=int(quantity+1)
                        key=b.id
                        database.collection("Baskets").document(key).update({"quantity":newquantity})      
    else:
        quantity=1
        data = {
        'useremail':useremail,
        'produceCode':produceCode,
        'quantity':quantity
        }
    
        database.collection("Baskets").add(data)
    return redirect("checkproduce")

def search(request):
    searchword=request.POST.get("searchword")
    companyinfolist= []
    productlist=[]
    companyinfo=database.collection("Companyinfos").get()
    produces=database.collection("Products").get()    
    
    for product in produces:
        if product.to_dict()["produceName"]==searchword:
            data=product.to_dict()
            productlist.append(data)


    for product in produces:
        if product.to_dict()["produceCode"]==searchword:
            data=product.to_dict()
            productlist.append(data)

    for company in companyinfo:
        data = company.to_dict()
        companyinfolist.append(data)
    context={
        'companyinfolist':companyinfolist,
        'productlist':productlist,
        'searchword':searchword
    }

    return render(request,"searchresult.html",context)

def newsubscribe():
    return render(request,"newsubscriber.html")


def uponequantity(request):
    if request.user.is_authenticated:
        useremail=request.POST.get("useremail")
        produceCode=request.POST.get("producecode")
        
        print(useremail)
        print(produceCode)

        bskts=database.collection("Baskets").where("produceCode","==",produceCode).get()

        for bskt in bskts:
            if bskt.to_dict()["useremail"]==useremail:
                bs=database.collection("Baskets").where("useremail","==",useremail).get()
                for b in bs:
                    if b.to_dict()["produceCode"]==produceCode:
                        data6=b.to_dict()
                        quantity=data6["quantity"]
                        newquantity=int(quantity+1)
                        key=b.id
                        database.collection("Baskets").document(key).update({"quantity":newquantity})  
                    
        return redirect("/basket/?b="+request.user.username)
    else:
        useremail=request.POST.get("useremail")
        produceCode=request.POST.get("producecode")
        print(produceCode)
        print(useremail)

        bskts=database.collection("Baskets").where("useremail","==",useremail).get()

        for bskt in bskts:
            if bskt.to_dict()["produceCode"]==produceCode:
                data2=bskt.to_dict()
                quantity=data2["quantity"]
                newquantity=int(quantity+1)
                key=bskt.id
                database.collection("Baskets").document(key).update({"quantity":newquantity})       
        return redirect("/basket/?b="+str(useremail))
def downonequantity(request):
    if request.user.is_authenticated:
        useremail=request.POST.get("useremail")
        produceCode=request.POST.get("producecode")
        
        print(useremail)
        print(produceCode)
        

        bskts=database.collection("Baskets").where("useremail","==",useremail).get()

        for bskt in bskts:
            if bskt.to_dict()["produceCode"]==produceCode:
                bs=database.collection("Baskets").where("produceCode","==",produceCode).get()
                for b in bs:
                    if b.to_dict()["produceCode"]==produceCode:
                        data6=b.to_dict()
                        if data6["useremail"]==useremail:
                            print(data6)
                            quantity=data6["quantity"]
                            newquantity=int(quantity-1)
                            key=b.id
                            if newquantity<=0:
                                pass
                            else:
                                database.collection("Baskets").document(key).update({"quantity":newquantity}) 
            
        context = {
            'useremail':useremail
        }
        return redirect("/basket/?b="+request.user.username)
    else:
        useremail=request.POST.get("useremail")
        produceCode=request.POST.get("producecode")
        baskets=database.collection("Baskets").where("useremail","==",useremail).get()
        print(useremail)
        print(produceCode)
        

        bskts=database.collection("Baskets").where("useremail","==",useremail).get()

        for bskt in bskts:
            if bskt.to_dict()["produceCode"]==produceCode:
                bs=database.collection("Baskets").where("produceCode","==",produceCode).get()
                for b in bs:
                    if b.to_dict()["produceCode"]==produceCode:
                        data6=b.to_dict()
                        quantity=data6["quantity"]
                        newquantity=int(quantity-1)
                        key=b.id
                        if newquantity<=0:
                            pass
                        else:
                            database.collection("Baskets").document(key).update({"quantity":newquantity}) 
        context = {
            'useremail':useremail
        }
        return redirect("/basket/?b="+useremail)
"""
def baskettt(request):
    bsktlist=[]
    prclist=[]
    useremail=request.GET.get("b")
    baskets=database.collection("Baskets").where("useremail","==",useremail).get()
    
    for basket in baskets:
        data=basket.to_dict()
        produceCode=data["produceCode"]
        produces=database.collection("Products").where("produceCode","==",produceCode).get()
        for produce in produces:
            data2=produce.to_dict()
            
            bs=database.collection("Baskets").where("produceCode","==",produceCode).get()
            for b in bs:
                data9=b.to_dict()
                data2["quantity"]=data9["quantity"]
            produceprice=data2["producePrice"]
            data2["totalprice"]=int(data2["quantity"])*int(produceprice)
            prclist.append(int(data2["totalprice"]))
            bsktlist.append(data2)
            
            
   
    totalprice=sum(prclist)
                
    context={
        'bsktlist':bsktlist,
        'totalprice':totalprice,
        'useremail':useremail,
        
    }
    return render(request,"baskett.html",context)


"""
def baskett(request):
    bsktlist=[]
    prclist=[]
    useremail=request.GET.get("b")
    baskets=database.collection("Baskets").where("useremail","==",useremail).get()
    
    for basket in baskets:
        data=basket.to_dict()
        produceCode=data["produceCode"]
        produces=database.collection("Products").where("produceCode","==",produceCode).get()
        for produce in produces:
            data2=produce.to_dict()
            
            bs=database.collection("Baskets").where("produceCode","==",produceCode).get()
            for b in bs:
                data9=b.to_dict()
                data2["quantity"]=data9["quantity"]
            produceprice=data2["producePrice"]
            data2["totalprice"]=int(data2["quantity"])*int(produceprice)
            prclist.append(int(data2["totalprice"]))
            bsktlist.append(data2)
            
            
   
    totalprice=sum(prclist)
                
    context={
        'bsktlist':bsktlist,
        'totalprice':totalprice,
        'useremail':useremail,
        
    }
    return render(request,"baskett.html",context)


def basket(request):
    bsktlist=[]
    prclist=[]
    useremail=request.GET.get("b")
    baskets=database.collection("Baskets").where("useremail","==",useremail).get()
    companyinfolist= []
    companyinfo=database.collection("Companyinfos").get()
        
    for company in companyinfo:
        data = company.to_dict()
        companyinfolist.append(data)

    

    for basket in baskets:
        data=basket.to_dict()
        produceCode=data["produceCode"]
        produces=database.collection("Products").where("produceCode","==",produceCode).get()
        for produce in produces:
            data2=produce.to_dict()
            
            bs=database.collection("Baskets").where("produceCode","==",produceCode).get()
            for b in bs:
                data9=b.to_dict()
                data2["quantity"]=data9["quantity"]
            produceprice=data2["producePrice"]
            data2["totalprice"]=int(data2["quantity"])*int(produceprice)
            prclist.append(int(data2["totalprice"]))
            bsktlist.append(data2)
            
            
   
    totalprice=sum(prclist)
                
    context={
        'bsktlist':bsktlist,
        'totalprice':totalprice,
        'useremail':useremail,
        'companyinfolist':companyinfolist
        
    }
    return render(request,"basket.html",context)






def removeBasket(request):
    if request.user.is_authenticated:
        useremail=request.POST.get("useremail")
        producecode=request.POST.get("producecode")
        baskets=database.collection("Baskets").where("useremail","==",useremail).get()
        for basket in baskets:
            data=basket.to_dict()
            produces=database.collection("Baskets").where("produceCode","==",producecode).get()
            for produce in produces:
                key=produce.id
                database.collection("Baskets").document(key).delete()
        return redirect("/basket/?b="+request.user.username)

    else:
        useremail=request.POST.get("useremail")
        producecode=request.POST.get("producecode")
        baskets=database.collection("Baskets").where("useremail","==",useremail).get()
        for basket in baskets:
            data=basket.to_dict()
            produces=database.collection("Products").where("produceCode","==",producecode).get()
            for produce in produces:
                key=produce.id
                database.collection("Baskets").document(key).delete()
        return redirect("/basket/?b="+useremail)







def clearBasket(request):
    useremail=request.POST.get("useremail")
    baskets=database.collection("Baskets").where("useremail","==",useremail).get()
    for basket in baskets:
        key=basket.id
        database.collection("Baskets").document(key).delete()
    return redirect("basket")


def logout(request):
    if request.method =="POST":
        auth.logout(request)
        return redirect("home")
    return redirect("home")