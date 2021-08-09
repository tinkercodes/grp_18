from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as Login,logout as Logout
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from .models import checkpost, vehicle_info, defaulter, closed_cases, staff
from django.utils import timezone
from . import forms
from binascii import hexlify
import os
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
	ctx={}
	return render(request,'home/index.html',ctx)


@login_required(login_url='/staffLogin/')
def register_checkpost(request):
	err_msg = ''
	if(request.user.has_perm('home.add_checkpost')):
		if(request.method=='POST'):
			form = forms.check_post_form(request.POST)
			if(form.is_valid()):
				key = hexlify(os.urandom(15)).decode()
				cp_id = hexlify(os.urandom(5)).decode()
				cp = checkpost(state=form.cleaned_data['state'],
					district=form.cleaned_data['state'],
					place = form.cleaned_data['place'],
					postCode = form.cleaned_data['pincode'],
					api_key = key,
					post_id = cp_id
					)
				cp.save()
				return render(request,'home/show_api_key.html',{'api_key':key,'post_id':cp_id})
			else:
				return render(request,'home/checkpost_form',{'form':form})
		else:
			form = forms.check_post_form()
			return render(request,'home/checkpost_form.html',{'form':form})
	else:
		form = forms.user_login_form()
		err_msg = 'You are not Authorized to add Check-Posts, Enter with a superuser account'
		return render(request,'home/staff_login.html',{'form':form,'err_msg':err_msg})

def login_checkpost(request):
	err_msg = ''
	if(request.method=='POST'):
		form = forms.check_post_login_form(request.POST)
		if(form.is_valid()):
			if(checkpost.objects.filter(state=form.cleaned_data['state'],
				district=form.cleaned_data['district'],
				postCode = form.cleaned_data['pincode'],
				post_id = form.cleaned_data['check_post_id']
				).count()>0):
				dfltr_list = defaulter.objects.filter(checkpost_id=checkpost.objects.get(post_id = form.cleaned_data['check_post_id']))
				closed_cases_list = closed_cases.objects.filter(checkpost_id=checkpost.objects.get(post_id = form.cleaned_data['check_post_id']))

				return render(request,'home/checkpost_details.html',{'dfltr_list':dfltr_list,'closed_cases_list':closed_cases_list})
			else:
				err_msg='No checkpost found for the input combination'
				return render(request,'home/checkpost_login_form.html',{'form':form,'err_msg':err_msg})
		else:
			return render(request,'home/checkpost_login_form.html',{'form':form})
	else:
		form = forms.check_post_login_form()
		return render(request,'home/checkpost_login_form.html',{'form':form,'err_msg':err_msg})

def validate_vrn(vrn):
	if(len!=10):
		return "Enter 10-digit Vehicle registration No."
	else:
		return True

def vrnForm(request):
	ctx={'error_msg':""}
	return render(request,'home/vrnform.html',ctx)

def vrnform_submit(request):
	ctx={'error_msg':""}
	if(request.method=="POST"):
		vrn=request.POST['VRN']
		if(len(vrn)!=10):
			ctx['error_msg']="Enter your 10-digit Vehicle registration No."
			ctx['vrn']=vrn
			return render(request,'home/vrnform.html',ctx)
		else:
			ctx['vrn']=vrn
			ctx['isData']=False
			if(defaulter.objects.filter(vrn_id=vehicle_info.objects.filter(vrn=vrn)[0]).count()>0):
				d=defaulter.objects.get(vrn_id=vehicle_info.objects.filter(vrn=vrn)[0])
				ctx['isData']=True
				ctx['owner']=vehicle_info.objects.filter(vrn=vrn)[0].reg_owner
				ctx['rulecat']=d.get_rule_cat_id_display()
				cp = checkpost.objects.get(post_id=d.checkpost_id)
				ctx['place']= str(cp.place) +' '+ str(cp.get_district_display()) +' '+ str(cp.get_state_display()) +' '+ str(cp.postCode)
				ctx['time']=d.date_time

				return render(request,'home/challandetail.html',ctx)
			else:

				return render(request,'home/challandetail.html',ctx)
	else:
		return render(request,'home/vrnform.html',ctx)


def staff_login(request):
	err_msg = ''
	if(request.method=="POST"):
		form = forms.user_login_form(request.POST)
		if(form.is_valid()):
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']
			try:
				username=User.objects.filter(email=email)[0].username
			except:
				err_msg='No account associated with this email'
				return render(request, 'home/staff_login.html',{'form':form,'err_msg':err_msg})
			user = authenticate(request, username=username, password=password)
			if user is not None:
				Login(request,user)
				 	# Redirect to a success page.
				# HttpResponseRedirect(url('home:index'))
				return HttpResponseRedirect('/')
			else:
				# Return an 'invalid login' error message.
				print(9999999999999999999999)
				return render(request,'home/staff_login.html',{'form':form})
		else:
			print(7777777777777777)
			return render(request,'home/staff_login.html',{'form':form})
	else:
		print(222222222222222222222222)
		if(request.user.is_authenticated):
			err_msg = 'Currently you are logged in as {}.'.format(request.user.username)
		if(request.GET.get('next')=='/registerCheckpost/'):
			err_msg = 'To register a check post, login with superuser account.'
		form = forms.user_login_form()
		return render(request, 'home/staff_login.html',{'form':form,'err_msg':err_msg})



def staff_registration(request):
	err_msg = ''
	if(request.method=='POST'):
		form = forms.user_registration_form(request.POST)
		if(form.is_valid()):
			if(checkpost.objects.filter(post_id = form.cleaned_data['check_post_id']).count()>0):
				user = User.objects.create_user(first_name=form.cleaned_data['first_name'],
						last_name=form.cleaned_data['last_name'],
						email=form.cleaned_data['email'],
						username = str(form.cleaned_data['first_name'])+' '+str(form.cleaned_data['last_name']),
						password=form.cleaned_data['password'])
				staff.objects.create(name = user,
				checkpost = checkpost.objects.get(post_id=form.cleaned_data['check_post_id'])
				)
				Login(request,user)
				return HttpResponseRedirect('/')
			else:
				err_msg = 'Post Id entered is not valid'
				return render(request,'home/staff_register.html',{'form':form,'err_msg':err_msg})
		else:
			return render(request,'home/staff_register.html',{'form':form})
	else:
		disable = ''
		if(request.user.is_authenticated):

			err_msg = 'Currently you are logged in as {}.'.format(request.user.username)
			disable = 'disabled'
		form = forms.user_registration_form()
		return render(request,'home/staff_register.html',{'form':form,'err_msg':err_msg,'disable':disable})

def staff_logout(request):
	Logout(request)
	return HttpResponseRedirect('/')
