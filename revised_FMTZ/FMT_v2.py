from re import sub
from datetime import datetime
from subprocess import Popen, PIPE
from screeninfo import get_monitors
from datetime import datetime as dt
from time import sleep
from os import system

import sys
import threading
import os
import pyautogui

#這份是接著上一份intern的code寫的，所以coding style有很多有出入的地方，別見怪。

#pathway直接寫死成預設
folder = "C:\Program Files\Geeks3D\FurMark2_x64\\"
folderForBatch = "C:\Program Files\Geeks3D\FurMark2_x64\\"
#這份是預設的start批次檔
file = folder + 'start_benchmark.bat'
#final_file
final_file=folder + 'last_benchmark.bat'
screenshotPath = 'C:\Program Files\Geeks3D\FurMark2_x64\screenshots'


def timeTag():
    t = dt.now().strftime("[%Y/%m/%d %H:%M:%S]") # [2022/08/10 14:23:06] 
    return t

def logNameInput():
    t = dt.now().strftime("_%Y%m%d%H%M%S") # _20220810-142306
    #store place same as exe file folder
    logName = input('Enter [Platform Name_Phase]:') + '_FMT' #aabbc_FMT_[TimeTag] # time tag will added when zipping file 
    if logName=='_FMT':
        logName='FMT' # FMT_20220810-142306 [TimeTag] will added when zipping file
        print(timeTag() +' Set platform name to ' + logName +"_[TimeTag] by default setting.\n") #[Time tag] Set test duration to FMT_[time_tag] by default setting.
    elif not logName == sub('\W+', '', logName):
        # print(timeTag(), "The platform name is invalid. Please enter a valid name! (only letters, numbers, underscore and no space)")
        print(timeTag(), 'Invalid platform name! Special characters is not allowed.')
        return logNameInput()
    # print(timeTag+' Set platform name to ' + logName +" .\n") #[Time tag] Set test duration to FMT_[time_tag] by default setting.
    else:
        print(timeTag() +' Set platform name to ' + logName +"_[TimeTag].\n") #[Time tag] Set test duration to FMT_[time_tag].
    return logName
    

def runtimeInput():
    runtime = input('Enter test duration(sec):') #string

    # default value
    if runtime=='':
        runtime=1800
        # runtime=10
        print(timeTag() +' Set test duration to ' + str(runtime) +"s by default setting.\n") #[Time tag] Set test duration to ??? sec. by default setting.
        return int(runtime)

    elif not runtime.isdigit():
        print(timeTag(), "Please enter an integer!")
        return runtimeInput()

    elif int(runtime)<20 or int(runtime)>990000:
        print(timeTag(), "Please enter an integer(max: 990000, min: 20)!")
        return runtimeInput()

    else:
        print(timeTag() +' Set test duration to ' + runtime +"s\n") #[Time tag] Set test duration to ??? sec.
    return int(runtime)

def idleInput():
    idle = input('Enter idle duration(sec):')

    if idle=='':
        # idle=3
        idle=300
        print(timeTag() +' Set idle duration to ' + str(idle) +"s by default setting.\n") #[Time tag] Set test duration to ??? sec. by default setting.
        return int(idle)

    elif not idle.isdigit():
        print(timeTag(), "Please enter an integer!")
        return idleInput()

    elif int(idle)<5 or int(idle)>990000:
        print(timeTag(), "Please enter an integer(max: 990000, min: 5)!")
        return idleInput()

    else:
        print(timeTag() +' Set idle duration to ' + idle +"s\n") #[Time tag] Set test duration to ??? sec.
    return int(idle)

def loopInput():
    n = input('Enter your test loops:')

    if n=='':
        n=4
        print(timeTag() +' Set test loop to ' + str(n) +"l by default setting.\n") #[Time tag] Set test loop to ??? by default setting.
        return int(n)

    elif not n.isdigit() :
        print(timeTag(), "Please enter an integer(min: 1)!")
        return loopInput()

    elif int(n)<1 :
        print(timeTag(), "Please enter an integer(min: 1)!")
        return loopInput()

    else:
        print(timeTag() +' Set test loop to ' + n +".\n") #[Time tag] Set test loop to ???.
    return int(n)

def inputData():
    runmode = input('Select the Test mode [1: default setting, 2: customize, 3: long run]: ')
    if runmode == '1':
        return  1800, 300, 4
    elif runmode == '2':
        return runtimeInput(),idleInput(),loopInput()
        # print("The log file name and the settings will be set by default when entering null:\nplatform name=FMT_[TimeTag], test duration=1800, idle=300, loops=4\n")
        # print("Press enter to run default value (log Name='default_log_name'/test duration=1800/idle duration=300/test loops=4)")
    elif runmode == '3':
        runFurMark(1)
        sys.exit()
    else:
        print(timeTag(), "Please enter 1,2 or 3!")
        return inputData()
    
def check_resolution():
    n = 0
    for m in get_monitors():
        n += 1
        width = str(m.width)
        height = str(m.height)
    if n == 1:
        print(timeTag(), "Get resolution =", width, 'x', height)
        return width, height
    else:
        print("<<Error>> Please make sure the system has single display!\n")
        return None, None

def write_batch(rt, width, height):
    if os.path.exists(file):
        with open(file, "rt") as f:
            x = f.read()
        with open(file, "wt") as f:
            f.write("C:\ncd " + folderForBatch + "\nfurmark --gpuinfo" + "\nfurmark --demo furmark-gl --msaa value 2 --width " + width + " --height " + height + " --max-time " + str(rt)+" --fullscreen")
    with open(final_file, "wt") as f:
        f.write("C:\ncd " + folderForBatch + "\nfurmark --gpuinfo" + "\nfurmark --demo furmark-gl --msaa value 2 --width " + width + " --height " + height +" --fullscreen")
    print(timeTag(), "Furmark setting done.")

def runFurMark(lastflag):
    print("\nCurently running furmark...")
    if lastflag==0:
        k = Popen(file, shell=True, stdout = PIPE)
    elif lastflag==1:
        k = Popen(final_file, shell=True, stdout = PIPE)
    stdout, stderr = k.communicate()
    if k.returncode == 0: # p.returncode is 0 if success
        print("Furmark finished running.")
        return True
    else:
        print(timeTag(), "Furmark starting error")
        return False
    
def ssFurmark(timer):
    sleep(timer)
    
    # 取得執行檔的路徑
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # 拼接路徑
    screenshot_dir = os.path.join(script_dir, 'screenshot')

    # 確認資料夾是否存在，不存在則建立
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)

    # 拼接完整的檔案路徑
    #ss_name = os.path.join(screenshot_dir, logName +'_screenshot_' + datetime.now().strftime("%Y%m%d-%H%M%S") + '.png')
    pyautogui.hotkey('win', 'printscreen')

    print("Screenshot saved!")

def showRemainIdle(idle):
    print(timeTag() + " idling "+ str(idle) +" Sec ...", end='\r') # idling 10 Sec
    remains = idle
    while remains >= 1:
        if(remains < 10):
            print(timeTag() + " idling      "+ str(remains) +" Sec ...", end='\r')
            sleep(1)
            remains -= 1
        elif(remains < 100):
            # print("idling 0000"+str(remains)+" s", end='\r')
            print(timeTag() + " idling     "+ str(remains) +" Sec ...", end='\r')
            sleep(1)
            remains -= 1
        elif(remains < 1000):
            # print("idling    "+str(remains)+" Sec", end='\r')
            print(timeTag() + " idling    "+ str(remains) +" Sec ...", end='\r')
            sleep(1)
            remains -= 1
        elif(remains < 10000):
            print(timeTag() + " idling   "+ str(remains) +" Sec ...", end='\r')
            print("idling   "+str(remains)+" Sec", end='\r')
            sleep(1)
            remains -= 1
        elif(remains < 100000):
            print(timeTag() + " idling  "+ str(remains) +" Sec ...", end='\r')
            print("idling  "+str(remains)+" Sec", end='\r')
            sleep(1)
            remains -= 1
        elif(remains < 1000000):
            print(timeTag() + " idling "+ str(remains) +" Sec ...", end='\r')
            print("idling "+str(remains)+" Sec", end='\r')
            sleep(1)
            remains -= 1


def main():
    system("title " + "FMTZ v.1.1")
    print('[HP products use only] This tool is developed and published by HP, please contact CPS SIT TPM if there is any problem.')
    print('Now you\'re running FurMark stress test tool\n')

    width, height = check_resolution()
    if width and height:
        runtime, idle, loop = inputData()
        print(runtime, idle, loop)

        # Write batch file
        write_batch(runtime, width, height)

        for i in range(loop-1):    
             # 創建兩個線程
            thread1 = threading.Thread(target=runFurMark,args=(0,))
            thread2 = threading.Thread(target=ssFurmark, args=(runtime-2,))

            # 啟動線程
            thread1.start()
            thread2.start()

            # 等待線程完成
            thread1.join()
            thread2.join()
            
            #shows remaining idle time
            showRemainIdle(idle)
            sleep(1)
        #最後一圈
        thread1 = threading.Thread(target=runFurMark,args=(1,))
        thread2 = threading.Thread(target=ssFurmark, args=(runtime-2,))
        thread1.start()
        thread2.start()

        # 等待線程完成
        thread1.join()
        thread2.join()

        print("\n"+timeTag()+' Test completed!')

if __name__ == '__main__':
    main()