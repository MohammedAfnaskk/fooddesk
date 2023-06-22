from django.urls import path
from .import views

urlpatterns = [
    path('',views.home,name='home'),
    path('shop/',views.shop,name='shop'),
    path('singleproduct/<int:single_id>',views.single_product,name='singleproduct'),
    path('wishlist/',views.wishlist,name="wishlist"),
    path('add_to_wishlist/',views.add_to_wishlist,name='add_to_wishlist'),
    path('delete_wishlist_item/',views.delete_wishlist_item,name='delete_wishlist_item'),
    path('shop/search/',views.search,name ="search"),
    
 
]
        