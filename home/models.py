from django.db import models
from django.contrib.auth.models import User
from . import choices

class checkpost(models.Model):
	state=models.IntegerField(choices= choices.states)
	district=models.IntegerField(choices= choices.district_26)
	place = models.CharField(max_length=50)
	postCode=models.CharField(max_length=20)
	api_key=models.CharField(max_length=15)
	post_id = models.CharField(max_length=5)
	def __str__(self):
		return self.post_id


class vehicle_info(models.Model):
	vrn=models.CharField(max_length=10)
	state = models.IntegerField(choices= choices.states)
	district=models.IntegerField(choices= choices.district_26)
	postCode=models.CharField(max_length=20)
	reg_owner=models.CharField(max_length=100)
	vehicle_type_id=models.IntegerField(choices= choices.vehicle_type)
	reg_email=models.EmailField(null=True)
	reg_phone=models.CharField(max_length=10)
	def __str__(self):
		return self.vrn
	

class defaulter(models.Model):
	vrn_id=models.ForeignKey(vehicle_info,on_delete=models.CASCADE)
	date_time=models.DateTimeField()
	rule_cat_id=models.IntegerField(choices= choices.rule_cat)
	checkpost_id=models.ForeignKey(checkpost,on_delete=models.CASCADE)
	def __str__(self):
			return str(self.vrn_id)


class staff(models.Model):
	name = models.ForeignKey(User,on_delete=models.CASCADE)
	checkpost = models.ForeignKey(checkpost,on_delete=models.CASCADE)
	cases_resolved = models.IntegerField(default=0)
	def __str__(self):
		return str(self.name)


class closed_cases(models.Model):
	vrn_id = models.ForeignKey(vehicle_info,on_delete=models.CASCADE)
	date_time = models.DateTimeField()
	is_paid = models.BooleanField()
	handled_by = models.ForeignKey(staff,on_delete=models.CASCADE)
	checkpost_id=models.ForeignKey(checkpost,on_delete=models.CASCADE)
	remark = models.CharField(max_length=100)
	def __str__(self):
		return str(self.vrn_id)

