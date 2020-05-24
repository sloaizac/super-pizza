from django.contrib import admin
from .models import Main_food, Alternative_food, Menu_item, Alternative_item, Topping

# Register your models here.

class Main_food_Admin(admin.ModelAdmin):
    list_display = ('id','name', 'description')
admin.site.register(Main_food, Main_food_Admin)

class Alternative_food_Admin(admin.ModelAdmin):
    list_display = ('id','name', 'description')
admin.site.register(Alternative_food, Alternative_food_Admin)

class Alternative_item_Admin(admin.ModelAdmin):
    list_display = ('id', 'type', 'description', 'price')
admin.site.register(Alternative_item, Alternative_item_Admin)

class Main_item_Admin(admin.ModelAdmin):
    list_display = ('id', 'type', 'features', 'small_price', 'large_price')
admin.site.register(Menu_item, Main_item_Admin)

class Topping_Admin(admin.ModelAdmin):
    list_display = ('id', 'description')
admin.site.register(Topping, Topping_Admin)
