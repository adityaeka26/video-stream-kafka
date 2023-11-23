# from time import sleep
# from kafka import KafkaProducer
# import cv2
# producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
# video = cv2.VideoCapture('test.mp4')
# count = 0
# if (video.isOpened() == False): 
#     print("Unable to read camera feed")
# while(True):
#     success, frame = video.read()
#     ret, img = cv2.imencode('.jpg', frame)
#     producer.send('my-topic', img.tobytes())
#     sleep(0)
# video.release()
# print('Sukses!')

import cv2
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
 
vidObj = cv2.VideoCapture('test.mp4') 
  
# Used as counter variable 
count = 0
  
# checks whether frames were extracted 
success = 1

while success: 
  
        # vidObj object calls read 
        # function extract frames 
        success, image = vidObj.read() 
  
        # Saves the frames with frame-count 
        # cv2.imwrite("frame%d.jpg" % count, image) 
        ret, img = cv2.imencode('.jpg', image)

        producer.send('my-topic-2', img.tobytes())
  
        count += 1