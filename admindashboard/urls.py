from django.urls import path
from .import views

urlpatterns = [
    path('',views.dashboard,name='dashboard'),
    path('userlist/',views.userlist,name='userlist'),
    path('blockuser/<int:user_id>',views.blockuser,name ='blockuser'),
    path('productlist/',views.productlist,name="productlist"),
    path('addproduct/',views.addproduct,name='addproduct'),
    path('editproduct/ <int:prod_id>',views.editproduct,name='editproduct'),
    path('deleteproduct/ <int:prod_id>',views.deleteproduct,name='deleteproduct'),
    path('signout/',views.signout,name='signout'),
    path('orderlist/',views.orderlist,name='orderlist'),
    path('update_status/<int:order_item_id>',views.update_status,name ='update_status'),
    path('categorys/',views.category,name='category'),
    path('addcategory/',views.addcategory,name='addcategory'),
    path('editcategory/<int:editcategory_id>/', views.editcategory, name='editcategory'),
    path('deletecategory/<int:deletecategory_id>',views.deletecategory,name='deletecategory'),
    path('salesreport/',views.salesreport, name="salesreport"),
    path('addproduct_variant/',views.addproduct_variant,name="addproduct_variant"),
    path('edit_variation/<int:variation_id>/', views.edit_variation, name='edit_variation'),
    path('Product_Variant_list/', views.Product_Variant_list, name='Product_Variant_list'),
    path('delete_variation/<int:variation_id>/', views.delete_variation, name='delete_variation'),
    path('addoffer/',views.addoffer, name="addoffer"),
    path('Adminoffer/',views.adminoffer, name="adminoffer"),
    path('editoffer/<int:offer_id>/',views.editoffer, name="editoffer"),
    path('deleteoffer/<int:delete_id>/',views.deleteoffer, name="deleteoffer")





    
]
