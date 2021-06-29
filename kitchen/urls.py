"""feastfreedom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views

from . import views
from kitchen.views import CustomerDetailView, CustomerUpdateView, CustomerDeleteView
app_name = 'kitchen'

urlpatterns = [
    #path('', HomePageView.as_view(), name='home'),
    path('', views.home.as_view(), name='home'),
    path('kitchen/', views.ProviderKitchenListView.as_view(), name='index'),
    path('kitchen/create/', views.KitchenCreateView, name='kitchen_create'),
    path('kitchen/<pk>/', views.KitchenDetailView.as_view(), name='kitchen_detail'),
    path('check/', views.check, name='check'),
    #path('', KitchenListView.as_view(), name='index'),
    path('providerkitchen/<pk>/', views.ProviderKitchenDetailView, name='provider_kitchen_detail'),
    path('kitchen/<pk>/update/', views.KitchenUpdateView.as_view(), name='kitchen_update'),
    path('kitchen/<pk>/delete/', views.KitchenDeleteView.as_view(), name='kitchen_confirm_delete'),
    # path('kitchen/<pk>/food/create', views.FoodCreateView, name='food_create'),
    # path('food/<pk>', views.FoodDetailView.as_view(), name='food_detail'),
    # path('kitchen/<kpk>/food/<fpk>/delete', views.FoodDeleteView, name='food_confirm_delete'),
    # path('kitchen/<kpk>/food/<fpk>/update', views.FoodUpdateView, name='food_update'),

    path('accounts/login/', auth_views.LoginView.as_view(template_name="registration/login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name="registration/logout.html"), name='logout'),

    # path('accounts/profile/', views.profile, name='profile'),
    path('accounts/profile/', views.profile, name='profile'),


    path('ordercreate', views.OrderCreate, name='order_create'),
    path('ordersuccess', views.OrderSuccess, name='order_success'),

    path('cartdetail', views.CartDetail, name='cart_detail'),
    path('cartadd/<pk>', views.CartAdd, name='cart_add'),
    path('cartremove/<pk>', views.CartRemove, name='cart_remove'),

    # re_path(r'^register/$', views.register, name='register'),

    re_path(r'^register/$', views.CustomerCreateView.new_customer, name='new_customer'),

    path('customer/<pk>', CustomerDetailView.as_view(), name='customer_detail'),
    path('customer/<pk>/update', CustomerUpdateView.as_view(), name='customer_update'),
    path('customer/<pk>/delete', CustomerDeleteView.as_view(), name='customer_delete'),


]
