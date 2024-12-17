import sys
import os
from typing import get_origin

import keyboard
import threading
import pyautogui
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog

AdbKeyValue = {
'2':'8',#1
'3':'9',#2
'4':'10',#3
'5':'11',#4
'6':'12',#5
'7':'13',#6
'8':'14',#7
'9':'15',#8
'10':'16',#9
'11':'7',#0

'16':'45',#q
'17':'51',#w
'18':'33',#e
'19':'46',#r
'20':'48',#t
'21':'53',#y
'22':'49',#u
'23':'37',#i
'24':'43',#o
'25':'44',#p
'30':'29',#a
'31':'47',#s
'32':'32',#d
'33':'34',#f
'34':'35',#g
'35':'36',#h
'36':'38',#j
'37':'39',#k
'38':'40',#l
'44':'54',#z
'45':'52',#x
'46':'31',#c
'47':'50',#v
'48':'30',#b
'49':'42',#n
'50':'41',#m

'59':'131',#f1
'60':'132',#f2
'61':'133',#f3
'62':'134',#f4
'63':'135',#f5
'64':'136',#f6
'65':'137',#f7
'66':'138',#f8
'67':'139',#f9
'68':'140',#f10
'87':'141',#f11
'88':'142',#f12

'72':'19',#up
'75':'21',#left
'80':'20',#donw
'77':'22',#right

'71':'122',#home
'79':'123',#end
'73':'92',#page up
'81':'93',#page down
'14':'112',#backspace
'83':'67',#delete
'15':'61',#tab
'28':'66',#enter
'57':'62',#space
'1':'111',#esc
'58':'115',#caps lock
'55':'318',#print screen

'26':'71',#[
'27':'72',#]
'41':'68',#`
'39':'74',#;
'40':'75',#'
'51':'55',#,
'52':'56',#.
'53':'76',#/
'43':'73',#"\\"
'12':'69',#-
'13':'70',#=

'42':'59',#left shift
'29':'113',#left ctrl
'91':'117',#left win
'56':'57',#left alt
'29':'114',#right ctrl
'54':'60'#right shift
}

# 鼠标水平位置，增大将向左移动
CALIBRATE_X=20
# 鼠标垂直位置，增大将向上移动
CALIBRATE_Y=60

PNGFILE='adbscreen.png'
DPT_SIZETIME=12.299
isDPT=False
global window
global winsize
global resizetime
global label
global photo
global slidepos
global keyboardrunning
global thread


def keyboardexit():
    global keyboardrunning
    keyboardrunning = False
    return
# 监听键盘线程
def listenkeyboard():
    print("---KEYBOARD LISTEN START---")
    keyboard.add_hotkey('ctrl+k',keyboardexit)
    while keyboardrunning:
        event = keyboard.read_event()
        if event.event_type == 'down':
            adbkey = AdbKeyValue.get(str(event.scan_code),"NONE")
            if(adbkey != "NONE"):
                cmd = 'adb shell input keyevent ' +adbkey
                print(cmd)
                os.system(cmd)
    print("---KEYBOARD LISTEN STOP---")
#报错退出
def errmessage(string):
    print(string)
    sys.exit()
# 执行shell命令，并显示在title和shell
def execadbcmd(string):
    global window
    print(string)
    window.title('ADB屏幕快照 -'+string)
    ret = os.system(string)
    print(ret)
    window.title('ADB屏幕快照')
# 加载图片
def loadimage():

    execadbcmd("adb shell screencap -p /sdcard/0.png")
    execadbcmd("adb pull /sdcard/0.png ./image/"+PNGFILE)
    try:
        adbimage = Image.open("./image/" + PNGFILE)
        return adbimage
    except:
        errmessage("adb pull failed")
        sys.exit()
# 显示图片
def showimage(adbimage):
    global winsize
    global label
    global photo
    image = adbimage.resize(winsize)
    #photo = ImageTk.PhotoImage(image)
    photo.paste(image)
    label.image = photo
    label.update()
def donothing(event):
    return
# adb锁
def adblock():
    global label
    label.bind('<ButtonRelease-1>', donothing)
    label.bind('<Button-3>', donothing)
    label.bind("<B1-Motion>", donothing)
    label.bind("<Double-Button-1>", donothing)
# adb锁
def adbunclok():
    global label
    label.bind('<ButtonRelease-1>', mouseclick)
    label.bind('<Button-3>', mouserightclick)
    label.bind("<B1-Motion>", mouseslide)
    label.bind("<Double-Button-1>", mouseslide)
# 鼠标右键点击
def mouserightclick(event):
    adblock()
    adbimage = loadimage()
    showimage(adbimage)
    adbunclok()
# PC屏幕坐标到设备屏幕坐标映射
def getdevicemousepos(event):
    global window
    global resizetime

    x, y = event.widget.winfo_pointerxy()
    x -= window.winfo_x()
    y -= window.winfo_y()
    if y >= CALIBRATE_Y:
        y -= CALIBRATE_Y
    else:
        return (0,0,0)
    if x >= CALIBRATE_X:
        x -= CALIBRATE_X
    else:
        return (0,0,0)
    if isDPT:
        return (int(x*resizetime*DPT_SIZETIME),int(y*resizetime*DPT_SIZETIME),1)
    else:
        return (int(x * resizetime), int(y * resizetime),1)
# adb命令
def adbmouseclick(x,y):
    if(isDPT):
        # execadbcmd("adb shell sendevent /dev/input/event1 3 57 1")#ABS_MT_TRACKING_ID
        execadbcmd("adb shell sendevent /dev/input/event1 3 55 0")  # ABS_MT_TOUCH_MAJOR
        execadbcmd("adb shell sendevent /dev/input/event1 3 53 "+str(x))  # ABS_MT_POSITION_X 0~20294
        execadbcmd("adb shell sendevent /dev/input/event1 3 54 "+str(y))  # ABS_MT_POSITION_Y 0~27059
        execadbcmd("adb shell sendevent /dev/input/event1 3 48 14")  # ABS_MT_TOUCH_MAJOR
        execadbcmd("adb shell sendevent /dev/input/event1 3 58 68")  # ABS_MT_PRESSURE
        execadbcmd("adb shell sendevent /dev/input/event1 1 330 1")  # BTN_TOUCH DOWN
        execadbcmd("adb shell sendevent /dev/input/event1 0 0 0")  # SYN_REPORT
        execadbcmd("adb shell sendevent /dev/input/event1 3 48 0")  # ABS_MT_TOUCH_MAJOR
        execadbcmd("adb shell sendevent /dev/input/event1 3 58 0")  # ABS_MT_PRESSURE
        # execadbcmd("adb shell sendevent /dev/input/event1 3 57 4294967295")#ABS_MT_TRACKING_ID
        execadbcmd("adb shell sendevent /dev/input/event1 1 330 0")  # BTN_TOUCH UP
        execadbcmd("adb shell sendevent /dev/input/event1 0 0 0")  # SYN_REPORT
    else:
        execadbcmd("adb shell input tap " + str(x) + " " + str(y))
# 鼠标单机释放
def mouseclick(event):
    adblock()
    x,y,z= getdevicemousepos(event)
    if z:
        adbmouseclick(x,y)
        adbimage = loadimage()
        showimage(adbimage)
    adbunclok()
# 鼠标双击
def mousedoubleclick(event):
    adblock()
    x,y,z = getdevicemousepos(event)
    if z:
        adbmouseclick(x, y)
        adbmouseclick(x, y)
    adbunclok()
# 鼠标左键滑动释放
def mousesliderelease(event):
    global slidepos
    global label
    label.bind('<ButtonRelease-1>', donothing)
    x,y,z = getdevicemousepos(event)
    if z:
        adbmouseclick(x, y)
        execadbcmd("adb shell input swipe "+str(slidepos[0])+" "+str(slidepos[1])+" "+str(x)+" "+str(y))
        adbimage = loadimage()
        showimage(adbimage)
    adbunclok()
# 鼠标左键滑动点击
def mouseslide(event):
    global slidepos
    global label
    if isDPT:
        return
    adblock()
    slidepos = getdevicemousepos(event)
    if slidepos[2]:
        label.bind('<ButtonRelease-1>', mousesliderelease)
    else:
        adbunclok()
# 鼠标中键点击
def mouse2keyboardrelease(event):
    global keyboardrunning
    global thread
    global label
    # 用户主动退出线程
    if False == keyboardrunning:
        mouse2keyboard(event)
        return
    label.bind('<Button-2>', donothing)
    keyboardrunning = False
    # 唤醒keyboard线程
    pyautogui.hotkey("Ctrl", "k")
    try:
        thread.join(5)
    except:
        print("Wait thread exit error!")

    label.bind('<Button-2>', mouse2keyboard)

# 鼠标中键点击
def mouse2keyboard(event):
    global keyboardrunning
    global thread
    global label
    label.bind('<Button-2>', donothing)
    try:
        thread = threading.Thread(target=listenkeyboard)
        keyboardrunning = True
        thread.start()
        label.bind('<Button-2>', mouse2keyboardrelease)
    except:
        print("Start keyboard thread error!")
        keyboardrunning = False
        label.bind('<Button-2>', mouse2keyboard)
# 初始窗口
def winsizeinit():
    global window
    global resizetime
    global winsize
    global isDPT

    adbimage = loadimage()
    i_x, i_y = adbimage.size
    prop = i_x / i_y

    x = window.winfo_screenwidth()
    y = window.winfo_screenheight()
    w_x = i_x
    w_y = i_y
    if w_x > (x / 2):
        w_x = (x / 2)
        w_y = x / prop
    if w_y > (2*y/3):
        w_y = (2*y/3)
        w_x = w_y * prop
    winsize = (int(w_x), int(w_y))
    resizetime = i_x / w_x
    return adbimage
def homecmd():
    execadbcmd("adb shell input keyevent 3")
def backcmd():
    execadbcmd("adb shell input keyevent 4")
def bluctoothcmd():
    execadbcmd("adb shell am start -a android.settings.BLUETOOTH_SETTINGS")
def wificmd():
    execadbcmd("adb shell am start -a android.intent.action.MAIN -n com.android.settings/.wifi.WifiSettings")
def languagecmd():
    execadbcmd("adb shell am start -a android.settings.LOCALE_SETTINGS")
def apkcmd():
    f_path = filedialog.askopenfilename(title="选择安装包",filetypes=[("APK files","*.apk")])
    execadbcmd("adb install -r "+f_path)
def Settingcmd():
    execadbcmd("adb shell am start  -n com.android.settings/com.android.settings.Settings")
def poweroffcmd():
    execadbcmd("adb shell setprop sys.powerctl shutdown")
def rebootcmd():
    execadbcmd("adb shell setprop sys.powerctl reboot")
def buttoninit():
    global window
    global winsize
    B = tk.Button(window, text="Home", command=homecmd, bg="gray", fg="yellow")
    C = tk.Button(window, text="Back", command=backcmd, bg="gray", fg="yellow")
    D = tk.Button(window, text="蓝牙", command=bluctoothcmd, bg="gray", fg="yellow")
    E = tk.Button(window, text="wifi", command=wificmd, bg="gray", fg="yellow")
    F = tk.Button(window, text="语言", command=languagecmd, bg="gray", fg="yellow")
    G = tk.Button(window, text="软件", command=apkcmd, bg="gray", fg="yellow")
    H = tk.Button(window, text="设置", command=Settingcmd, bg="gray", fg="yellow")
    I = tk.Button(window, text="关机", command=poweroffcmd, bg="gray", fg="yellow")
    J = tk.Button(window, text="重启", command=rebootcmd, bg="gray", fg="yellow")

    B.grid(row=0,column=1,sticky="nsew")
    C.grid(row=1,column=1,sticky="nsew")
    D.grid(row=2, column=1,sticky="nsew")
    E.grid(row=3, column=1,sticky="nsew")
    F.grid(row=4, column=1,sticky="nsew")
    G.grid(row=5, column=1,sticky="nsew")
    H.grid(row=6, column=1,sticky="nsew")
    I.grid(row=7, column=1, sticky="nsew")
    J.grid(row=8, column=1, sticky="nsew")

def main():
    global window
    global winsize
    global label
    global photo
    global keyboardrunning
    global isDPT
    global CALIBRATE_Y
    print("---ADB SCREEN START---")
    keyboardrunning = False
    if (len(sys.argv) > 1) and ("DPT" == sys.argv[1]):
        isDPT = True

    window = tk.Tk()
    window.resizable(False, False)
    window.title('ADB屏幕快照')

    adbimage = winsizeinit()

    buttoninit()

    image = adbimage.resize(winsize)
    photo = ImageTk.PhotoImage(image)
    label = tk.Label(window, image=photo)
    label.grid(row=0, column=0,rowspan=9)

    # 绑定鼠标左键单击事件>>点击并更新快照
    label.bind('<ButtonRelease-1>', mouseclick)
    # 绑定鼠标右键>>更新快照
    label.bind('<Button-3>', mouserightclick)
    # 绑定鼠标左键滑动>>滑动并更新快照
    label.bind("<B1-Motion>", mouseslide)
    # 绑定双击>>双击
    label.bind("<Double-Button-1>", mouseslide)
    # 绑定中键点击>>切换键盘输入
    label.bind("<Button-2>", mouse2keyboard)
    window.mainloop()
    return

if __name__ == '__main__':
    main()