# Video Stream Kafka

## Requirements
- Docker
- Anaconda / Miniconda

## How to run

### Kafka
```
docker compose up -d
```

### Conda Environment
1. Create conda environment using Python 3.11
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
