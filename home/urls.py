from django.urls import path

from . import views
app_name='home'
urlpatterns = [
	path('', views.home, name='home'),
	path('vrnForm/', views.vrnForm, name='vrnForm'),
	path('vrnformsubmit/', views.vrnform_submit, name='vrnform_submit'),
	path('registerCheckpost/', views.register_checkpost, name='register_checkpost'),
	path('loginCheckpost/', views.login_checkpost, name='login_checkpost'),
	path('staffLogin/', views.staff_login, name='staff_login'),
	path('staffRegistration/', views.staff_registration, name='staff_registration'),
	path('staffLogout/', views.staff_logout, name='staff_logout'),
	]
	
