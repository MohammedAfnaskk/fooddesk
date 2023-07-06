from django.urls import path
from .import views

urlpatterns = [
    path('order_details/',views.order_details, name='order_details'),
    path('view_order/<str:t_no>',views.vieworder, name='orderview'),
    path('ordercancel/<int:order_id>',views.ordercancel,name='ordercancel'),
    path('order_return/<int:order_id>',views.order_return,name='order_return'),

]