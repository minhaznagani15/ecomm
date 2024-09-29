from django.shortcuts import render,HttpResponse,redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import Product,Cart,Order
from django.db.models import Q
import random
import razorpay
from django.core.mail import send_mail
# Create your views here.

def about(request):
    return HttpResponse("This is About page")

def home(request):
    return HttpResponse("This is Home page")

def contact(request):
    return HttpResponse("This is Contact page")

def edit(request,rid):
    print("Id to be edited:",rid)
    return HttpResponse("Id to be edited "+rid)

def addition(request,x1,x2):
    add=int(x1)+int(x2)
    return HttpResponse("Addition is: "+ str(add))

class SimpleView(View):
    def get(self,request):
        return HttpResponse("Hello from simple View!!")
    
def hello(request):
    context={}
    context['greet']="Good morning,we are learning DTL"
    context['x']=120
    context['y']=100
    context['l']=[10,20,30,40]
    context['products']=[
            {'id':1,'name':'samsung','cat':'mobile','price':5000},
            {'id':3,'name':'woodland','cat':'shoes','price':4500},
            {'id':4,'name':'vivo','cat':'mobile','price':7000}
            ]
    return render(request,'hello.html',context)


#-------Estore project------------
def index(request):
    # userid=request.user.id
    # print(userid)
    # print(request.user.is_authenticated)
    context={}
    p=Product.objects.filter(is_active=True)
    print(p)
    context['products']=p
    return render(request,'index.html',context)

def product_details(request):
    return render(request,'product_details.html')

def register(request):
    if request.method=='POST':
        uname=request.POST['uname']
        upass=request.POST['upass']
        ucpass=request.POST['ucpass']
        # print(uname)
        context={}
        if uname=="" or upass=="" or ucpass=="":
            context['errmsg']= "Fields cannot be Empty!!"
        elif upass != ucpass:
            context['errmsg']= "password and confirm password didn't match!!"
        else:
            try:
                u=User.objects.create(password=upass,username=uname,email=uname)
                u.set_password(upass)
                u.save()
                context['success']= "User Created successfully!!"
            except Exception:
                context['errmsg']="Username already Exists !!!"
        return render(request,'register.html',context)
    #    return HttpResponse('User Created successfully')
    else:
        return render(request,'register.html')
    
def user_login(request):
    if request.method=='POST':
        uname=request.POST['uname']
        upass=request.POST['upass']
        context={}
        if uname=="" or upass=="":
            context['errmsg']="Fields cannot be Empty!!"
        else:
            u=authenticate(username=uname,password=upass)
            print(u)
            if u is not None:
                login(request,u)
                return redirect('/')
        return render(request,'login.html',context)
    else:
        return render(request,'login.html')
    
def user_logout(request):
        logout(request)
        return redirect('/')

def catfilter(request,cv):
    q1=Q(is_active=True)
    q2=Q(cat=cv)
    p=Product.objects.filter(q1 & q2)
    print(p)
    context={}
    context['products']=p
    return render(request,'index.html',context)

def sort(request,sv):
    if sv == '0':
        col='price'
    else:
        col='-price'
    p=Product.objects.filter(is_active=True).order_by(col)
    context={}
    context['products']=p
    return render(request,'index.html',context)

def range(request):
    min=request.GET['min']
    max=request.GET['max']
    # print(min)
    # print(max)
    q1=Q(is_active=True)
    q2=Q(price__gte=min)
    q3=Q(price__lte=max)
    p=Product.objects.filter(q1 & q2 & q3)
    context={}
    context['products']=p
    return render(request,'index.html',context)
    # return HttpResponse('Value fetched')

def product_details(request,pid):
        p=Product.objects.filter(id=pid)
        print(p)
        context={}
        context['products']=p
        return render(request,'product_details.html',context)

def addtocart(request,pid):
    if request.user.is_authenticated:
        userid=request.user.id
        #   print(userid)
        #   print(pid)
        u=User.objects.filter(id=userid)
        p=Product.objects.filter(id=pid)
        q1=Q(uid=u[0])
        q2=Q(pid=p[0])
        c=Cart.objects.filter(q1&q2)
        n=len(c)
        context={}
        context['products']=p
        if n==1:
            context['errmsg']="Product Already Exist in Cart!!!"
        else:
            c=Cart.objects.create(uid=u[0],pid=p[0])
            c.save()
            context['success']="Product Added Successfully to cart!!"
        return render(request,'product_details.html',context)
        # return HttpResponse('Added to cart')
    else:
        return redirect('/login')
    
def viewcart(request):
    c=Cart.objects.filter(uid=request.user.id)
    # print(c)
    # print(c[0])
    # print(c[0].id)
    # print(c[0].uid.username)
    # print(c[0].pid.price)
    # print(c[0].pid.name)
    context={}
    n=len(c)
    s=0
    for x in c:
        # print(x.pid.price)
        s=s+ x.pid.price * x.qty
    context['total']=s
    context['np']=n
    context['data']=c
    return render(request,'cart.html',context)

def remove(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/viewcart')

def updateqty(request,qv,cid):
    c=Cart.objects.filter(id=cid)
    # print(c)
    # print(c[0])
    # print(c[0].qty)
    if qv=='1':
        t=c[0].qty + 1
        c.update(qty=t)
    else:
        if c[0].qty>1:
            t=c[0].qty - 1
            c.update(qty=t)
    return redirect('/viewcart')

def placeorder(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    # print(c)
    oid=random.randrange(1000,9999)
    # print(oid)
    for x in c:
        # print(x)
        # print(x.pid)
        # print(x.uid)
        # print(x.qty)
        o=Order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
        o.save()
        x.delete()
    orders=Order.objects.filter(uid=request.user.id)
    context={}
    context['data']=orders
    np=len(orders)
    s=0
    for x in orders:
        s=s+x.pid.price * x.qty
    context['total']=s
    context['n']=np
    # return HttpResponse('place order successfully')
    return render(request,'placeorder.html',context)

def makepayment(request):
    orders=Order.objects.filter(uid=request.user.id)
    context={}
    s=0
    for x in orders:
        s=s+x.pid.price * x.qty
        oid=x.order_id
    client = razorpay.Client(auth=("rzp_test_pjmfONoAV5hhRJ", "2qLFlWxOv0vaA1jxWEEHwbcA"))
    data = { "amount": s*100, "currency": "INR", "receipt": oid }
    payment = client.order.create(data=data)
    # print(payment)
    context['data']=payment
    context['uemail']=request.user.email
    return render(request,'pay.html',context)
    # return HttpResponse('success')

def sendusermail(request,uemail):
    # uemail=request.user.email
    msg="order details are:"
    send_mail(
    "Ekart Order Placed Successfully",
    msg,
    "minhaznagani@gmail.com",
    [uemail],
    fail_silently=False,
    )
    return HttpResponse('Mail sent Successfully')