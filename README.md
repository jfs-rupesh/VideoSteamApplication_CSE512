# This repository contains a video streaming application built using Flask, React, Kafka, MongoDB, and AWS S3. The application enables users to upload videos, which are then transcoded for streaming using FFmpeg and served through NGINX.
.\venv\Scripts\activate  

#Run docker comppose
docker-compose up --build

#postman API
curl --location 'http://127.0.0.1:5000//api/upload' \
--form 'video=@"/C:/Users/91966/OneDrive/Desktop/video/sample-5s.mp4"'
