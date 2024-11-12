# CSE512
.\venv\Scripts\activate  

#Run docker comppose
docker-compose up --build

#postman API
curl --location 'http://127.0.0.1:5000//api/upload' \
--form 'video=@"/C:/Users/91966/OneDrive/Desktop/video/sample-5s.mp4"'