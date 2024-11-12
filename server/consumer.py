import json
import requests
import boto3
import ffmpeg
import os
from kafka import KafkaConsumer

# Initialize Kafka Consumer
consumer = KafkaConsumer(
    'video-uploads',  # Kafka topic
    bootstrap_servers='kafka:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='video-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)


aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')

# AWS S3 setup

aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')

s3_client = boto3.client(
    's3',
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key
)

# Consume messages from Kafka
def process_video_message(message):
    video_data = message.value
    video_url = video_data['video_url']
    
    # Download video from S3
    video_response = requests.get(video_url, stream=True)
    input_file_path = '/tmp/input_video.mp4'
    
    with open(input_file_path, 'wb') as f:
        for chunk in video_response.iter_content(chunk_size=8192):
            f.write(chunk)
    
    # Transcode video using FFmpeg
    output_file_path = '/tmp/output_video.m3u8'
    ffmpeg.input(input_file_path).output(output_file_path, format='hls', hls_time=10, hls_list_size=0).run()

    # Optionally upload transcoded video back to S3
    s3_client.upload_file(output_file_path, 'video-stream-cse512', f'transcoded_videos/{os.path.basename(output_file_path)}')

    print(f"Processed video: {video_url}")


# Continuously consume messages from Kafka
def consume_kafka_messages():
    for message in consumer:
        process_video_message(message)


if __name__ == '__main__':
    consume_kafka_messages()