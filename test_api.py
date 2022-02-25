import requests
import time

base = 'http://192.168.1.192:8003/'
base = 'http://71.86.108.7:8003/'
base = 'http://127.0.0.1:8003/'

# test put request
# send data to server
response = requests.put("http://127.0.0.1:8003/api/4150", {"name":"Luke Kerbs", "location":"San Juan Bautista"})
print(response.json(), '\n')

time.sleep(3)

# test get repsonse
# retrieve data fom server
response = requests.get("http://127.0.0.1:8003/api/4150")
print(response.json(), '\n')