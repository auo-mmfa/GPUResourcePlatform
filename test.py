import pynvml
import subprocess
import os

pynvml.nvmlInit()

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
        result += "Temperature：{0}°C".format(temperature) + "<br>"
        #print("Temperature：{0}°C".format(temperature))
        #print("Performance：{0}".format(performance))
        #print("PowerState: {0}".format(powerState))
        #print("PowerUsage: {0}".format(powerUsage / 1000))
        #print("FanSpeed: {0}".format(FanSpeed))
        #print("UtilizationRates: {0}".format(UtilizationRates.gpu))  
        for proc in pynvml.nvmlDeviceGetComputeRunningProcesses(handle):
            userName, exeName = GetUserAndExeName(str(proc.pid))
            if (exeName.lower() != "cmd.exe"):
                continue
            else:
                commandline = GetCommandLine(str(proc.pid))
                print(commandline)
    return result

def GetUserAndExeName(GPUPID):
    inputCommand = "tasklist /v /nh /fi  \"PID eq " +GPUPID+"\""
    taskLine =subprocess.Popen(inputCommand,shell=True,stdout=subprocess.PIPE, universal_newlines=True).communicate()
    taskInfo = taskLine[0].split()
    exeName = taskInfo[0]
    userNameWithHost = taskInfo[7]
    userName = userNameWithHost.split('\\')[1].lower()
    return userName,exeName

def GetCommandLine(ParentPID):
    inputCommand = "wmic process where \"ParentProcessId="+str(ParentPID)+"\" get commandline,description"
    taskLine = os.popen(inputCommand).read()
    indexOfEnter = taskLine.index("\n")
    removeNoisetaskLine = taskLine[indexOfEnter:].lstrip().rstrip()
    indexOfSplitBlank = removeNoisetaskLine.rfind(" ")
    commandline = removeNoisetaskLine[:indexOfSplitBlank]
    description = removeNoisetaskLine[indexOfSplitBlank+1:]
    if(description.lower() == "python.exe"):
        return commandline
    else:
        return "It's not a python Job"        

if(__name__=="__main__") :
    print(GetNvidiaGPUInfo())