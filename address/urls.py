from django.urls import path
from .import views

urlpatterns = [
    path('userprofile/',views.userprofile,name='userprofile'),
    path('add_address/',views.add_address,name='add_address'),
    path('update_address/<int:adrs_id>',views.update_address,name='update_address'),
    path('deleteAddress/<int:address_id>',views.delete_address,name='deleteAddress'),
    path('change_password/',views.change_password,name='change_password'),
    path('add_address_checkout/',views.add_address_checkout,name='add_address_checkout'),
    path('update_address_checkout/<int:adrs_id>',views.update_address_checkout,name="update_address_checkout")

    
    
]
