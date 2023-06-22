from django.urls import path
from .import views

urlpatterns = [
    path('order_details/',views.order_details, name='order_details'),
    path('view_order/<str:t_no>',views.vieworder, name='orderview')
    
]