import time
import cv2
import json
import base64

from kafka import KafkaProducer
from kafka.errors import KafkaError

video_path = 'data/test.mp4'
kafka_topic = 'video-stream'
kafka_host = 'localhost:9092'

kafka_producer = KafkaProducer(bootstrap_servers=kafka_host)

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

  fps = video.get(cv2.CAP_PROP_FPS)
  delay = 1.0 / fps

  while video.isOpened():
    timestamp = time.time()

    success, frame = video.read()
    if not success:
      break

    timestamp = time.time()

    # Convert frame to JSON
    json_str = frame_to_json(frame, timestamp)

    future = kafka_producer.send(kafka_topic, json_str)
    try:
      future.get(timeout=10)
    except KafkaError as e:
      print(e)
      break

    print('.', end='', flush=True)

    time.sleep(delay)

# emit_video(0)
emit_video(video_path)