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


    
]
