import time
import sys
import cv2
import json
import base64

from kafka import KafkaProducer
from kafka.errors import KafkaError

producer = KafkaProducer(bootstrap_servers=('localhost:9092'))
topic = 'video-stream'

def frame_to_json(frame, timestamp):
    # Encode frame to JPEG
    ret, jpeg = cv2.imencode('.jpeg', frame)

    # Convert JPEG bytes to base64 string
    image_str = base64.b64encode(jpeg.tobytes()).decode('utf-8')

    # Create data dictionary
    data = {
      'image': image_str,
      'timestamp': timestamp,
    }

    # Convert data dictionary to JSON string
    json_str = json.dumps(data).encode('utf-8')

    return json_str

def emit_video(path_to_video):
  print('start')
  video = cv2.VideoCapture(path_to_video)

  while video.isOpened():
    timestamp = time.time()

    success, frame = video.read()
    if not success:
      break

    timestamp = time.time()  # Replace with your method of getting the timestamp

    # Convert frame to JSON
    json_str = frame_to_json(frame, timestamp)

    future = producer.send(topic, json_str)
    try:
      future.get(timeout=10)
    except KafkaError as e:
      print(e)
      break

    print('.', end='', flush=True)

# emit_video(0)
emit_video('data/test.mp4')
# emit_video(0)