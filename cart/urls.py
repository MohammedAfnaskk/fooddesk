from django.urls import path
from .import views

urlpatterns = [
    path('cart/',views.cart, name='cart'),
    path('addtocart/',views.addtocart,name='addtocart'),
    path('update_cart/',views.update_cart,name='update_cart'),
    path('cart/removeFromCart/<int:cart_id>/', views.removeFromCart, name='removeFromCart'),
    path('checkout/',views.checkout,name='checkout'),
    path('place_ordert',views.place_order,name='place_order'),
    path('proceedtopay',views.razarypaycheck,name='proceedtopay'),

    
]