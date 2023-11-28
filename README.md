# Video Stream Kafka
Simple Video Streaming and Processing with Python and Kafka.

## Requirements
- Docker
- Anaconda / Miniconda

## Python Package Requirements
- kafka-python 2.0.2
- opencv-python 4.8.0.74
- ultralytics 8.0.217

## How to run

### Kafka
```
docker compose up -d
```

### Conda Environment
1. Create conda environment with Python 3.11
    ```
    conda create -n video-stream python=3.11
    ```
2. Change conda environment to video-stream
    ```
    conda activate video-stream
    ```
3. Install package requirements using pip
    ```
    pip install -r requirements.txt
    ```

### Consumer
```
python consumer.py
```

### Producer
```
python producer.py
```
