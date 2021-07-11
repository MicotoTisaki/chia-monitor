import subprocess
import os
import getpass
import psutil
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import glob
import math
import threading
import time


def subprocess_args(include_stdout=True):
    if hasattr(subprocess, 'STARTUPINFO'):
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        env = os.environ
    else:
        si = None
        env = None

    if include_stdout:
        ret = {'stdout': subprocess.PIPE}
    else:
        ret = {}

    ret.update({'stdin': subprocess.PIPE,
                'stderr': subprocess.PIPE,
                'startupinfo': si,
                'env': env })
    return ret


def byteToGiB(size):
    if size < 1024:
        return str(round(size,1))+'B'
    else:
        size = size/1024

    if size < 1024:
        return str(round(size,1))+'B'
    else:
        size = size/1024

    if size < 1024:
        return str(round(size,1))+'MiB'
    else:
        size = size/1024

    if size < 1024:
        return str(round(size,1))+'GiB'
    else:
        size = size/1024

    if size < 1024:
        return str(round(size,1))+'TiB'
    else:
        size = size/1024
        return str(round(size,1))+'PiB'

def countPlot(path):
    count = 0
    for name in glob.glob(path+'*.plot'):
        count += 1
    return count

def getTotalCapacity(path):
    totalCapacity=0
    for name in glob.glob(path+'*.plot'):
        totalCapacity+=int(os.path.getsize(name))
    return totalCapacity

def getPathFromChia():
    cmd = ['chia','plots','show']

    os.chdir("C:\\Users")
    os.chdir(getpass.getuser())
    os.chdir("AppData\\Local\\chia-blockchain")
    os.chdir(glob.glob("app-*")[0])
    os.chdir('resources\\app.asar.unpacked\\daemon')


    try:
        returncode2 = subprocess.run(cmd, **subprocess_args(True))
    except (subprocess.CalledProcessError, IndexError, OSError):
        pass

    temp = returncode2.stdout
    temp2 = temp.decode('utf-8')
    number = temp2.find("\r\n\r\n")
    dirStr = temp2[number+4:-1]
    dir = dirStr.split()
    return dir

def getDetail(dir):
    detail = [dir]
    dsk = psutil.disk_usage(dir)
    detail.append(dsk.total)
    detail.append(dsk.free)
    detail.append(countPlot(dir))
    detail.append(getIdleNumber(dsk.free))
    return detail

def getIdleNumber(size):
    number = math.floor(size/(101.5*1024*1024*1024))
    return number

def reloadUI(tree,statusLabel):
    pathList = getPathFromChia()
    
    tree.delete(*tree.get_children())
    tree.heading(0, text='path')
    tree.heading(1, text='capacity')
    tree.heading(2, text='Idle capacity')
    tree.heading(3, text='number')
    tree.heading(4, text='Idle number')
    

    for i in range(0, len(pathList)):
        detail = getDetail(pathList[i])
        item1 = detail[0]
        item2 = byteToGiB(detail[1])
        item3 = byteToGiB(detail[2])
        item4 = detail[3]
        item5 = detail[4]


        tree.insert('', 'end', values=(item1, item2, item3, item4, item5))

    pathList = getPathFromChia()

    labelData = getStatus(pathList)
    labelData.append(byteToGiB(labelData[1]))
    labelStr = 'Capacity : ' + labelData[2] + '  Number : ' + str(labelData[0])
    statusLabel["text"]=labelStr
    print("reloaded")
    return

def getStatus(pathList):
    capacity=0
    number=0
    
    for i in range(0, len(pathList)):
        detail = getDetail(pathList[i])
        capacity += getTotalCapacity(pathList[i])
        number += int(detail[3])
    return [number,capacity]

def addDir(tree,statusLabel):
    iDir = os.path.abspath(os.path.dirname("/"))
    folder_name = tk.filedialog.askdirectory(initialdir=iDir)
    print(folder_name)
    if(folder_name != ""):
        cmd = ["chia","plots","add","-d",folder_name]
        try:
            returncode2 = subprocess.run(cmd, **subprocess_args(True))
        except (subprocess.CalledProcessError, IndexError, OSError):
            pass
    reloadUI(tree,statusLabel)
    return

def deleteDir(tree,statusLabel):
    select=0
    for id in tree.selection():
        select = tree.set(id)
    if(select == 0):
        return
    
    cmd = ["chia","plots","remove","-d",select['0']]
    try:
        returncode2 = subprocess.run(cmd, **subprocess_args(True))
    except (subprocess.CalledProcessError, IndexError, OSError):
        pass
    reloadUI(tree,statusLabel)
    return

def autoReload(tree,statusLabel):
    while True:
        reloadUI(tree,statusLabel)
        time.sleep(120)



def MainWindow():
    root = tk.Tk()
    root.title('chia-monitor')

    frame = ttk.Frame(root, padding=5)
    frame.grid(row=0, column=0)

    fm_status = tk.Frame(frame)

    tree = ttk.Treeview(frame,selectmode='browse')
    
    pathList = getPathFromChia()

    labelData = getStatus(pathList)
    labelData.append(byteToGiB(labelData[1]))
    labelStr = 'Capacity : ' + labelData[2] + '  Number : ' + str(labelData[0])
    statusLabel = tk.Label(fm_status,text=labelStr)
    statusLabel.pack(side='left',padx=30)
    

    addButton = tk.Button(fm_status,text="Add dir",command=lambda: addDir(tree,statusLabel))
    addButton.pack(side='left',padx=5)
    
    reloadButton = tk.Button(fm_status,text="reload",command=lambda: reloadUI(tree,statusLabel))
    reloadButton.pack(side='right',padx=5)

    deleteButton = tk.Button(fm_status,text="Delete dir",command=lambda: deleteDir(tree,statusLabel))
    deleteButton.pack(side='right',padx=5)


    fm_status.pack(side='top',pady=10)

    

    tree['columns'] = (0,1,2,3,4)

    tree['show'] = 'headings'

    for i in range(0,5):
        tree.column(i,width=100)

    
    
    tree.heading(0, text='path')
    tree.heading(1, text='capacity')
    tree.heading(2, text='Idle capacity')
    tree.heading(3, text='number')
    tree.heading(4, text='Idle number')
    

    for i in range(0, len(pathList)):
        detail = getDetail(pathList[i])
        item1 = detail[0]
        item2 = byteToGiB(detail[1])
        item3 = byteToGiB(detail[2])
        item4 = detail[3]
        item5 = detail[4]


        tree.insert('', 'end', values=(item1, item2, item3, item4, item5))

    scroll = tk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
    scroll.pack(side=tk.RIGHT, fill="y")

    tree["yscrollcommand"] = scroll.set

    tree.pack()

    t=threading.Timer(1,autoReload,args=[tree,statusLabel])
    t.start()


    root.mainloop()



if __name__ == '__main__':
    MainWindow()
