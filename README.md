# adbsnapshot
 adb快照  
## 功能
PC窗口显示设备屏幕快照，将针对窗口的操操作转化为针对设别的操作  
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
在adbsnapshot目录下运行  
`python adbsnapshot.py`  
## 说明  
- 只支持连接一个adb设备  
- 启动前需要先建立adb连接
- 执行的命令会显示在窗口的title
- 执行命令和命令结果会显示在终端上
