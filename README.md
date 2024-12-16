## 功能
PC窗口显示设备屏幕快照，将针对窗口的操作转化为针对设备的操作  
支持的操作  
- 鼠标单击  
- 鼠标双击 
- 鼠标滑动
- 键盘输入
## 原理  
通过adb截屏命令将截屏文件传到PC并显示在窗口，将针对窗口的操作映射到adb指令并发送给设别  
## 运行
- 安装依赖包  
`pip install pillow keyboard pyautogui`  
- 运行  
在**adbsnapshot**目录下运行  
`python adbsnapshot.py`   
## 操作  
- 鼠标左键单击>>单击并更新屏幕快照  
- 鼠标右键>>更新屏幕快照  
- 鼠标左键双击>>双击  
- 鼠标左键滑动>>滑动并更新快照  
- 鼠标中键>>开启/关闭键盘输入
## 说明  
- 只支持连接一个adb设备  
- 启动前需要先建立adb连接
- 执行的命令会显示在窗口的title
- 执行的命令和命令结果会显示在终端上  
- adb传输速度较慢，wifi连接下需要1s
- 可于设备触屏失效时的设备控制  
- 键盘只简单映射了75布局键盘的键值  
![](https://github.com/Marspacecraft/adbsnapshot/blob/main/pic.png)    

## DPT-RP1  
- `adbsnapshot_dpt.py`脚本专门针对dpt-rp1设备  
- 先执行`python adbsnapshot_dpt.py`命令，如果点击无效，再使用`python adbsnapshot_dpt.py DPT`命令,该命令会发送event，模拟touch操作。短按命令无法生效，原因未知。点击由长按实现，部分场景可能无法实现短按。

