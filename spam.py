import requests
import time
"""
Производит спам на балансировщик
"""
time.sleep(50)
for i in range(300):
    r = requests.get("http://0.0.0.0:8989")
    time.sleep(1)

