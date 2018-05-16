import cv2
import numpy as np
import time
from imutils.object_detection import non_max_suppression

# 使用人头检测，还可以使用人体检测？但是觉得不好，可能会有太多遮挡，人挨着人的情况，还是人头比较好
# 要是有一个好一点的分拣器就好了

import Person

now_per=0
per_in=0
per_out=0
per_all_static=0



def detect_track(mode):
    global per_all_static
    global now_per
    global per_in
    global per_out
    cap = cv2.VideoCapture(1)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
    face_patterns = cv2.CascadeClassifier('cascades.xml')
    vis = True  # 是否调整视频大小
    minsize = 100  # 视频中监测到的最小大小minsize
    par1 = 1.1  # 参数1scaleFactor
    par2 = 3  # 参数2minNeighbors

    width = cap.get(3)
    hight = cap.get(4)
    # 为了可视化好看一点，可以手动替换width和hight为合适的值
    if vis == True:
        width = 1080
        hight = 520
    imgArea = width * hight
    areaTH = imgArea / 250
    areaTL = imgArea / 10
    font = cv2.FONT_HERSHEY_SIMPLEX
    # Lineas de entrada/salida
    line_up = int(2 * (hight / 5)) - 50
    line_down = int(3 * (hight / 5)) + 50

    up_limit = int(1 * (hight / 5)) - 50
    down_limit = int(4 * (hight / 5)) + 50
    print(
        "h" + str(hight) + "  " + "w" + str(width) + "  " + "line_up" + str(line_up) + "  " + "line_down" + str(
            line_down))
    print(str(up_limit) + "    " + str(down_limit))
    print("Red line y:", str(line_down))
    print("Blue line y:", str(line_up))
    line_down_color = (255, 0, 0)
    line_up_color = (0, 0, 255)
    pt1 = [0, line_down]
    pt2 = [width, line_down]
    pts_L1 = np.array([pt1, pt2], np.int32)
    pts_L1 = pts_L1.reshape((-1, 1, 2))
    pt3 = [0, line_up]
    pt4 = [width, line_up]
    pts_L2 = np.array([pt3, pt4], np.int32)
    pts_L2 = pts_L2.reshape((-1, 1, 2))

    pt5 = [0, up_limit]
    pt6 = [width, up_limit]
    pts_L3 = np.array([pt5, pt6], np.int32)
    pts_L3 = pts_L3.reshape((-1, 1, 2))
    pt7 = [0, down_limit]
    pt8 = [width, down_limit]
    pts_L4 = np.array([pt7, pt8], np.int32)
    pts_L4 = pts_L4.reshape((-1, 1, 2))
    persons = []
    pid = 0
    fps=0
    now=time.time()

    while 1:
        fps+=1
        if time.time()-now>=1:
            print(fps)
            fps=0
            now=time.time()


        #所有的入场就是入场，所有的出场就是出场
        now_per = per_in - per_out

        pid = pid % 1000
        ret, img = cap.read()

        try:
            img = cv2.resize(img, (width, hight))
        except:
            print("测试结束")  # 一般是因为最后一帧无法处理？？？
            break




        dets = face_patterns.detectMultiScale(img, scaleFactor=par1, minNeighbors=par2, minSize=(minsize, minsize))
        rects = np.array([[x, y, w, h] for (x, y, w, h) in dets])
        detections = non_max_suppression(rects, probs=None, overlapThresh=0.6)

        for item in detections:
            (dx, dy, dw, dh) = item
            area = dw * dh
            if areaTH < area < areaTL:
                cx = int(dx + dw / 2)
                cy = int(dy + dh / 2)
                # print(str(cy)+"      "+str(dh))

                newrec = True
                if cy in range(up_limit, down_limit):
                    for i in persons:
                        if abs(cx - i.getX()) <= dw /2  and abs(cy - i.getY()) <= dh /2 :
                            # el objeto esta cerca de uno que ya se detecto antes
                            newrec = False
                            i.updateCoords(cx, cy)  # actualiza coordenadas en el objeto and resets age
                            if i.going_UP(line_down, line_up):
                                per_all_static+=1#这个就在这里默默统计吧，可能一直用不上
                                per_in += 1
                                print("ID:", i.getId(), 'crossed going up at', time.strftime("%c"))
                            elif i.going_DOWN(line_down, line_up):
                                per_out += 1
                                print("ID:", i.getId(), 'crossed going down at', time.strftime("%c"))
                            break
                        if i.getState() == '1':
                            if i.getDir() == 'down' and i.getY() > down_limit:
                                i.setDone()
                            elif i.getDir() == 'up' and i.getY() < up_limit:
                                i.setDone()
                        if i.timedOut():
                            # sacar i de la lista persons
                            index = persons.index(i)
                            persons.pop(index)
                            del i  # liberar la memoria de i
                    if newrec:
                        p = Person.MyPerson(pid, cx, cy, 5)
                        persons.append(p)
                        pid += 1
                cv2.circle(img, (cx, cy), 5, (0, 0, 255), -1)
                img = cv2.rectangle(img, (dx, dy), (dx + dw, dy + dh), (0, 255, 0), 2)

        for pla, i in enumerate(persons):
            if i.getY() > down_limit or i.getY() < up_limit:
                del persons[pla]
            elif time.time() - i.getSP() >= 0.5:
                del persons[pla]
            else:
                cv2.putText(img, str(i.getId()), (i.getX(), i.getY()), font, 0.5, i.getRGB(), 1, cv2.LINE_AA)

        str_up = 'UP: ' + str(per_in)
        str_down = 'DOWN: ' + str(per_out)
        img = cv2.polylines(img, [pts_L1], False, line_down_color, thickness=2)
        img = cv2.polylines(img, [pts_L2], False, line_up_color, thickness=2)
        img = cv2.polylines(img, [pts_L3], False, (255, 255, 255), thickness=1)
        img = cv2.polylines(img, [pts_L4], False, (255, 255, 255), thickness=1)
        cv2.putText(img, str_up, (10, 40), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(img, str_up, (10, 40), font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
        cv2.putText(img, str_down, (10, 90), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(img, str_down, (10, 90), font, 0.5, (255, 0, 0), 1, cv2.LINE_AA)

        cv2.imshow('Frame', img)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
#目前只统计当前人数，总人数需要到最后再改emm


def change_per(in_per,out_per):
    global per_in
    global per_out
    per_in=in_per
    per_out=out_per




detect_track("MAIN_machine")


"""
        try:
            img = cv2.resize(img, (1000, 520))
        except:
            print("测试结束")  # 一般是因为最后一帧无法处理？？？
            break
"""