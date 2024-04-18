import requests

BASE= "http://127.0.0.1:5000/"

data=[
    {"name":"MyVideo1","views":1,"likes":10},
    {"name":"MyVideo2","views":2,"likes":100},
    {"name":"MyVideo3","views":3,"likes":1000},
]

for i in range(len(data)): 
    response= requests.put(BASE+f"video/{i}",data[i])
    print(response.json())

response= requests.get(BASE+"video/1")
print(response.json())

response= requests.delete(BASE+"video/2")
print(response)