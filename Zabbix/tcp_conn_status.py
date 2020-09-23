import urllib2,sys

response = urllib2.urlopen("http://127.0.0.1:9998/ngx_status")
webdata = response.readlines()

def ACTIVE():
    active = webdata[0].split(':')[1].strip()
    print int(active)
def ACCEPTS():
    accepts = webdata[2].split(' ')[1].strip()
    print int(accepts)
def HANDLED():
    handled = webdata[2].split(' ')[2].strip()
    print int(handled)
def REQUESTS():
    requests = webdata[2].split(' ')[3].strip()
    print int(requests)
def READING():
    reading = webdata[3].split(' ')[1].strip()
    print int(reading)
def WRITING():
    writing = webdata[3].split(' ')[3].strip()
    print int(writing)
def WAITING():
    waiting = webdata[3].split(' ')[5].strip()
    print int(waiting)
    
monitorkey = sys.argv[1]

if monitorkey == "ACTIVE":
    ACTIVE()
elif monitorkey == "ACCEPTS":
    ACCEPTS()
elif monitorkey == "HANDLED":
    HANDLED()
elif monitorkey == "REQUESTS":
    REQUESTS()
elif monitorkey == "READING":
    READING()
elif monitorkey == "WRITING":
    WRITING()
elif monitorkey == "WAITING":
    WAITING()