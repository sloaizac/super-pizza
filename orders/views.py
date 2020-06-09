from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from . import forms
import json
from .models import Main_food, Alternative_food, Menu_item, Alternative_item, Topping, Orders

shopping_lists = {}
order_list = {}

# Create your views here.

#Load menu
def index(request):
    menuType = Main_food.objects.all()
    alternativeType = Alternative_food.objects.all()
    menu = {}
    alternatives = {}
    for item in menuType:
        menuItem =  Menu_item.objects.filter(type=item.id)
        menu[item.name] = menuItem
    for item in alternativeType:
        alternativeItem =  Alternative_item.objects.filter(type=item.id)
        alternatives[item.name] = alternativeItem
    toppings = Topping.objects.all()
    return render(request, 'index.html', {'menu': menu, 'alternatives': alternatives, 'toppings': toppings})

#update shopping list
@csrf_exempt
def updateSL(request):
    if request.method == 'POST':
        user = request.user
        try:
            shopping_lists[user] = json.loads(request.POST['list'])
        except:
            item = request.POST['item']
            try:
                shopping_lists[user] += [item]
            except:
                shopping_lists[user] = [item]
        return HttpResponse('successfully', status=200)
    return Http404('Page not found')

#get shopping list
@csrf_exempt
def getSL(request):
    try:
        return JsonResponse({'list': shopping_lists[request.user]})
    except:
        return JsonResponse({'list': []})


#order
@csrf_exempt
def order(request):
    user = request.user
    if request.method == 'POST':
        order_list[user] = request.POST['list']
        return HttpResponse('successfully', status=200)
    else:
        return render(request, 'order.html')

@csrf_exempt
def getOrder(request):
    return JsonResponse({'list': order_list[request.user]})

@csrf_exempt
def makeOrder(request):
    a = json.loads(order_list[request.user])
    order = Orders.objects.create(username= str(request.user), detail_json= json.dumps({'user': str(request.user), 'order': list(map(change, a))}))
    shopping_lists[request.user] = []
    order_list[request.user] = []
    return redirect('index')

def change(item):
    return json.loads(item)

@csrf_exempt
def myOrders(request):
    orders = Orders.objects.get(username=str(request.user))
    return render(request, 'myorders.html', {'orders': orders})
  
#login, logout, register
def signup(request):
    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = forms.SignUpForm
    return render(request, 'signup.html', {'form': form})

def signin(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return redirect('signin')
    else:
        return render(request, 'signin.html')

def logout_view(request):
    logout(request)
    return redirect(index)