import _thread

import detect_track
import time


import socket

""""
说一说我的想法,所有的入场就是入场，所有的出场就是出场

"""


process=[]
Label_time=time.time()
now_per=0
all_per=0
base_per=0#基础人数，如果系统重启，设置这个值为场内人数就好,用户服务里面可以选择在数据库加载还是自己瞎编
last_all_per=0
last_per=0
Client_last_per=0

#mode="MAIN_machine"#有两种模式：MAIN_machine（主机模式）;SUB_machine（丛书主机）;






#其实还是应该分为两部分，统计当前的和统计总人数
def changeper(change_pernum):#修改当前人数,每次修改之后需要将主机和附属机器的进出值修改为0？？？
    global base_per
    import num_diss
    print("ceshiwanc")
    base_per=change_pernum
    detect_track.change_per(0,0)#将进出场人数修改为0，0
    #还需要将副机的in out 和总数值设为0
    num_diss.com="change"



def main(mode,host):
    global last_per
    global Label_time
    global base_per
    global now_per
    global all_per
    global last_all_per
    if mode=="MAIN_machine":#主机器主要分为三个进程？？？1.检测；2.用户输入；3.主副通信
        import sqllink
        import num_diss
        """
        hostname = socket.gethostname()
        result = socket.getaddrinfo(hostname, None, 0, socket.SOCK_STREAM)
        host=[x[4][0] for x in result][-1]
        """


        try:
            det1=_thread.start_new_thread(detect_track.detect_track,("MAIN_machine",))
            process.append(det1)
            print("检测跟踪上线...")
        #now_per, per_in_all, per_out_all=detect_track.get_now_per()
        except:
            print("检测程序发生故障，将立刻重启...")
            det1=_thread.start_new_thread(detect_track.detect_track,("MAIN_machine",))
            process[0]=det1
            print("检测程序重新上线...")

        try:
            sever1=_thread.start_new_thread(num_diss.sever,())
            process.append(sever1)
            print("双机通信上线...")
        except:
            print("双机通信故障...")
            sever1=_thread.start_new_thread(num_diss.sever,())
            process[2]=sever1
            print("双机通信重新上线...")

        while True:
            now_per=base_per+detect_track.now_per+num_diss.Client_num
            all_per=detect_track.per_all_static+num_diss.Client_all
            if now_per!=last_per:
                last_per=now_per
                print("当前场内人数为  "+str(now_per))
            if all_per!=last_all_per:
                last_all_per=all_per
                print("目前总共参观人数为    "+str(all_per))
            now=time.time()
            time.sleep(1)
            if now-Label_time>=60:
                Label_time=now
                sqllink.insert(now_per,all_per)

    if mode=="SUB_machine":
        global Client_last_per
        import num_Client

        try:
            det2=_thread.start_new_thread(detect_track.detect_track,("SUB_machine",))
            process.append(det2)
            print("检测跟踪上线...")
        #now_per, per_in_all, per_out_all=detect_track.get_now_per()
        except:
            print("检测程序发生故障，将立刻重启...")
            det2=_thread.start_new_thread(detect_track.detect_track,("SUB_machine",))
            process[0]=det2
            print("检测程序重新上线...")

        while True:
            time.sleep(1)
            Client_per=detect_track.now_per
            if Client_per!=Client_last_per:#这里只以当前人数变化作为通信发起条件
                Client_last_per=Client_per
                res=""
                try:
                    res=num_Client.consult(Client_per,detect_track.per_all_static,host)
                except:
                    print("副机无法连接主机,请及时查询主机状态")
                if res=="change":
                    detect_track.change_per(0, 0)

