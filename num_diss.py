#import detect_track
#使用端口8848
#主机端

import socket

#import detect_track

#now_num=detect_track.pid

import socket               # 导入 socket 模块
Client_num=0
Client_all=0
com="maintain"
def sever():
    global Client_num
    global Client_all
    global com
    s = socket.socket()  # 创建 socket 对象
    host = '192.168.147.1'  # 获取本地主机名
    port = 8848  # 设置端口
    s.bind((host, port))  # 绑定端口

    s.listen(5)  # 等待客户端连接
    while True:
        c, addr = s.accept()  # 建立客户端连接。
        ans = c.recv(1024)
        arg_f=ans.split("|")[0]
        arg_t=ans.split("|")[1]
        Client_num=int(arg_f)
        Client_all=int(arg_t)
        if com=="maintain":#维持原本状态不变
            c.send('accept'.encode("utf-8"))
            c.close()  # 关闭连接
        elif com=="change":#发生修改事件
            c.send('change'.encode('utf-8'))#这里可能要添加一个循环函数吧？？？
            c.close()
            com="maintain"


