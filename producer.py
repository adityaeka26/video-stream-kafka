import time
import cv2
import json
import base64

from kafka import KafkaProducer
from kafka.errors import KafkaError

video_path = 'data/pklot.mp4'
kafka_topic = 'video-stream'
kafka_host = 'localhost:9092'

kafka_producer = KafkaProducer(bootstrap_servers=kafka_host)

def frame_to_json(frame, timestamp):
  _, jpeg = cv2.imencode('.jpeg', frame)

  image_str = base64.b64encode(jpeg.tobytes()).decode('utf-8')

  data = {
    'image': image_str,
    'timestamp': timestamp,
  }

  json_str = json.dumps(data).encode('utf-8')

  return json_str

def emit_video(path_to_video):
  print('start')
  video = cv2.VideoCapture(path_to_video)

  original_fps = video.get(cv2.CAP_PROP_FPS)
  new_fps = 15
  delay = 1.0 / original_fps

  frame_skip_rate = int(original_fps / new_fps)
  frame_counter = 0
  
  time_start = time.time()

  while video.isOpened():
    time_frame_start = time.time()

    success, frame = video.read()
    if not success:
      break

    if frame_counter % frame_skip_rate == 0:
      json_str = frame_to_json(frame, time_frame_start)

      future = kafka_producer.send(kafka_topic, json_str)
      try:
        future.get(timeout=10)
      except KafkaError as e:
        print(e)
        break

    # print('.', end='', flush=True)

    frame_counter += 1

    current_time = time.time()
    if current_time - time_frame_start < delay:
      time.sleep(delay - (current_time - time_frame_start))

    print(current_time - time_start, flush=True)

emit_video(video_path)