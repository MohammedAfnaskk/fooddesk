from django.urls import path ,include
from .import views

urlpatterns = [
    path('',views.login,name='login'),
    path('signup',views.signup,name='signup'),
    path('logout/',views.logout,name='logout'),
    path('signin/',views.signin,name='signin'),
    path('signupadmin/',views.signupadmin,name='signupadmin'),
     path('forgotpassword/',views.forgot_password,name="forgotpassword"),

]