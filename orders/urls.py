from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signin/", views.signin, name="signin" ),
    path("signup/", views.signup, name='signup'),
    path("logout/", views.logout_view, name='logout'),
    path("update-sl/", views.updateSL, name='updateSL'),
    path("get-sl/", views.getSL, name='getSL'),
    path("order/", views.order, name='order'),
    path("get-order/", views.getOrder, name='getOrder'),
    path("make-order/", views.makeOrder, name='makeOrder'),
]
