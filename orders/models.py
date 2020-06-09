from django.db import models
import json
from django.utils.timezone import now
from django.utils.safestring import mark_safe
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers.data import JsonLexer

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

class Orders(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    detail_json = models.TextField()
    username = models.TextField()
    date = models.DateTimeField(default=now, blank=True)
    done =  models.BooleanField(default=False)

    def detail_json_formatted(self):

        # dump the json with indentation set

        # example for detail_text TextField
        json_obj = json.loads(self.detail_json)
        data = json.dumps(json_obj, indent=2)


        # format it with pygments and highlight it
        formatter = HtmlFormatter(style='colorful')
        response = highlight(data, JsonLexer(), formatter)

         # include the style sheet
        style = "<style>" + formatter.get_style_defs() + "</style><br/>"

        return mark_safe(style + response)

    detail_json_formatted.short_description = 'Details order'
    class Meta:
        managed = True
        db_table = 'orders'
        verbose_name = 'order'
        verbose_name_plural = 'orders'