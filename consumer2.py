from kafka import KafkaConsumer
import numpy as np
import cv2
from ultralytics import YOLO

consumer = KafkaConsumer('my-topic-3', bootstrap_servers=['localhost:9092', 'localhost:9093', 'localhost:9094'])
def get_video():
  for message in consumer:
    frame = np.frombuffer(message.value, dtype='uint8')

    image = cv2.imdecode(frame, cv2.IMREAD_COLOR)

    model = YOLO('yolov8n.pt')
    model.to('cuda')
    results = model.track(image, persist=True)
    annotated_frame = results[0].plot()

    yield annotated_frame
for value in get_video():
  cv2.imshow('frame', value)
     
  if cv2.waitKey(1) == ord('q'):
    break
cv2.destroyAllWindows()
