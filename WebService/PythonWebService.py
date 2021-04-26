from flask import Flask
import os
import pynvml
import subprocess
import socket
from flask_cors import CORS

pynvml.nvmlInit()

def printNvidiaGPU(gpu_id):
    # get GPU temperature
    gpu_device = pynvml.nvmlDeviceGetHandleByIndex(gpu_id)
    handle = pynvml.nvmlDeviceGetHandleByIndex(gpu_id)
    gpu_name = pynvml.nvmlDeviceGetName(handle)
    temperature = pynvml.nvmlDeviceGetTemperature(gpu_device, pynvml.NVML_TEMPERATURE_GPU)
    totalMemory = pynvml.nvmlDeviceGetMemoryInfo(gpu_device).total
    usedMemory = pynvml.nvmlDeviceGetMemoryInfo(gpu_device).used
    #performance = pynvml.nvmlDeviceGetPerformanceState(gpu_device)
    #powerUsage = pynvml.nvmlDeviceGetPowerUsage(gpu_device)
    #powerState = pynvml.nvmlDeviceGetPowerState(gpu_device)
    #FanSpeed = pynvml.nvmlDeviceGetFanSpeed(gpu_device)
    #UtilizationRates = pynvml.nvmlDeviceGetUtilizationRates(gpu_device)
    print("GPU Id: "+ str(i) )
    print("GPU Name: "+ gpu_name.decode("utf-8") )
    print("MemoryInfo：{0}M/{1}M，使用率：{2}%".format("%.1f" % (usedMemory / 1024 / 1024), "%.1f" % (totalMemory / 1024 / 1024), "%.1f" % (usedMemory/totalMemory*100)))
    print("Temperature：{0}°C".format(temperature))
    #print("Performance：{0}".format(performance))
    #print("PowerState: {0}".format(powerState))
    #print("PowerUsage: {0}".format(powerUsage / 1000))
    #print("FanSpeed: {0}".format(FanSpeed))
    #print("UtilizationRates: {0}".format(UtilizationRates.gpu))

app = Flask(__name__)
CORS(app)

@app.route("/",methods=["GET"])
def welcome():
    return "Welcome to Python Webservice"

@app.route("/GetActiveUsers",methods=["GET"])
def GetActiveUsers():
    hostname = socket.gethostname()
    cmd_to_run = "quser /server:"+hostname
    results = subprocess.Popen(cmd_to_run,shell=True,stdout=subprocess.PIPE, universal_newlines=True).communicate()
    line = results[0].split("\n")
    activeUsers = []
    for i in range(len(line)):
        if("使用中" in line[i]):
            userInfo = line[i].split("  ")[0].strip()
            activeUsers.append(userInfo)
    return "登入中的User: "+str(activeUsers)+"<hr size=""2"" align=""center"" noshade width=""100%"" color=""#D3D3D3"">"

@app.route("/GetHostname",methods=["GET"])
def GetHostname():
    hostname = socket.gethostname()
    return "電腦名稱: "+str(hostname)    

@app.route("/GetNvidiaGPUInfo",methods=["GET"])
def GetNvidiaGPUInfo():
    gpucount = pynvml.nvmlDeviceGetCount()
    result = ""
    for gpu_id in range(gpucount):
        gpu_device = pynvml.nvmlDeviceGetHandleByIndex(gpu_id)
        handle = pynvml.nvmlDeviceGetHandleByIndex(gpu_id)
        gpu_name = pynvml.nvmlDeviceGetName(handle)
        temperature = pynvml.nvmlDeviceGetTemperature(gpu_device, pynvml.NVML_TEMPERATURE_GPU)
        totalMemory = pynvml.nvmlDeviceGetMemoryInfo(gpu_device).total
        usedMemory = pynvml.nvmlDeviceGetMemoryInfo(gpu_device).used
        #performance = pynvml.nvmlDeviceGetPerformanceState(gpu_device)
        #powerUsage = pynvml.nvmlDeviceGetPowerUsage(gpu_device)
        #powerState = pynvml.nvmlDeviceGetPowerState(gpu_device)
        #FanSpeed = pynvml.nvmlDeviceGetFanSpeed(gpu_device)
        #UtilizationRates = pynvml.nvmlDeviceGetUtilizationRates(gpu_device)
        
        result += "GPU Id: "+ str(gpu_id) + "<br>"
        #print("GPU Id: "+ str(gpu_id))
        result += "GPU Name: "+ gpu_name.decode("utf-8") + "<br>"
        #print("GPU Name: "+ gpu_name.decode("utf-8"))
        result += "MemoryInfo：{0}M/{1}M，使用率：{2}%".format("%.1f" % (usedMemory / 1024 / 1024), "%.1f" % (totalMemory / 1024 / 1024), "%.1f" % (usedMemory/totalMemory*100)) + "<br>"
        #print("MemoryInfo：{0}M/{1}M，使用率：{2}%".format("%.1f" % (usedMemory / 1024 / 1024), "%.1f" % (totalMemory / 1024 / 1024), "%.1f" % (usedMemory/totalMemory*100)))
        result += "Temperature：{0}°C".format(temperature)
        result += "<hr size=""2"" align=""center"" noshade width=""100%"" color=""#D3D3D3"">"
        #print("Temperature：{0}°C".format(temperature))
        
        #print("Performance：{0}".format(performance))
        #print("PowerState: {0}".format(powerState))
        #print("PowerUsage: {0}".format(powerUsage / 1000))
        #print("FanSpeed: {0}".format(FanSpeed))
        #print("UtilizationRates: {0}".format(UtilizationRates.gpu))  

    return result

@app.route("/GetResourceInfo",methods=["GET"])
def GetResourceInfo(): 
    hostname = socket.gethostname()
    ResourceInfo = ""
    ResourceInfo += GetHostname() +"<hr size=""2"" align=""center"" noshade width=""100%"" color=""#D3D3D3"">"+ GetActiveUsers() + GetNvidiaGPUInfo() 
    return ResourceInfo

if(__name__=="__main__") :
    app.run(host='0.0.0.0', port=8081,threaded=True,debug=False)