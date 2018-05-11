import tkinter as tk
#默认一旦开始检测，双机系统就会同时开始检测...不然会很麻烦...双机视频传输，我就先不写了，没时间ORZ

import threading
from threading import Thread
import detect_track
import time
import num_diss
import sqllink
import main

process=[]
Label_time=time.time()
now_per=0
all_per=0
base_per=10#基础人数，如果系统重启，设置这个值为场内人数就好,用户服务里面可以选择在数据库加载还是自己瞎编
last_all_per=0

mode="SUB_machine"#有两种模式：MAIN_machine（主机模式）;SUB_machine（丛书主机）;
last_per=0
Client_last_per=0





def button_1():#开启一个线程，打开检测程序
    Thread(target=main.main,args=("MAIN_machine","127.0.0.1")).start()


"""
def button_2():#关闭线程

    print("shadiao")
"""
def button_3():#修改当前人数
    var=t.get()
    change_pernum=int(var)
    print(change_pernum)
    Thread(target=main.changeper,args=(change_pernum,)).start()

def button_4():#修改总人数
    #var_usr_name.set("ceshi")
    var = t2.get()
    change_allnum=int(var)
    print(var)
    detect_track.per_all_static=change_allnum

def button_5():#辅机开启
    var=t3.get()
    print(var)
    Thread(target=main.main,args=("SUB_machine",var,)).start()

def button_6():#辅机结束
    pass



#我的想法是分为之几个部分的：1.检测跟踪程序启动关闭；2.用户控制（输入）；3.双机通信控制，比如辅机的数值修改什么的，不过估计不用，大不了直接全部重置

window = tk.Tk()
window.title('counting main window')
window.geometry('800x600')

# 这里是窗口的内容
l = tk.Label(window,
    text='大创展人数统计系统v2.0 @BUPT',    # 标签的文字
    bg='green',     # 背景颜色
    font=('Arial', 12),     # 字体和字体大小
    width=30, height=2  # 标签长宽
    )
l.pack()    # 固定窗口位置

b = tk.Button(window,
    text='主机开始检测',      # 显示在按钮上的文字
    width=30, height=2,
    command=button_1)    # 点击按钮式执行的命令
#b.pack()   # 按钮位置
b.place(x=100,y=60)

""""
b2 = tk.Button(window,
    text='主机结束检测',      # 显示在按钮上的文字
    width=30, height=2,
    command=button_2)   # 点击按钮式执行的命令
#b2.pack()   # 按钮位置
b2.place(x=400,y=60)
"""

t = tk.Entry(window)#用户输入修改人数的地方
t.place(x=300,y=120)


b3 = tk.Button(window,
    text='确认修改当前人数',      # 显示在按钮上的文字
    width=30, height=1,
    command=button_3)   # 点击按钮式执行的命令
b3.place(x=10,y=120)
#b3.pack()   # 按钮位置




t2 = tk.Entry(window)  #用户输入修改人数的地方
t2.place(x=300,y=170)
#t2.pack()






b4 = tk.Button(window,
    text='确认修改总人数',      # 显示在按钮上的文字
    width=30, height=1,
    command=button_4)   # 点击按钮式执行的命令
#b4.pack()   # 按钮位置
b4.place(x=10,y=170)

L2=tk.Label(text="如为辅机，输入主机IP")
L2.place(x=100,y=210)

t3=tk.Entry(window)
t3.place(x=300,y=210)




b5=tk.Button(window,text="辅机开始检测",width=30,height=1,command=button_5)
b5.place(x=100,y=240)
"""
b6=tk.Button(window,text="辅机结束检测",width=30,height=1,command=button_6)
b6.place(x=400,y=240)
"""



"""
var_usr_name = tk.StringVar()#定义变量
var_usr_name.set('example@python.com')#变量赋值'example@python.com'
entry_usr_name = tk.Entry(window, textvariable=var_usr_name)#创建一个`entry`，显示为变量`var_usr_name`即图中的`example@python.com`
entry_usr_name.place(x=160, y=150)
"""




window.mainloop()
