from django.db import models

# Create your models here.

class Main_food(models.Model): # Pizza, dinners, subs, etc
    id = models.AutoField(auto_created = True, primary_key = True)
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name

class Alternative_food(models.Model): # Salads, pasta, etc
    id = models.AutoField(auto_created = True, primary_key = True)
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name

class Menu_item(models.Model):
    type = models.ForeignKey(Main_food, on_delete=models.CASCADE)
    features = models.CharField(max_length=64)
    small_price = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    large_price = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

class Alternative_item(models.Model):
    type = models.ForeignKey(Alternative_food, on_delete=models.CASCADE)
    description = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=5, decimal_places=2)

class Topping(models.Model):
    id = models.AutoField(auto_created = True, primary_key = True)
    description = models.CharField(max_length=20)