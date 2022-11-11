import requests
import time

time.sleep(10)
for i in range(90):
    r = requests.get("http://0.0.0.0:8989")
    time.sleep(1)

