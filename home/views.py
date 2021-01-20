from django.shortcuts import render
from django.urls import reverse 
from django.http import HttpResponse, HttpResponseRedirect
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as Login,logout as Logout
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from .models import defaulter,vehicleInfo
from django.utils import timezone

# Create your views here.
def home(request):
	ctx={}
	return render(request,'home/index.html',ctx)

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
			if(defaulter.objects.filter(vrn=vrn).count()>0):
				d=defaulter.objects.get(vrn=vrn)
				ctx['owner']=vehicleInfo.objects.get(vrn=vrn).reg_owner
				ctx['rulecat']=d.ruleCat_id
				ctx['place']=d.checkPost_id
				ctx['time']=d.date
			
				return render(request,'home/challandetail.html',ctx)
			else:
				
				return 
	else:
		return render(request,'home/vrnform.html',ctx)


def login(request):
	context={
	"error_username":"",
	"error_password":""
	}
	if(request.method=="POST"):
	    username = request.POST['username']
	    password = request.POST['password']
	    user = authenticate(request, username=username, password=password)
	    if user is not None:
	        Login(request,user)
	        # Redirect to a success page.
	        # HttpResponseRedirect(url('home:index'))
	        return HttpResponseRedirect('/home/')
	    else:
	        # Return an 'invalid login' error message.
	        return HttpResponseRedirect('/login/')
	else:
		return render(request, 'home/login.html',context)

	

def signup(request):
	context={
	"error_username":"",
	"error_pass1":"",
	"error_pass1":""
	}
	if(request.method=="POST"):
		username=request.POST['username']
		password=request.POST['password']
		email=request.POST['email']
		user = User.objects.create_user(username, email, password)
		user.save()
		return HttpResponseRedirect('/home/')

	return render(request, 'home/signup.html',context)

