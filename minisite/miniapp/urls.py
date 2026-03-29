from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('cart/', views.cart, name='cart'),
    path('add/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('order/', views.place_order, name='place_order'),
    path('orders/', views.orders, name='orders'),
    path('success/', views.success, name='success'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    
]