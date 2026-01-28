from django.contrib import admin
from django.urls import path
from hii import views

urlpatterns = [
    path("",views.index,name="hii"),
    path("about",views.about,name="about"),
    path("shop",views.shop,name="shop"),
    path("contact",views.contact,name="contact"),
    path("product/<int:pk>",views.product,name="product"),

    

]