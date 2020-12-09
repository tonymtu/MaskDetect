import os
import cv2
import time
import multiprocessing
from motor import ServoDrive
from baidu_api_lib.baidu_picture import baidu_picture_2_msg
                                                                                                    

def detect_show(text, rate_, qu):
    print(text)

    APP_ID = "22901116"
    API_KEY = "BV4t8zLSicSo5MxK3HuLVnQE"
    SECRET_KEY = "DejFQqHdEqG8jhDXv1kqQHdPokL9P47h"
    baidu_request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"

    try:
        # 打开摄像头
        capture = cv2.VideoCapture(0) 
        
        size = 0
        mask_flag = 0
        send = True # 是否向队列中发送消息
        last = 0 # 上次向队列中发送消息的时间

        # 传入百度AI的参数
        pic_msg = baidu_picture_2_msg(APP_ID, API_KEY, SECRET_KEY)
        picture_time = 0
        
        while True:
            ret, frame = capture.read()
            rate = rate_ # 帧率相关参数
            picture_time += 1
            
            if (picture_time % rate) == 1:
                cv2.imwrite("camera_pic.jpg",frame)  
                
                size = 0

                # 从百度AI获取图片分析结果
                response = pic_msg.pic_2_msg(baidu_request_url, "camera_pic.jpg")
                # print(response.json())
                
                error_msg = response.json()["error_msg"]
                
                if error_msg == "SUCCESS": 
                    face_num = response.json()["result"]["face_num"]
                    
                    # 获取人脸位置，画出图框
                    for i in range(face_num):
                        location = response.json()["result"]["face_list"][i]["location"]
                        mask_data = response.json()["result"]["face_list"][i]["mask"]["type"]
                        left_top = (int(location["left"]), int(location["top"]))
                        right_bottom = (int(left_top[0] + location["width"]), int(left_top[1] + location["height"]))
                        
                        # 选取最大的脸，记录size和mask_data
                        size_tmp = max(location["width"], location["height"])
                        if size_tmp > size:
                            size = size_tmp
                            mask_flag = mask_data
                        
                        # 戴口罩绿框，没戴红框
                        if mask_data == 0:
                            cv2.rectangle(frame, left_top, right_bottom, (0,0,255),2)
                        else:
                            cv2.rectangle(frame, left_top, right_bottom, (0,255,0),2)
                
                # size>=200才视为有效，一次成功后等待三秒
                if size>=200:
                    print("send :", send)
                    if not send:
                        if time.time() - last > 3:
                            send = True
                    else:
                        if mask_flag == 0:
                            qu.put(False)
                            print("---false sent---")
                        else:
                            qu.put(True)
                            print("===true sent===")
                        last = time.time()
                        send = False                
                
                # 本地显示视频图像
                cv2.imshow("screen", frame) 
            cv2.waitKey(1)  
        os.remove("camera_pic.jpg")
    
    except KeyboardInterrupt:             
        # 释放cap,销毁窗口
        capture.release()                                   
        cv2.destroyAllWindows()  
        os.remove("camera_pic.jpg")
        print("任务被终止")


def response(text, qu):
    print(text)
    servo = ServoDrive(5)
    while True:
        print("inside loop")
        tmp = qu.get()
        print("--------{}---------".format(tmp))
        if tmp:
            os.system("mplayer ./audio/pass.mp3")
        else:
            os.system("mplayer ./audio/noMask.mp3")
            servo.turn(500)
            time.sleep(10)
            servo.turn(100)


if __name__ == "__main__":
    q_respond = multiprocessing.Queue()

    start_show = multiprocessing.Process(target=detect_show, args=("display system ready", 10, q_respond))
    responds = multiprocessing.Process(target=response, args=("launch response", q_respond))

    start_show.start()
    responds.start()