import cv2
import pandas as pd
from ultralytics import YOLO
from playsound import playsound
import random



def cam_detection(path_x):

    model = YOLO('best (11).pt')

    # def RGB(event, x, y, flags, param):
    #     if event == cv2.EVENT_MOUSEMOVE:
    #         colorsBGR = [x, y]
    #         print(colorsBGR)

    # cv2.namedWindow('RGB')
    # cv2.setMouseCallback('RGB', RGB)
    video_capture = path_x
    cap=cv2.VideoCapture(video_capture)
    my_file = open("coco.txt", "r")
    data = my_file.read()
    class_list = data.split("\n")
    count = 0

    # Define class labels for bottles and cans
    drowsy_label = "drowsy"
    awake_label = "awake"

    while True:
        ret, frame = cap.read()
        count += 1
        if count % 3 != 0:
            continue

        frame = cv2.resize(frame, (1020, 500))

        results = model.predict(frame, conf=0.7)
        xyxy_boxes = results[0].boxes.xyxy
        confidences = results[0].boxes.conf
        class_ids = results[0].boxes.cls

        detected = False  # Flag to check if any object was detected

        for i in range(len(xyxy_boxes)):
            x1, y1, x2, y2 = map(int, xyxy_boxes[i][:4])
            class_id = int(class_ids[i])
            label = class_list[class_id]
            confidence = float(confidences[i])

            if confidence > 0.7:
                detected = True

                if label == awake_label:
                    print("awake")
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, f'{label}: {confidence:.2f}', (x1, y1), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 1)

                elif label == drowsy_label:
                    playsound('Alarm.mp3')
                    print("drowsy")
                    n = random.random()
                    filename = f'./static/captured_images/image_{n}.jpg'
                    cv2.imwrite(filename,frame)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, f'{label}: {confidence:.2f}', (x1, y1), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 1)
        yield frame
cv2.destroyAllWindows()
   



