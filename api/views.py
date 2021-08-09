from django.shortcuts import render
from rest_framework import viewsets
from .serializers import CheckPostSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import models
from rest_framework import serializers
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import csv
from home.models import *
import datetime
from django.core.mail import send_mail
from django.conf import settings
from home.choices import *





@csrf_exempt
def handle_upload(request):
	if request.method == 'POST':
		try:
			api_key = request.POST['api_key']
			post_id = request.POST['post_id']
			model = request.POST['model']
		except ('keyError'):
			return HttpResponse('Request has not post_id or api_key', status=400)
		file = request.FILES['file'].read().decode("utf-8")
		lines = file.split("\n")
		fields=lines[0]
		if(model=='defaulter' or model=='closed_cases'):
			try:

				check_post=checkpost.objects.filter(post_id=post_id,api_key=api_key)
				if(check_post.count()>0):
					check_post=check_post[0]
					print(check_post)
					if(model=='defaulter'):
						count=0
						for line in lines[1::]:
							row = line.split(',')
							if(len(row)==3 and row[0]!='' and row[1]!='' and row[2]!=''):
								vrn = vehicle_info.objects.filter(vrn=row[0])
								if(vrn.count()>0):
									vrn=vrn[0]
									defaulter.objects.create(vrn_id = vrn,
													rule_cat_id = int(row[1],2),
													checkpost_id = check_post,
													date_time = row[2]
													)
									count+=1

									print(vrn.reg_email,vrn.reg_owner,check_post.place,check_post.district,check_post.state, rule_cat[int(row[1],2)][1])
									send_mail(
									    'Challan Issued for {}'.format(vrn.vrn),
									    'Challan is issued for vehicle registration no. {},Registered owner {}, at {}, {}, {} ,{} for {}.'.format(vrn.vrn,vrn.reg_owner,check_post.place,dict(district_26)[check_post.district],dict(states)[check_post.state],row[2],dict(rule_cat)[int(row[1],2)]),
									    settings.EMAIL_HOST_USER,
									    [vrn.reg_email,],
									    fail_silently=True,
									)


						return HttpResponse('total {} row{} of defaulter{} data is saved'.format(count,"s" if(len(lines)>2) else "","s" if(len(lines)>2) else "" ), status=201)

					elif(model=='closed_cases'):
						count=0
						for line in lines[1::]:
							row = line.split(',')
							print(row)
							if(len(row)==2 and row[0]!='' and row[1]!=''):
								count+=1
								vrn = vehicle_info.objects.filter(vrn=row[0])[0]
								closed_cases.objects.create(vrn_id = vrn,
												date_time = row[1],
												checkpost_id = check_post,
												handled_by = staff.objects.filter(checkpost=check_post)[0],
												remark= 'machine_error',
												is_paid=False )
								print('done')
						return HttpResponse('total {} row{} of defaulter{} data is saved'.format(count,"s" if(len(lines)>2) else "","s" if(len(lines)>2) else "" ), status=201)

			except:
				return HttpResponse('request authentication failed', status=400)

		elif(model=='checkpost'):
			count=0
			for line in lines[1::]:
				row = line.split(',')
				print(row)
				if(len(row)==6  and row[0]!='' and row[1]!='' and row[2]!='' and row[3]!='' and row[4]!='' and row[5]!=''):
					count+=1
					checkpost.objects.create(state=row[0],
					district=row[1],
					place=row[2],
					postCode=row[3],
					api_key=row[4],
					post_id=row[5] )

			return HttpResponse('total {} row{} of defaulter{} data is saved'.format(count,"s" if(len(lines)>2) else "","s" if(len(lines)>2) else "" ), status=201)

		elif(model=='vehicle_info'):
			count=0
			for line in lines[1::]:
				row = line.split(',')
				print(row)
				if(len(row)==8 and row[0]!='' and row[1]!='' and row[2]!='' and row[3]!='' and row[4]!='' and row[5]!='' and row[6]!='' and row[7]!=''):
					count+=1
					vehicle_info.objects.create(vrn=row[0],
					state=row[1],
					district=row[2],
					postCode=row[3],
					reg_owner=row[4],
					vehicle_type_id=row[5],
					reg_email=row[6],
					reg_phone=row[7] )

			return HttpResponse('total {} row{} of defaulter{} data is saved'.format(count,"s" if(len(lines)>2) else "","s" if(len(lines)>2) else "" ), status=201)


			# if(model=='staff'):
			# 	for line in lines:
			# 		row = line.split(',')
			# 		checkpost.objects.create(vrn_id = vrn,
			# 							rule_cat_id = int(row[1],2),
			# 							checkpost_id = checkpost.objects.get(post_id=post_id),
			# 							date_time = row[2] )

		else:

			return HttpResponse('Model does not exist or can not be populated with API request', status=400)


		# if(checkpost.objects.filter(post_id=post_id,api_key=api_key).count()>0):
		# 	# print('line 2')
		# 	file = request.FILES['file'].read().decode("utf-8")
		# 	print(api_key,post_id,file)
		# 	lines = file.split("\n")
		# 	fields=lines[0]
		# 	for line in lines[1::]: #vrn,crime_string,post_id,crime
		# 		row = line.split(',')
		# 		print(row)
		# 		# print(row,'lllllllllllllllllllll')
		# 		# print(vehicle_info.objects.get(vrn=row[0]))#,'kkkkkkk',row[0],'UP12AP1254')
		# 		# print(row[0]==vehicle_info.objects.get(id=1))
		# 		if(vehicle_info.objects.filter(vrn=row[0])):
		# 			vrn = vehicle_info.objects.filter(vrn=row[0])[0]
		# 			dfltr = defaulter(vrn_id = vrn,
		# 							rule_cat_id = int(row[1],2),
		# 							checkpost_id = checkpost.objects.get(post_id=post_id),
		# 							date_time = row[2])
		# 			dfltr.save()


		# 	return HttpResponse('total {} row{} of defaulter{} data is saved'.format(len(lines)-1,"s" if(len(lines)>2) else "","s" if(len(lines)>2) else "" ), status=201)
		# else:
		# 	HttpResponse('api_key and post_id authentication failed', status=400)

	else:
		return HttpResponse('only POST requests are accepted', status=400)





class CheckPostViewSet(viewsets.ModelViewSet):
    queryset = checkpost.objects.all().order_by('state')
    serializer_class = CheckPostSerializer

    def post(self, request, format=None):
        serializer = CheckPostSerializer(data=request.data)

        if request.method=='POST':
            return Response(data=serializer.data, status=201)
        else:
            return Response(serializer.errors, status_code=400)
###################################################################################

# @api_view(['GET', 'POST'])
# def hell(request):
#     if request.method == 'POST':
#     	if request.POST['state']=='UP':
#     		print(request.data)
#     		serializer = CheckPostSerializer(data=request.data)
#     		serializer.is_valid(raise_exception=True)
#     		serializer.save()
#     		return Response({"message": "Got some data!", "data": request.data})
#     	return Response({"message": "Hello, world!"})
# class Photo(models.Model):
#     file = models.FileField()

#     def __str__(self):
#         return self.file.name

# class PhotoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Photo
#         fields = ('id', 'file')   # <-- HERE

# class PhotoViewSet(viewsets.ModelViewSet):
#     queryset = Photo.objects.all()
#     serializer_class = PhotoSerializer





# def save_dfltr_data(request):
# 	if(request.method == 'GET'):
# 		file = request.FILES['file']
# 		handle_uploaded_file(file)
# 		return Response(data='done', status=status.HTTP_201_CREATED)
# 	else:
# 		Response(data='done', status=status.HTTP_201_CREATED)

# def handle_uploaded_file(f):
# 	with open('some/file/name.txt', 'wb+') as destination:
# 		for chunk in f.chunks():
# 			destination.write(chunk)

# class FileUploadView(APIView):
#     parser_classes = (FileUploadParser, )

#     def post(self, request, format='txt'):
#         up_file = request.FILES['file']
#         destination = open('/Users/Username/' + up_file.name, 'wb+')
#         for chunk in up_file.chunks():
#             destination.write(chunk)
#         destination.close()  # File should be closed only after all chuns are added

#         # ...
#         # do some stuff with uploaded file
#         # ...
#         return Response(up_file.name, status.HTTP_201_CREATED)