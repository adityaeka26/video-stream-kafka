from kafka import KafkaConsumer
import numpy as np
import cv2
from ultralytics import YOLO
import json
import time
import base64

consumer = KafkaConsumer('video-stream', bootstrap_servers='localhost:9092')
average_latency = 0
frame_count = 0
total_latency = 0

def get_video():
  for message in consumer:
    data = json.loads(message.value)

    global total_latency
    global frame_count
    global average_latency
    
    latency = (time.time() - data['timestamp']) * 1000
    total_latency += latency
    frame_count += 1
    average_latency = total_latency / frame_count

    print()
    print('-----------------------')
    print(f'Latency: {latency} ms')
    print(f'Total latency: {total_latency} ms')
    print(f'Frame count: {frame_count}')
    print(f'Average latency: {average_latency} ms')

    image_bytes = base64.b64decode(data['image'])

    frame = np.frombuffer(image_bytes, dtype='uint8')
    image = cv2.imdecode(frame, cv2.IMREAD_COLOR)

    model = YOLO('yolov8n.pt')
    # model.to('cuda')
    results = model.track(image, persist=True)
    annotated_frame = results[0].plot()

    print('-----------------------')

    yield annotated_frame

for value in get_video():
  cv2.imshow('frame', value)
     
  if cv2.waitKey(1) == ord('q'):
    break

cv2.destroyAllWindows()
