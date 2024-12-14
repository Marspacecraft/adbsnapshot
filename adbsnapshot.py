import sys
import os
from PIL import Image, ImageTk
import tkinter as tk

PNGFILE='adbscreen.png'
TITLESIZE=30
global window
global winsize
global resizetime
global label
global photo
global slidepos
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

    print("---ADB SCREEN START---")
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
    window.mainloop()
    return

if __name__ == '__main__':
    main()