from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('login',views.login,name="login"),
    path('getlocation',views.getlocation,name="location"),
    path('predict',views.predict,name="predict"),
    path('signup', views.userSignUp,name="signup"),
    path('regression',views.regression, name='regression'),
    path('resetpassword',views.ResetPassword, name='resetpassword')

]