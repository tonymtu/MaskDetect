import sys
import os
import cv2 as cv

sys.path.append('./baidu_api_lib')
from baidu_picture import baidu_picture_2_msg

APP_ID = '22901116'
API_KEY = 'BV4t8zLSicSo5MxK3HuLVnQE'
SECRET_KEY = 'DejFQqHdEqG8jhDXv1kqQHdPokL9P47h'

baidu_request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"

if __name__ == "__main__":
    try:
        # 打开摄像头
        capture = cv.VideoCapture(0) 

        # 传入百度AI的参数
        pic_msg = baidu_picture_2_msg(APP_ID, API_KEY, SECRET_KEY)
        
        picture_time = 0
        
        while True:
            ret, frame = capture.read()
            
            rate = 10 # 帧率相关参数
            picture_time += 1
            if (picture_time % rate) == 1:
                cv.imwrite('camera_pic.jpg',frame)  
                #从百度AI获取图片分析结果
                response = pic_msg.pic_2_msg(baidu_request_url, 'camera_pic.jpg')
                # print(response.json())
                error_msg = response.json()["error_msg"]
                if error_msg == 'SUCCESS': 
                    face_num = response.json()["result"]["face_num"]
                    #获取人脸位置，画出图框
                    for i in range(face_num):
                        location = response.json()["result"]["face_list"][i]["location"]
                        mask_data = response.json()["result"]["face_list"][i]["mask"]["type"]
                        left_top = (int(location['left']), int(location['top']))
                        right_bottom = (int(left_top[0] + location['width']), int(left_top[1] + location['height']))
                        #戴口罩绿框，没戴红框
                        if mask_data == 0:
                            cv.rectangle(frame, left_top, right_bottom, (0,0,255),2) 
                        else:
                            cv.rectangle(frame, left_top, right_bottom, (0,255,0),2) 
                    
                # 本地显示视频图像
                cv.imshow('screen', frame) 

            cv.waitKey(1)  
                    
        os.remove('camera_pic.jpg')
               
    except KeyboardInterrupt:             
        # 释放cap,销毁窗口
        capture.release()                                   
        cv.destroyAllWindows()  
        os.remove('camera_pic.jpg')
        print("任务被终止")