from django.shortcuts import render,redirect
import pyrebase
from requests.sessions import session
from django.contrib import auth,messages
import uuid
import firebase_admin
from firebase_admin import credentials,firestore

config = {
  
}

firebase=pyrebase.initialize_app(config)
authe=firebase.auth()
database = firestore.client()
storage = firebase.storage() 








# Create your views here.

def index(request):
    if request.user.is_superuser:
        return render(request,"manage/index.html")
    else:
        return redirect("signinn")

def signin(request):
    return render(request,"manage/signin.html")




def logincontrol(request):
    if request.method=="POST":
        email = request.POST.get('email')
        username=email
        password = request.POST.get('password')

        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request, user)
            print("login başarılı")
            return redirect("manage/index")
        else:
            print("kullanıcı adı veya parola yanlış")
            return redirect("signinn")

def companyinfo(request):
    if request.user.is_superuser:
        companyinfolist=[]
        companyinfo=database.collection("Companyinfos").get()
        
            
        for company in companyinfo:
            data = company.to_dict()
            companyinfolist.append(data)
            
        context = {
            'companyinfolist':companyinfolist,

            }
        return render(request,"manage/companyinfo.html",context)
    else: 
        return redirect("signinn")

def addcategory(request):
    if request.user.is_superuser:
        return render(request,"manage/addcategory.html")
    else:
        return redirect("signinn")
def addCategory(request):
    if request.user.is_superuser:
        categoryname=request.POST.get("categoryname")
        data = {
            'categoryname':categoryname,
            
        }
        
        
    

        database.collection("Categories").add(data)
        return redirect("checkcategory")
    else:
        return redirect("signinn")


def addproduce(request):
    if request.user.is_superuser:
        categorylist=[]
        categories=database.collection("Categories").get()
        
            
        for category in categories:
            data = category.to_dict()
            categorylist.append(data)
            
        context = {
            'categorylist':categorylist,

            }
        return render(request,"manage/addproduce.html",context)
    else: 
        return redirect("signinn")

def addProduce(request):
    if request.method == "POST":
        if request.user.is_superuser:
   
            produceCode=str(uuid.uuid1())
            produceImageURL=request.POST.get('produceImageURL')
            produceCategory=request.POST.get('produceCategory')
            produceStatus=request.POST.get('produceStatus')
            produceName=request.POST.get('produceName')
            produceStock=request.POST.get('produceStock')
            producePrice=int(request.POST.get('producePrice'))
            produceDescription=request.POST.get('produceDescription')

            
            
            
                
            data = {
                        "produceImageURL":produceImageURL,
                        "produceCategory":produceCategory,
                        'produceStatus':produceStatus,
                        "produceCode":produceCode,
                        "produceName":produceName,
                        "produceStock":produceStock,
                        "producePrice":producePrice,
                        "produceDescription":produceDescription
                        
                        

                    }

            database.collection("Products").add(data)
            return redirect("checkproduce")
        else:
            return redirect("signinn")

def checkproduce(request):
    if request.user.is_superuser:
        productlist=[]
        produces=database.collection("Products").get()
        
        for produce in produces:
            data = produce.to_dict()
            productlist.append(data)
        
        context = {
        'productlist':productlist,

        }
        return render(request,"manage/checkproduce.html",context)
    else:
        return redirect("signinn")
def contactforms(request):
    contactlist=[]
    contacts=database.collection("Contacts").get()
        
    for contact in contacts:
        data = contact.to_dict()
        contactlist.append(data)
        
    context = {
        'contactlist':contactlist,

        }
    return render(request,"manage/contactforms.html",context)
def updateproduce(request):
    if request.method=="POST":
        if request.user.is_superuser:
            producecode=request.POST.get('producecode')
            produceimage=request.POST.get('produceimage')
            producecategory=request.POST.get('producecategory')
            producename=request.POST.get('producename')
            producestock=request.POST.get('producestock')
            produceprice=request.POST.get('produceprice')
            producedescription=request.POST.get('producedescription')
            categorylist = []
            categories=database.collection("Categories").get()

        
            for category in categories:
                data = category.to_dict()
                categorylist.append(data)

            context = {
                'producecode':producecode,
                'produceimage':produceimage,
                'producecategory':producecategory,
                'producename':producename,
                'producestock':producestock,
                'produceprice':produceprice,
                'producedescription':producedescription,
                'categorylist':categorylist
            }
            return render(request,"manage/updateproduce.html",context)
        else:
            return redirect("signinn")

def updateProduce(request):
    if request.method=="POST":
        if request.user.is_superuser:
            producecode=request.POST.get('producecode')
            newproduceimage=request.POST.get('newproduceimage')
            newproducecategory=request.POST.get('newproducecategory')
            newproduceName=request.POST.get('newproducename')
            newproducestock=request.POST.get('newproducestock')
            newproduceprice=request.POST.get('newproduceprice')
            newproducedescription=request.POST.get('newproducedescription')
            
            produces=database.collection("Products").where("produceCode","==",producecode).get()

        
            for product in produces:
                if product.to_dict()["produceCode"]==producecode:
                    key=product.id
                    database.collection("Products").document(key).update({"produceImageURL":newproduceimage})
                    database.collection("Products").document(key).update({"produceName":newproduceName})
                    database.collection("Products").document(key).update({"produceStock":newproducestock})
                    database.collection("Products").document(key).update({"producePrice":newproduceprice})
                    database.collection("Products").document(key).update({"produceDescription":newproducedescription})
                    database.collection("Products").document(key).update({"produceCategory":newproducecategory})
                    return redirect("checkproduceadmin")
        else:
            return redirect("signinn")
    


def checkcategory(request):
    if request.user.is_superuser:
        categorylist = []
        categories=database.collection("Categories").get()

        
        for category in categories:
            data = category.to_dict()
            categorylist.append(data)
        

        context = {
        'categorylist':categorylist,

        }
        return render(request,"manage/checkcategory.html",context)
    else:
        return redirect("signinn")


def updatecategory(request):
    if request.user.is_superuser:
        categoryname=request.POST.get('categoryname')
        categorylist=[]
        categories=database.collection("Categories").where("categoryname","==",categoryname).get()

        for category in categories:
            data = category.to_dict()
            categorylist.append(data)
        

        context = {
        'categorylist':categorylist,

        }

        return render(request,"manage/updatecategory.html",context)
    else:
        return redirect("signinn")

def updateCategory(request):
    if request.method=="POST":
        if request.user.is_superuser:
            newcategoryname=request.POST.get('newcategoryname')
            categoryname=request.POST.get('categoryname')
            
            categories=database.collection("Categories").where("categoryname","==",categoryname).get()

            for category in categories:
                if category.to_dict()["categoryname"]==categoryname:
                    key=category.id
                    database.collection("Categories").document(key).update({"categoryname":newcategoryname})
            return redirect("checkcategory")
        else:
            return redirect("signinn")

def deletecategory(request):
    if request.method=="POST":
        if request.user.is_superuser:
            categoryname=request.POST.get('categoryname')

            context = {
                'categoryname':categoryname
            }

            return render(request,"manage/deletecategory.html",context)
        else:
            return redirect("signinn")

def deleteCategory(request):
    if request.method=="POST":
        if request.user.is_superuser:
            categoryname=request.POST.get('categoryname')
            categories=database.collection("Categories").where("categoryname","==",categoryname).get()

            for category in categories:
                if category.to_dict()["categoryname"]==categoryname:
                    key=category.id
                    database.collection("Categories").document(key).delete()

            return redirect("checkcategory")
        else:
            return redirect("signinn")    

def checkuser(request):
    if request.user.is_superuser:
        userlist = []
        users=database.collection("Users").get()

        
        for user in users:
            data = user.to_dict()
            userlist.append(data)
        

        context = {
        'userlist':userlist,

        }
        return render(request,"manage/checkuser.html",context)
    else:
        return redirect("signinn")


