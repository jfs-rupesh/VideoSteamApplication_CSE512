import os
import ffmpeg
import boto3
from botocore.exceptions import BotoCoreError, ClientError

# Set up S3 client using environment variables
aws_access_key = 'AKIAW3MEDPFB5X6VXVEB'
aws_secret_key = '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'

s3_client = boto3.client(
    's3',
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key
)

BUCKET_NAME = os.getenv('S3_BUCKET', 'video-stream-cse512')  # Default bucket
temp_dir = os.getenv('TEMP', '.')  # Use temp directory or current directory as fallback
input_file_path = os.path.join(temp_dir, 'input_video.mp4')
output_file_path = os.path.join(temp_dir, 'output_video.m3u8')

def process_video_message(message):
    video_data = message.value
    object_key = video_data.get('video_key')  # Change to 'video_key' to specify S3 key in message
    
    if not object_key:
        print("Error: 'video_key' missing in message")
        return

    # input_file_path = 'input_video.mp4'
    # output_file_path = 'output_video.m3u8'
    
    try:
        # Step 1: Download video directly from S3 using boto3
        print(f"Downloading video from S3 bucket {BUCKET_NAME} with key {object_key}")
        
        # Download the video file directly from S3 to local storage
        s3_client.download_file(BUCKET_NAME, object_key, input_file_path)
        
        # Check if the file is larger than 1 KB to validate download
        if os.path.getsize(input_file_path) <= 1024:
            print("Downloaded file size is too small. Possible download error.")
            return

        # Step 2: Transcode video using FFmpeg
        print("Transcoding video to HLS format")
        ffmpeg.input(input_file_path).output(output_file_path, format='hls', hls_time=10, hls_list_size=0).run()
        
        # Step 3: Upload transcoded video back to S3
        transcoded_key = f'transcoded_videos/{os.path.basename(output_file_path)}'
        print(f"Uploading transcoded video to S3: {transcoded_key}")
        
        s3_client.upload_file(output_file_path, BUCKET_NAME, transcoded_key)
        print(f"Processed and uploaded video: {object_key}")
    
    except (BotoCoreError, ClientError) as e:
        print(f"Failed to download or upload to S3: {e}")
    
    except ffmpeg.Error as e:
        print(f"FFmpeg error during transcoding: {e}")
    
    finally:
        # Cleanup temporary files
        if os.path.exists(input_file_path):
            os.remove(input_file_path)
        if os.path.exists(output_file_path):
            os.remove(output_file_path)


# Sample main function to test process_video_message
def main():
    print('Inside main')
    
    # Use the object key instead of the URL in the message
    message = {
        "value": {
            "video_key": "videos/sample-5s.mp4"
        }
    }

    class Message:
        def __init__(self, value):
            self.value = value

    process_video_message(Message(message["value"]))

if __name__ == "__main__":
    main()
