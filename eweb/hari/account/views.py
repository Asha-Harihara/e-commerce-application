
import json
from math import prod
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from .form import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.http import JsonResponse
def registerPage(request):
    if request.user.is_authenticated:
       return redirect('home')
     
    form=CreateUserForm()
    
    if request.method=='POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user=form.cleaned_data.get('username')
            messages.success(request, 'Account was created for '+user)
            return redirect('login')

    context={'form':form}
    return render(request, 'register.html', context)

def loginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect')
          
    context={}
    return render(request, 'login.html', context)

def logoutUser(request):
   logout(request)
   return redirect('login')

login_required(login_url='login')
def home(request):
    if not request.user.is_authenticated:
       return redirect('login') 
    return render(request,'home.html')

login_required(login_url='login')
def sellhome(request):
    if not request.user.is_authenticated:
       return redirect('login') 
    
    return render(request,'sellhome.html')


login_required(login_url='login')
def buyhome(request):
    if not request.user.is_authenticated:
       return redirect('login') 
    products=Product.objects.all()
    tags=Tags.objects.all()
    context={'products':products, 'tags':tags}
    return render(request,'buyhome.html', context)


def cart(request):
    if not request.user.is_authenticated:
       return redirect('login') 

        
    currcart=PresentCart.objects.filter(buyer=request.user)
    cart_total=sum([c.get_total for c in currcart])
    context={'currcart':currcart, 'cart_total':cart_total}
    return render(request,'cart.html', context)

def orders(request):
    if not request.user.is_authenticated:
        return redirect('login')
    orderitems=OrderedItems.objects.filter(order__buyer=request.user)
    context={'order': orderitems}
    return render(request, 'orders.html', context)

def checkout(request):
    if not request.user.is_authenticated:
        return redirect('login')
    shippingid=-1
    currcart=PresentCart.objects.filter(buyer=request.user)
    cart_total=sum([c.get_total for c in currcart])
    if request.method=='POST':
        apart=request.POST.get('address')
        pincode=request.POST.get('pincode')
        area=request.POST.get('area')
        city=request.POST.get('city')
        state=request.POST.get('state')
        country=request.POST.get('country')
        shippingAdress, created=Adress.objects.get_or_create(apartment=apart, pincode=pincode, area=area, city=city, state=state, country=country)
        shippingAdress.save()
        shippingid=shippingAdress.id
        context={'currcart':currcart, 'cart_total':cart_total, 'sid':shippingid, 'shippi':shippingAdress}
        return render(request, 'checkout.html', context)
    
    context={'currcart':currcart, 'cart_total':cart_total, 'sid':shippingid}
    return render(request, 'checkout.html', context)

def updateItem(request):
    data=json.loads(request.body)
    productId=data['productId']
    action=data['action']
    print('Action:', action)
    print('Prodct', productId)

    user=request.user
    product=Product.objects.get(id=productId)
    
    # currcart,blah=PresentCart.objects.get_or_create(buyer=user, product=product)
   # currcart=PresentCart.objects.filter(buyer=user, product=product).first()
    #if currcart is None:
     #   currcart=PresentCart.objects.create(buyer=user, product=product)
        #currcart.save()
    currcart,p=PresentCart.objects.get_or_create(buyer=user, product=product)
    if action=='add':
          if currcart.quantity+1<=product.quantity:
            currcart.quantity=(currcart.quantity+1)
    elif action=='remove':
          currcart.quantity=(currcart.quantity-1)
        
    currcart.save()

    if currcart.quantity<=0:
        currcart.delete()
    return JsonResponse('Item was added', safe=False)


def orderItems(request):
    data=json.loads(request.body)
    shippingid=data['shippid']
    user=request.user
    #print('shipping id', shippingid)
    shippingadd=Adress.objects.get(id=shippingid)
    #create order object first
    newOrder=Order(buyer=user, delivery_address=shippingadd)
    newOrder.save()
    currcart=PresentCart.objects.filter(buyer=request.user)
    for x in currcart: 
       item=OrderedItems(product=x.product, order=newOrder, quantity=x.quantity)
       item.save()
       x.product.quantity-=x.quantity
       x.product.save()
       PresentCart.objects.filter(id=x.id).delete()
    
    return JsonResponse('Order is ordered', safe=False)


def viewurprod(request):
    if not request.user.is_authenticated:
        return redirect('login')
    products=Product.objects.filter(seller=request.user)
    context={'urpro':products}
    return render(request, 'viewurprod.html', context)


def updateQuant(request):
    data=json.loads(request.body)
    productId=data['productId']
    action=data['action']
    print('Action:', action)
    print('Prodct', productId)

    user=request.user
    product=Product.objects.get(id=productId)
    
    if action=='add':
          product.quantity+=1
    elif action=='remove':
          if(product.quantity>0):
           product.quantity-=1
        
    product.save()

    return JsonResponse('Item was added', safe=False)



def viewurorder(request):
    if not request.user.is_authenticated:
        return redirect('login')
    orders=OrderedItems.objects.filter(product__seller=request.user, order__completed=False).exclude(status="DELIVERED")
    context={'orders':orders}
    return render(request, 'viewurorder.html', context)


def updateStatus(request):
    data=json.loads(request.body)
    productId=data['productId']
    action=data['action']
    print('Action:', action)
    print('Prodct', productId)

   
    product=OrderedItems.objects.get(id=productId)
    
    if action=='pending':
          product.status="PENDING"
    elif action=='delivery':
           product.status="DELIVERED"
    elif action=="out":
           product.status="OUT FOR DELIVERY"
    product.save()

    return JsonResponse('Item was added', safe=False)


def addproduct(request):
    
    context=None
    if request.method=='POST':
        apart=request.POST.get('address')
        pincode=request.POST.get('pincode')
        area=request.POST.get('area')
        city=request.POST.get('city')
        state=request.POST.get('state')
        country=request.POST.get('country')
        shippingAdress, created=Adress.objects.get_or_create(apartment=apart, pincode=pincode, area=area, city=city, state=state, country=country)
        shippingAdress.save()
        name=request.POST.get('name')
        price=request.POST.get('price')
        seller=request.user
        quantity=request.POST.get('quantity')
        shop=shippingAdress
        image=request.FILES['image']
        
        product=Product(name=name, price=price, seller=seller, quantity=quantity, shop=shop, image=image)
        product.save()

        return render(request, 'viewurprod.html')

    return render(request, 'addprod.html')   