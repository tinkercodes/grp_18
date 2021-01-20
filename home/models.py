from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class vehicleType(models.Model):
	vtype=models.CharField(max_length=20)
	def __str__(self):
		return self.vtype


class checkPost(models.Model):
	postCode=models.CharField(max_length=20)
	state=models.CharField(max_length=30)
	district=models.CharField(max_length=30)
	def __str__(self):
		return str(self.district)+", "+str(self.state)+", "+str(self.postCode)

class ruleCat(models.Model):
	rule=models.TextField(max_length=200)
	def __str__(self):
		return self.rule

class vehicleInfo(models.Model):
	vrn=models.CharField(max_length=10)
	reg_owner=models.CharField(max_length=100)
	vehicleType_id=models.ForeignKey(vehicleType,on_delete=models.CASCADE)
	reg_email=models.EmailField(null=True)
	reg_phone=models.CharField(max_length=10)

class defaulter(models.Model):
	vrn=models.CharField(max_length=10)
	date=models.DateTimeField()
	ruleCat_id=models.ForeignKey(ruleCat,on_delete=models.CASCADE)
	checkPost_id=models.ForeignKey(checkPost,on_delete=models.CASCADE)
	time=models.TimeField()


class fir(models.Model):
	vrn=models.CharField(max_length=10)
	description=models.TextField(max_length=200)
	date=models.DateTimeField()