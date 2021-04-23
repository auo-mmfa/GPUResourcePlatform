from flask import Flask
import os
import pynvml
import subprocess
import socket

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
    print("MemoryInfo�G{0}M/{1}M�A�ϥβv�G{2}%".format("%.1f" % (usedMemory / 1024 / 1024), "%.1f" % (totalMemory / 1024 / 1024), "%.1f" % (usedMemory/totalMemory*100)))
    print("Temperature�G{0}�XC".format(temperature))
    #print("Performance�G{0}".format(performance))
    #print("PowerState: {0}".format(powerState))
    #print("PowerUsage: {0}".format(powerUsage / 1000))
    #print("FanSpeed: {0}".format(FanSpeed))
    #print("UtilizationRates: {0}".format(UtilizationRates.gpu))

app = Flask(__name__)

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
        if("�ϥΤ�" in line[i]):
            userInfo = line[i].split("  ")[0].strip()
            activeUsers.append(userInfo)
    return "�n�J����User: "+str(activeUsers)

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
        
        result += "GPU Id: "+ str(gpu_id) + "\n"
        #print("GPU Id: "+ str(gpu_id))
        result += "GPU Name: "+ gpu_name.decode("utf-8") + "\n"
        #print("GPU Name: "+ gpu_name.decode("utf-8"))
        result += "MemoryInfo�G{0}M/{1}M�A�ϥβv�G{2}%".format("%.1f" % (usedMemory / 1024 / 1024), "%.1f" % (totalMemory / 1024 / 1024), "%.1f" % (usedMemory/totalMemory*100)) + "\n"
        #print("MemoryInfo�G{0}M/{1}M�A�ϥβv�G{2}%".format("%.1f" % (usedMemory / 1024 / 1024), "%.1f" % (totalMemory / 1024 / 1024), "%.1f" % (usedMemory/totalMemory*100)))
        result += "Temperature�G{0}�XC".format(temperature) + "\n"
        #print("Temperature�G{0}�XC".format(temperature))
        
        #print("Performance�G{0}".format(performance))
        #print("PowerState: {0}".format(powerState))
        #print("PowerUsage: {0}".format(powerUsage / 1000))
        #print("FanSpeed: {0}".format(FanSpeed))
        #print("UtilizationRates: {0}".format(UtilizationRates.gpu))  

    return result

if(__name__=="__main__") :
    app.run(host='0.0.0.0', port=80,threaded=True,debug=False)
