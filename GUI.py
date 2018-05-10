import tkinter as tk



#我的想法是分为之几个部分的：1.检测跟踪程序启动关闭；2.用户控制（输入）；3.双机通信控制，比如辅机的数值修改什么的，不过估计不用，大不了直接全部重置

window = tk.Tk()
window.title('my window')
window.geometry('200x100')

# 这里是窗口的内容
e = tk.Entry(window,show='*')
e.pack()



t = tk.Text(window,height=2)
t.pack()
window.mainloop()
