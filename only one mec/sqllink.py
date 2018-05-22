import datetime

import pymysql
import time
#只有主机可以和服务器联系,更新MYSQL数据
#主机和其它机器先协商当前总人数
db=pymysql.connect("localhost","root","","personnum")
cursor = db.cursor()
#这个函数可以用来添加记录，但是从需求来看，貌似不需要updata函数，如需跟新直接添加一条记录就好，没人会看mysql的记录


def insert(now_per,all_per):
    sql_static="select count(*) from personnum"
    results=()
    #显示目前记录总数，以便后序操作
    try:
        cursor.execute(sql_static)
        results = cursor.fetchall()
        print("目前记录总数   "+str(results[0][0]))
    except:
        print("测试查询总数失败")

    #此时如果初始记录条数为0，就插入初始记录
    if results[0][0]==0:
        dt=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql_insert_init="insert into personnum (time_id,all_per,now_per,time) values('%d','%d','%d','%s')"%(0,0,0,dt)
        try:
            cursor.execute(sql_insert_init)
            db.commit()
            print("插入成功")
        except:
            print("初始值插入失败")
    time_id,all_per,now_per,time_last=0,0,0,"NULL"
    #找到上一条记录
    sql_select_last="select * from personnum where time_id=(select max(time_id) from personnum)"
    try:
        cursor.execute(sql_select_last)
        last=cursor.fetchall()
        time_id=last[0][0]
        all_per=last[0][1]
        now_per=last[0][2]
        time_last=last[0][3]
        #print("time_id   all_per    now_per time_last")
        print(str(time_id)+"    "+str(all_per)+"    "+str(now_per)+"    "+str(time_last))
        print("查询上一条记录成功")
    except:
        print("查询上一条记录失败")


    #插入记录
    dt=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql_insert="insert into personnum (time_id,all_per,now_per,time) values('%d','%d','%d','%s')"%(time_id+1,now_per,all_per,dt)
    if time_last!="NULL":
        try:
            cursor.execute(sql_insert)
            db.commit()
            print("添加记录成功")
        except:
            print("添加记录失败")
    else:
        print("未能查询得到上一条记录")



def init():
    #找到上一条记录
    sql_select_last="select * from personnum where time_id=(select max(time_id) from personnum)"
    try:
        cursor.execute(sql_select_last)
        last=cursor.fetchall()
        time_id=last[0][0]
        all_per=last[0][1]
        now_per=last[0][2]
        time_last=last[0][3]
        #print("time_id   all_per    now_per time_last")
        print(str(time_id)+"    "+str(all_per)+"    "+str(now_per)+"    "+str(time_last))
        print("查询上一条记录成功")
        return int(str(all_per))
    except:
        print("查询上一条记录失败")
