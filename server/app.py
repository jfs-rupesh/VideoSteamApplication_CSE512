import json
import threading
from flask import Flask, request, jsonify 
from flask_cors import CORS
import boto3
from kafka import KafkaProducer,KafkaConsumer
from pymongo import MongoClient
import os
import requests
import ffmpeg
import sys
import logging


app = Flask(__name__)
CORS(app)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)  # Ensure logs are visible in Docker logs
    ]
)
logger = logging.getLogger(__name__)

# AWS S3 setup
# Load AWS credentials from environment variables
aws_access_key = '*' 
aws_secret_key = '*'


s3_client = boto3.client(
    's3',
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key
)

# MongoDB setup
mongo_client = MongoClient('mongodb://mongodb:27017/')
db = mongo_client['video-streaming']
videos_collection = db['videos']

# Kafka setup
kafka_producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

# Kafka Consumer to consume messages from the video-uploads topic
def start_kafka_consumer():
    logger.info("Starting Kafka consumer...")
    sys.stdout.flush()
    consumer = KafkaConsumer(
        'video-uploads',
        bootstrap_servers='kafka:9092',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='video-group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    for message in consumer:
        logger.info("Inside Kafka consumer, received a message.")
        video_data = message.value
        video_url = video_data['video_url']
        logger.info(f"Received video URL: {video_url}")
        process_video_message(message)

def process_video_message(message):
    logger.info('Processing video message...')
    video_data = message.value
    video_url = video_data['video_url']
    
    # Download video from S3
    video_response = requests.get(video_url, stream=True)
    input_file_path = '/tmp/input_video.mp4'
    object_key='videos/fixed_test.mp4'


     #testing
    input_file_path2 = 'input_video_v2.mp4'
    output_file_path = 'output_video.m3u8'  
    s3_client.download_file('video-stream-cse512', 'videos/fixed_test.mp4', input_file_path2)
    ffmpeg.input(input_file_path2).output(output_file_path, format='hls', hls_time=10, hls_list_size=0).run()
    transcoded_key = f'transcoded_videos/{os.path.basename(output_file_path)}'
    print(f"Uploading transcoded video : {transcoded_key}")   
    s3_client.upload_file(output_file_path, 'video-stream-cse512', transcoded_key)
    print(f"Processed and uploaded trasncoded video: {object_key}")
    #testing over


    



    
    with open(input_file_path, 'wb') as f:
        for chunk in video_response.iter_content(chunk_size=8192):
            f.write(chunk)
    logger.info("Video downloaded from S3.")

    # Transcode video using FFmpeg
    output_dir = '/tmp/hls_output/'
    os.makedirs(output_dir, exist_ok=True)
    output_playlist_path = os.path.join(output_dir, 'output_video.m3u8')
    
   
   
    try:
        ffmpeg.input(input_file_path).output(output_playlist_path, format='hls', hls_time=10, hls_list_size=0).run()
        logger.info("Video transcoding completed.")
    except Exception as e:
        logger.error(f"Error during video transcoding: {e}")
        return

    # Upload .m3u8 and .ts files to S3
    for file_name in os.listdir(output_dir):
        logger.info('Uploading transcoded video to S3...')
        local_file_path = os.path.join(output_dir, file_name)
        s3_key = f"transcoded_videos/{file_name}"
        s3_client.upload_file(local_file_path, 'video-stream-cse512', s3_key)
        logger.info(f"Uploaded {file_name} to S3 as {s3_key}")
    
    logger.info(f"Processed video: {video_url}")


# "Hello World" route for testing
@app.route('/api/hello', methods=['GET'])
def hello_world():
    return jsonify({'message': 'Hello, World!'}), 200

@app.route('/api/upload', methods=['POST'])
def upload_video():
    print('inside upload call')
    video = request.files['video']
    if not video:
        return jsonify({'error': 'No video provided'}), 400
    
    # Upload to S3
    s3_response = s3_client.upload_fileobj(
        video,
        'video-stream-cse512', f'videos/{video.filename}'
    )
    print('sending message to kafka')
    # Send message to Kafka
    kafka_producer.send('video-uploads', {
        'video_url': f'https://video-stream-cse512.s3.amazonaws.com/videos/{video.filename}'
    })
    kafka_producer.flush()

    # Store metadata in MongoDB
    videos_collection.insert_one({
        'title': video.filename,
        'video_url': f'https://video-stream-cse512.s3.amazonaws.com/videos/{video.filename}'
    })

    return jsonify({'message': 'Video uploaded successfully'}), 200

if __name__ == '__main__':
    # Start Kafka Consumer in a separate thread
    consumer_thread = threading.Thread(target=start_kafka_consumer)
    consumer_thread.daemon = True  # Allow the consumer thread to exit when the main program exits
    consumer_thread.start()
    # Run Flask app
    app.run(host='0.0.0.0', port=5000)