## 功能
PC窗口显示设备屏幕快照，将针对窗口的操作转化为针对设备的操作  
支持的操作  
- 鼠标单击  
- 鼠标双击 
- 鼠标滑动
## 原理  
通过adb截屏命令将截屏文件传到PC并显示在窗口，将针对窗口的操作映射到adb指令并发送给设别  
## 运行
- 安装依赖包  
`pip install pillow`  
- 运行  
在**adbsnapshot**目录下运行  
`python adbsnapshot.py`   
## 操作  
- 鼠标左键单击>>单击并更新屏幕快照  
- 鼠标右键>>更新屏幕快照  
- 鼠标左键双击>>双击  
- 鼠标左键滑动>>滑动并更新快照
## 说明  
- 只支持连接一个adb设备  
- 启动前需要先建立adb连接
- 执行的命令会显示在窗口的title
- 执行的命令和命令结果会显示在终端上  
- adb传输速度较慢，wifi连接下需要1s
- 可于设备触屏失效时的设备控制
![](https://github.com/Marspacecraft/adbsnapshot/blob/main/pic.png)    

