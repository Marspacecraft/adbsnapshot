import sys
import os
import keyboard
import threading
import pyautogui
from PIL import Image, ImageTk
import tkinter as tk

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

PNGFILE='adbscreen.png'
TITLESIZE=30
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
    global window
    window.bind('<ButtonRelease-1>', donothing)
    window.bind('<Button-3>', donothing)
    window.bind("<B1-Motion>", donothing)
    window.bind("<Double-Button-1>", donothing)
# adb锁
def adbunclok():
    global window
    window.bind('<ButtonRelease-1>', mouseclick)
    window.bind('<Button-3>', mouserightclick)
    window.bind("<B1-Motion>", mouseslide)
    window.bind("<Double-Button-1>", mouseslide)
# 鼠标右键点击
def mouserightclick(event):
    adblock()
    adbimage = loadimage()
    showimage(adbimage)
    adbunclok()
# PC屏幕坐标到设备屏幕坐标映射
def mousepos2string(event):
    global window
    global resizetime

    x, y = event.widget.winfo_pointerxy()
    x -= window.winfo_x()
    y -= window.winfo_y()
    if y > TITLESIZE:
        y -= TITLESIZE
    ret = str(int(x*resizetime))+" "+str(int(y*resizetime))
    return ret
# 鼠标单机释放
def mouseclick(event):
    adblock()
    execadbcmd("adb shell input tap "+mousepos2string(event))
    adbimage = loadimage()
    showimage(adbimage)
    adbunclok()
# 鼠标双击
def mousedoubleclick(event):
    adblock()
    pos = mousepos2string(event)
    execadbcmd("adb shell input tap " + pos)
    execadbcmd("adb shell input tap " + pos)
    adbunclok()
# 鼠标左键滑动释放
def mousesliderelease(event):
    global slidepos
    window.bind('<ButtonRelease-1>', donothing)
    execadbcmd("adb shell input swipe "+slidepos+" "+mousepos2string(event))
    adbimage = loadimage()
    showimage(adbimage)
    adbunclok()
# 鼠标左键滑动点击
def mouseslide(event):
    global slidepos
    adblock()
    slidepos = mousepos2string(event)
    window.bind('<ButtonRelease-1>', mousesliderelease)
# 鼠标中键点击
def mouse2keyboardrelease(event):
    global keyboardrunning
    global thread
    window.bind('<Button-2>', donothing)
    keyboardrunning = False
    # 唤醒keyboard线程
    pyautogui.hotkey("Ctrl", "k")
    try:
        thread.join(5)
    except:
        print("Wait thread exit error!")

    window.bind('<Button-2>', mouse2keyboard)

# 鼠标中键点击
def mouse2keyboard(event):
    global keyboardrunning
    global thread
    window.bind('<Button-2>', donothing)
    try:
        thread = threading.Thread(target=listenkeyboard)
        keyboardrunning = True
        thread.start()
        window.bind('<Button-2>', mouse2keyboardrelease)
    except:
        print("Start keyboard thread error!")
        keyboardrunning = False
        window.bind('<Button-2>', mouse2keyboard)
# 初始窗口
def winsizeinit():
    global window
    global resizetime
    global winsize
    adbimage = loadimage()
    i_x, i_y = adbimage.size
    prop = i_x / i_y

    x = window.winfo_screenwidth()
    y = window.winfo_screenheight()

    if i_x > (x / 2):
        i_x = (x / 2)
        i_y = i_x / prop
    if i_y > (y / 2):
        i_y = (y / 2)
        i_x = i_y * prop
    winsize = (int(i_x), int(i_y))
    x, y = adbimage.size
    resizetime = x / i_x
    return adbimage

def main():
    global window
    global winsize
    global label
    global photo
    global keyboardrunning

    print("---ADB SCREEN START---")
    keyboardrunning = False

    window = tk.Tk()
    window.resizable(False, False)
    window.title('ADB屏幕快照')

    adbimage = winsizeinit()
    image = adbimage.resize(winsize)
    photo = ImageTk.PhotoImage(image)
    label = tk.Label(window, image=photo)
    label.pack()

    # 绑定鼠标左键单击事件>>点击并更新快照
    window.bind('<ButtonRelease-1>', mouseclick)
    # 绑定鼠标右键>>更新快照
    window.bind('<Button-3>', mouserightclick)
    # 绑定鼠标左键滑动>>滑动并更新快照
    window.bind("<B1-Motion>", mouseslide)
    # 绑定双击>>双击
    window.bind("<Double-Button-1>", mouseslide)
    # 绑定中键点击>>切换键盘输入
    window.bind("<Button-2>", mouse2keyboard)
    window.mainloop()
    return

if __name__ == '__main__':
    main()