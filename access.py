#from flask import Flask,request
import socket
#app = Flask(__name__)

#@app.route('/',methods=["GET","POST"])
def asdf():
    deviceName = socket.gethostname()
    d=socket.socket()
    d.bind(('',0))
    deviceIPAddr = socket.gethostbyname(deviceName)
    
    print("deviceIPAddr ", deviceIPAddr)
    exIP = socket.gethostbyname_ex(deviceName)
    a = socket.gethostbyaddr(deviceName)
    deviceUnitId=deviceName
    currentIp=exIP 
    lastIp=exIP[2] 
    PORT=d.getsockname()[1]
    deviceIp=exIP[2] 
    devicePort='8081'
    data= [deviceUnitId, currentIp, PORT,deviceIp,devicePort]
    print(data)    

    return data
'''@app.route('/',methods=["GET","POST"])
def device_dat():
    if request.method=='POST':
        data=request.data
        dat_lst=eval(data)
        print(dat_lst)'''


        
if __name__ == '__main__':
    #app.run()
    asdf()
    

