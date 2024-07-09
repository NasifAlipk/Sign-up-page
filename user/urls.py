from django.contrib import admin
from django.urls import path
from user import views

urlpatterns = [
    path('', views.LoginPage, name='login'),
    path('signup/', views.SignupPage, name='signup'),
    path('home/', views.HomePage, name='home'),
    path('logout/', views.LogoutPage, name='logout'),
    path('index/', views.AdminPage, name='index'),
    path('add', views.AddUser,name='add'),
    path('edit', views.EditUser,name='edit'),
    path('update/<int:id>/',views.UpdateUser, name='update'),
    path('deleteinfo', views.DeleteUserInfo, name="deleteinfo"),
    path('delete/<int:id>/',views.DeleteUser, name="delete"),
    path('adminlogin/', views.AdminLogin, name='adminlogin'),
]