import requests
import time


def url_decifer(instruction):
    x = (instruction.split("/")[3]).split("_")
    pills = int(x[0])
    container = int(x[1])
    
    if container == 1:
        for i in range(pills):
            URL = "http://192.168.1.174/cont1"
            requests.post(url = URL)
            time.sleep(2)
    elif container == 2:
        for i in range(pills):
            URL = "http://192.168.1.174/cont2"
            requests.post(url = URL)
            time.sleep(2)
    elif container == 3:
        for i in range(pills):
            URL = "http://192.168.1.174/cont3"
            requests.post(url = URL)
            time.sleep(2)
    else:
        for i in range(pills):
            URL = "http://192.168.1.174/cont4"
            requests.post(url = URL)
            time.sleep(2)

#URL = "http://192.168.1.174/1_3?"
#url_decifer("http://192.168.1.174/2_2")
#r = requests.post(url = URL)