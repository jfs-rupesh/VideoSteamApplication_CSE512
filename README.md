

# Video Streaming Application

This is a distributed video streaming application built with a Flask backend and a React frontend. It supports video upload, transcoding, search, and playback functionalities.

---

## **Project Structure**

### **Backend**
Located in `VideoSteamApplication_CSE512`.

- **`server/`**: Contains the backend Flask application.
- **`docker-compose.yml`**: Docker Compose file to run backend services.

### **Frontend**
Located in `videoPlayer/video-frontend`.

- **React Frontend**: React application for user interface.

---

## **Prerequisites**

Before running the application, ensure the following are installed:

- Docker and Docker Compose
- Node.js and npm
- MongoDB and Kafka (or use Docker for these services)
- AWS S3 bucket for video storage
- Python (optional for manual backend testing)

---

## **Environment Variables**

Ensure that you set up the `.env` file in the backend with the following values:

```env
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
MONGO_URI=mongodb://mongodb:27017/
KAFKA_BOOTSTRAP_SERVERS=kafka:9092
```

Replace placeholders with your actual configuration values.

---

## **Running the Application**

### **Step 1: Start Backend with Docker Compose**

1. Open a terminal and navigate to the backend directory:
   ```bash
   cd DDS_Project_Final\VideoSteamApplication_CSE512
   ```

2. Run the following command to start the backend:
   ```bash
   docker-compose up --build
   ```

   This will:
   - Build and start the Flask backend.
   - Start MongoDB and Kafka services (if included in `docker-compose.yml`).

3. The backend will be accessible at `http://localhost:5000`.

---

### **Step 2: Install and Start Frontend**

1. Open another terminal and navigate to the frontend directory:
   ```bash
   cd DDS_Project_Final\videoPlayer/video-frontend
   ```

2. Install the required dependencies:
   ```bash
   npm install
   ```

3. Start the React application:
   ```bash
   npm start
   ```

4. The frontend will be accessible at `http://localhost:3000`.

---

### **Step 3: Test the Application**

1. Open a web browser and navigate to `http://localhost:3000`.
2. Use the frontend to:
   - Upload videos.
   - Search for uploaded videos.
   - Play videos from the video list or via a direct URL.

---

## **Using the Application**

### **Admin View**
Click the **Admin** button in the menu to switch to the admin view. This mode allows uploading videos and managing content.

### **Search Videos**
Use the search bar to find videos by title.

### **Video Playback**
Click on a video from the search results or enter a `.m3u8` URL in the input field to play a video.

---

## **Troubleshooting**

- **MongoDB Connection Error**: Ensure the MongoDB service is running and reachable from the Flask backend.
- **Kafka Consumer Issues**: Verify that the Kafka topic `video-uploads` exists and the Kafka broker is running.
- **S3 Access Issues**: Check the AWS credentials and S3 bucket configuration in `.env`.

---
## **Additional Notes**

- The `input_video.mp4` file is a sample video for testing.
- The `README.md` file contains instructions for both manual and Dockerized setups.
- Logs are available in the Docker console for debugging.
