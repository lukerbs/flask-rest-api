import requests
import json
import time

BASE = 'http://127.0.0.1:8003/api/'

data = [
	{"name":"Luke", "age": 26, "gender":"Male", "location":"San Juan Bautista"},
	{"name":"Robert", "location":"Gilroy"},
	{"name":"Hannah", "location":"Paicines"},
	{"name":"Bella", "age": 25, "location":"San Juan Bautista"}
	]

for i in range(len(data)):
	data[i] = json.dumps(data[i], indent = 4) 

headers = {"Content-Type": "application/json"}

# test put request
# send data to server
print('\n')
print('PUT REQUEST - Adding Data to Database')
for i in range(len(data)):
	response = requests.put(BASE + str(i), data=data[i], headers=headers)
	print(response.json(), '\n')
	time.sleep(.1)
print('\n\n')

input('Go?')

# test get repsonse
# retrieve data fom server
print('GET REQUEST - Retreiving Data from Database')
for i in range(len(data)):
	response = requests.get(BASE + str(i))
	print(response.json(), '\n')
print('\n\n')

input('Go?')

# API call to update data
print('UPDATE REQUEST - Updating Data from Database')
response = requests.patch(BASE + str(2), data={"name":"Hannah","age":24}, headers=headers)
print(response.json(), '\n')
print('\n\n')

input('Go?')

# test get repsonse to verify update
# retrieve data fom server
print('GET REQUEST - Retreiving Data from Database')
for i in range(len(data)):
	response = requests.get(BASE + str(i))
	print(response.json(), '\n')
print('\n\n')

input('Go?')

# API call to delete data
print("Delete REQUEST - Deleting user from database")
response = requests.delete(BASE + str(1))
print(response, '\n')
print('\n\n')

input('Go?')

# try 'getting' data again
# retrieve data fom server
for i in range(len(data)):
	try:
		response = requests.get(BASE + str(i))
		print(response.json(), '\n')
	except:
		print(f"ID:{i} does not exist")


