# This repository contains a video streaming application built using Flask, React, Kafka, MongoDB, and AWS S3. The application enables users to upload videos, which are then transcoded for streaming using FFmpeg and served through NGINX.
.\venv\Scripts\activate  

#Run docker comppose
docker-compose up --build

#postman API
curl --location 'http://127.0.0.1:5000//api/upload' \
--form 'video=@"/C:/Users/91966/OneDrive/Desktop/video/sample-5s.mp4"'


# Process the message here (download, transcode, upload)
# Implement transcoding and other logic here
# Example: Transcode video, save to S3, etc.
# Consume messages from Kafka
# def process_video_message(message):
#     video_data = message.value
#     video_url = video_data['video_url']
    
#     # Download video from S3
#     video_response = requests.get(video_url, stream=True)
#     input_file_path = '/tmp/input_video.mp4'
    
#     with open(input_file_path, 'wb') as f:
#         for chunk in video_response.iter_content(chunk_size=8192):
#             f.write(chunk)
    
#     # Transcode video using FFmpeg
#     output_file_path = '/tmp/output_video.m3u8'
#     ffmpeg.input(input_file_path).output(output_file_path, format='hls', hls_time=10, hls_list_size=0).run()

#     # Optionally upload transcoded video back to S3
#     s3_client.upload_file(output_file_path, 'video-stream-cse512', f'transcoded_videos/{os.path.basename(output_file_path)}')

#     print(f"Processed video: {video_url}")

# def process_video_message_v2(message):
    # video_data = message.value
    # object_key = video_data.get('video_key')  # Change to 'video_key' to specify S3 key in message
    
    # if not object_key:
    #     print("Error: 'video_key' missing in message")
    #     return

    # # input_file_path = 'input_video.mp4'
    # # output_file_path = 'output_video.m3u8'
    
    # try:
    #     # Step 1: Download video directly from S3 using boto3
    #     print(f"Downloading video from S3 bucket {BUCKET_NAME} with key {object_key}")
        
    #     # Download the video file directly from S3 to local storage
    #     s3_client.download_file(BUCKET_NAME, object_key, input_file_path)
        
    #     # Check if the file is larger than 1 KB to validate download
    #     if os.path.getsize(input_file_path) <= 1024:
    #         print("Downloaded file size is too small. Possible download error.")
    #         return

    #     # Step 2: Transcode video using FFmpeg
    #     print("Transcoding video to HLS format")
    #     ffmpeg.input(input_file_path).output(output_file_path, format='hls', hls_time=10, hls_list_size=0).run()
        
    #     # Step 3: Upload transcoded video back to S3
    #     transcoded_key = f'transcoded_videos/{os.path.basename(output_file_path)}'
    #     print(f"Uploading transcoded video to S3: {transcoded_key}")
        
    #     s3_client.upload_file(output_file_path, BUCKET_NAME, transcoded_key)
    #     print(f"Processed and uploaded video: {object_key}")
    
    # except (BotoCoreError, ClientError) as e:
    #     print(f"Failed to download or upload to S3: {e}")
    
    # except ffmpeg.Error as e:
    #     print(f"FFmpeg error during transcoding: {e}")
    
    # finally:
    #     # Cleanup temporary files
    #     if os.path.exists(input_file_path):
    #         os.remove(input_file_path)
    #     if os.path.exists(output_file_path):
    #         os.remove(output_file_path)
