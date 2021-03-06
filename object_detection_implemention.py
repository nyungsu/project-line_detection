import cv2
import numpy as np
# import timeit
import line_detection as ld
import object_detection as od


video = cv2.VideoCapture('실선 차선인식 test.mp4')

#라인 검출용 하이퍼 파라미터
rho = 2
theta = np.pi/180
threshold = 90
min_line_len = 120
max_line_gap = 150


#Load YOLO
net,classes,layer_names,output_layers,colors = od.load_YOLO()

while True :
    ret, frame = video.read()
    frame = cv2.resize(frame,(960,720))
    if not ret:
        break
    # if ret is True:
    #     start_t = timeit.default_timer()
    height, width, channels = frame.shape
    # ------------------------------------------------------------
    
    # 객체 검출
    frame = od.detecting_object(frame, output_layers, height, width, channels)
    
    # ------------------------------------------------------------
    
    # 객체 검출된 영상 받아서 차선 검출
    pre_processing_video = ld.pre_processing(frame)
    lined_video = ld.drawing_line(pre_processing_video, rho, theta, threshold, min_line_len, max_line_gap)
    final = cv2.addWeighted(lined_video, 1., frame, 1., 0. )
    
    #--------------------------------------------------------------
    
    # terminate_t = timeit.default_timer()
    # FPS = int(1./(terminate_t - start_t ))
    cv2.imshow('frame', frame)
    cv2.imshow('dst', final)
    # print(FPS) 

    if cv2.waitKey(10) == 27:
        break


cv2.destroyAllWindows()