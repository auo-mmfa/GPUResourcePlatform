import pynvml
import subprocess
import os

pynvml.nvmlInit()

def GetNvidiaGPUInfo(pidUserDict,PidCommandlineDic):
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
        result += "Temperature：{0}°C".format(temperature) + "<br>"
        #print("Temperature：{0}°C".format(temperature))
        #print("Performance：{0}".format(performance))
        #print("PowerState: {0}".format(powerState))
        #print("PowerUsage: {0}".format(powerUsage / 1000))
        #print("FanSpeed: {0}".format(FanSpeed))
        #print("UtilizationRates: {0}".format(UtilizationRates.gpu))  
        for proc in pynvml.nvmlDeviceGetComputeRunningProcesses(handle):
            if str(proc.pid) in pidUserDict:
                userName =  pidUserDict[str(proc.pid)]
                commandline = PidCommandlineDic[str(proc.pid)]
                result += "User: "+userName+", Job: "+commandline+ "<br>"
    return result    

def MakePidUserDic():
    pidUserDict = {}
    inputCommand = "tasklist /v /nh /fi \"IMAGENAME eq python.exe\""
    taskLine =subprocess.Popen(inputCommand,shell=True,stdout=subprocess.PIPE, universal_newlines=True).communicate()
    taskCollection = taskLine[0].split("\n")
    word = "AUO"
    for i in range(len(taskCollection)):
        if word in taskCollection[i]:
            taskInfo = taskCollection[i].split()
            pid = taskInfo[1]
            userNameWithHost = taskInfo[-3]
            userName = userNameWithHost.split('\\')[1].lower()
            pidUserDict[pid] = userName
    return pidUserDict

def MakePidCommandlineDic():
    pidCommandlineDict = {}
    inputCommand = "wmic process where name=\"python.exe\" get commandline,processid"
    taskLine = os.popen(inputCommand).read()
    indexOfEnter = taskLine.index("\n")
    removeNoisetaskLine = taskLine[indexOfEnter:].lstrip().rstrip()
    taskCollection = taskLine.split("\n")
    word = "python"
    for i in range(len(taskCollection)):
        if word in taskCollection[i]:
            taskInfo = taskCollection[i].split()
            pid = taskInfo[-1]
            commandline = taskCollection[i].replace(pid,"").lstrip().rstrip()
            pidCommandlineDict[pid] = commandline
    return pidCommandlineDict
       

if(__name__=="__main__") :
    pidUserDict = MakePidUserDic()
    PidCommandlineDic = MakePidCommandlineDic()
    print(GetNvidiaGPUInfo(pidUserDict,PidCommandlineDic))