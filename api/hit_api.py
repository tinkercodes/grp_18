import requests
url='http://127.0.0.1:8000/api/checkPost/'
data={
	'state':'UP',
	'district':'SRNGR',
	'postCode':'871009'
}

response=requests.post(url=url,data=data)
print(response.text)
# for id in range(6,250):
# 	response=requests.delete(url=url,args=)
# 	print(response)