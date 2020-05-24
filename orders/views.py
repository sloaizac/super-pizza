from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from . import forms
from .models import Main_food, Alternative_food, Menu_item, Alternative_item, Topping

# Temporal shopping lists

shopping_lists = {}

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

#shopping car
@csrf_exempt
def addItem(request):
    if request.method == 'POST':
        item = request.POST['item']
        user = request.user
        try:
            shopping_lists[user] += [item]
        except:
            shopping_lists[user] = [item]
        return HttpResponse('successfully', status=200)
    return Http404('Page not found')

@csrf_exempt
def getShoppingList(request):
    if request.method == 'POST':
        user = request.user
        try:
            return JsonResponse({'response': shopping_lists[user]})
        except:
            return HttpResponse('No tiene pedidos', status=403)
    return Http404('Page not found')


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