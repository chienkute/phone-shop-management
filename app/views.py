from django.shortcuts import render,redirect

from django.http import JsonResponse
from .models import *
import json
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.db.models import Sum
from django.core.paginator import Paginator



def search(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        keys = Product.objects.filter(name__contains = searched)
        paginator = Paginator(keys, 9)
        page = request.GET.get('page')
        product_list = paginator.get_page(page)
    categories = Category.objects.all()
    return render(request, 'app/search.html',{"searched":searched,"keys":keys,'product_list':product_list,"categories":categories})

def category(request):
    categories = Category.objects.all()
    # lấy giá trị tham số từ URL
    active_category = request.GET.get('category','')
    products = Product.objects.none()
    if request.user.is_authenticated:
        order_items = OrderItem.objects.filter(order__customer=request.user, order__complete=False)
        # tính tổng số lượng sản phẩm
        total_items = order_items.aggregate(Sum('quantity'))['quantity__sum']
        if total_items is not None:
            total_items = int(total_items)
        else:
            total_items = 0
    else:
        total_items = 0
    min_price = request.GET.get('min_price',100)
    max_price = request.GET.get('max_price',1000000)
    if active_category:
        products = Product.objects.filter(category__slug = active_category)
        paginator = Paginator(products, 9)
        # lấy tham số page từ url xác định trang htai
        page = request.GET.get('page')
        # lấy danh sách sản phẩm trang hiện tại
        product_list = paginator.get_page(page)
    else :
        products = Product.objects.filter(price__gte=min_price, price__lte=max_price) 
        paginator = Paginator(products, 9)
        page = request.GET.get('page')
        product_list = paginator.get_page(page)
    if request.method == "POST":
        searched = request.POST["searched"]
        products = Product.objects.filter(name__contains = searched)
        paginator = Paginator(products, 9)
        page = request.GET.get('page')
        product_list = paginator.get_page(page)
    context = {'categories' : categories,'products' : products,'active_category' : active_category,'total_items':total_items,'product_list':product_list}
    return render(request, 'app/category.html',context)

def home(request):
    if request.user.is_authenticated:
        order_items = OrderItem.objects.filter(order__customer=request.user, order__complete=False)
        total_items = order_items.aggregate(Sum('quantity'))['quantity__sum']

        if total_items is not None:
            total_items = int(total_items)
        else:
            total_items = 0
    else:
        total_items = 0
    categories = Category.objects.all()
    total_products = Product.objects.count()
    products = Product.objects.all()
    paginator = Paginator(products, 9)
    page = request.GET.get('page')
    product_list = paginator.get_page(page)
    context = {'products' : products,'total_products':total_products,'categories':categories,'total_items' : total_items,'product_list':product_list}
    return render(request, 'app/home.html',context)

def place_order(request):
    if request.user.is_authenticated:
        items = OrderItem.objects.filter(order__customer=request.user, order__complete=False)
        total_items = items.aggregate(Sum('quantity'))['quantity__sum']
        total = sum([item.get_total for item in items])
        totals = total - 10
        if total_items is not None:
            total_items = int(total_items)
        else:
            total_items = 0
    else:
        total_items = 0
        total = 0
        totals = 0
    order = Order.objects.all()
    context = {'items':items,'order':order,'total_items':total_items,'total':total,'totals':totals}
    return render(request, 'app/place-order.html',context)
def order_complete(request):
    if request.user.is_authenticated:
        order = Order.objects.filter(customer = request.user,complete=False)
        items = OrderItem.objects.filter(order__customer = request.user,order__complete = False)
        total_items = items.aggregate(Sum('quantity'))['quantity__sum']
        total = sum([item.get_total for item in items])
        totals = total - 10
        if total_items is not None:
            total_items = int(total_items)
        else:
            total_items = 0
    else:
        total_items = 0
        total = 0
        totals = 0
    context = {"items":items,"total_items":total_items,"total":total,"totals":totals,"order":order}
    return render(request, 'app/order_complete.html',context)
def detail(request, id):
    if request.user.is_authenticated:
        order_items = OrderItem.objects.filter(order__customer=request.user, order__complete=False)
        total_items = order_items.aggregate(Sum('quantity'))['quantity__sum']
        if total_items is not None:
            total_items = int(total_items)
        else:
            total_items = 0
    else:
        total_items = 0
    product = Product.objects.get(pk=id)
    return render(request, 'app/product-detail.html', {'product': product,'total_items':total_items})

def navbar(request):
    if request.user.is_authenticated:
        order_items = OrderItem.objects.filter(order__customer=request.user, order__complete=False)
        total_items = order_items.aggregate(Sum('quantity'))['quantity__sum']

        if total_items is not None:
            total_items = int(total_items)
        else:
            total_items = 0
    else:
        total_items = 0
    return render(request, 'app/includes/navbar.html',{'total_items':total_items})
def sign_in(request):
    if request.user.is_authenticated:
        order_items = OrderItem.objects.filter(order__customer=request.user, order__complete=False)
        total_items = order_items.aggregate(Sum('quantity'))['quantity__sum']
        if total_items is not None:
            total_items = int(total_items)
        else:
            total_items = 0
    else:
        total_items = 0
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else: messages.info(request,'User or Password not correct!')
    context = {'total_items':total_items}
    return render(request, 'app/account/sign_in.html',context)
def register(request):
    if request.user.is_authenticated:
        order_items = OrderItem.objects.filter(order__customer=request.user, order__complete=False)
        total_items = order_items.aggregate(Sum('quantity'))['quantity__sum']
        if total_items is not None:
            total_items = int(total_items)
        else:
            total_items = 0
    else:
        total_items = 0
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sign_in')
    context = {'form':form,'total_items':total_items}
    return render(request, 'app/account/register.html',context)
def logoutPage(request):
    logout(request)
    return redirect('sign_in')
def cart(request):
    items = OrderItem.objects.all()
    if request.user.is_authenticated:
        items = OrderItem.objects.filter(order__customer=request.user, order__complete=False)
        total_items = items.aggregate(Sum('quantity'))['quantity__sum']
        total = sum([item.get_total for item in items])
        totals = total - 10
        if total_items is not None:
            total_items = int(total_items)
        else:
            total_items = 0
    else:
        total_items = 0
        total = 0
        totals = 0
    context = {'items':items,'total_items':total_items,'total':total,'totals':totals}
    return render(request, 'app/order/cart.html',context)
def updateItem(request):
    # truy vấn body và lưu vào biến data
    data = json.loads(request.body)
    # trích xuất giá trị từ data
    productId = data['productId']
    action = data['action']
    customer = request.user
    product = Product.objects.get(id = productId)
    order,created = Order.objects.get_or_create(customer=customer,complete=False)
    orderItem,created = OrderItem.objects.get_or_create(order=order,product=product)
    if action == 'add':
        orderItem.quantity +=1
    elif action == 'remove':
        orderItem.quantity -=1
    orderItem.save()
    if orderItem.quantity<=0:
        orderItem.delete()
    # Trả về một HTTP response dưới dạng JSON để thông báo cho phía máy khách (client) rằng sản phẩm đã được cập nhật thành công.
    return JsonResponse('added',safe=False)
def payment_success(request):
    if request.user.is_authenticated:   
        order = Order.objects.get(customer=request.user, complete=False)
        order.complete = True
        order.save()

    return redirect('home')
def history(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(customer = request.user,complete=True)
        order_item = OrderItem.objects.filter(order__customer=request.user, order__complete=True)
        total = sum([item.get_total for item in order_item])
        totals = total + 56
        order_items = OrderItem.objects.filter(order__customer=request.user, order__complete=False)
        total_items = order_items.aggregate(Sum('quantity'))['quantity__sum']
        if total_items is not None:
            total_items = int(total_items)
        else:
            total_items = 0
    else:
        total_items = 0
        totals = 0
        total = 0

    context = {"order_item":order_item,"orders":orders,"total_items":total_items,"totals":totals,"total":total}
    return render(request, 'app/history.html',context)

