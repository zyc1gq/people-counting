import socket

def consult(now_num,all_per):
    s = socket.socket()  # 创建 socket 对象
    host = '192.168.147.1'  # 获取本地主机名
    port = 8848  # 设置端口好

    s.connect((host, port))
    s.send((str(now_num)+"|"+str(all_per)))
    ans = s.recv(1024)
    print(ans)
    if ans == "accept".encode('utf-8'):
        print("传输成功")
        s.close()
        return "accept"
    elif ans=="change".encode('utf-8'):
        print("开始修改副机数值")
        s.close()
        return "change"

    return "testok"


#consult(10)