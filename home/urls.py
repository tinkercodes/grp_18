from django.urls import path

from . import views
app_name='home'
urlpatterns = [
	path('', views.home, name='home'),
	path('vrnForm/', views.vrnForm, name='vrnForm'),
	path('vrnformsubmit/', views.vrnform_submit, name='vrnform_submit'),
	# path('challanDetail/', views.challanDetail, name='challandetail'),
	]
	
