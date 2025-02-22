# Distributed Video Streaming Application

## Overview
This project is a **Distributed Video Streaming Application** developed as part of the CSE 512 course. The application provides efficient and scalable video streaming capabilities, leveraging distributed computing principles.

## Features
- Distributed architecture for scalable video streaming
- Efficient video segmentation and adaptive bitrate streaming
- Backend built using FastAPI
- Frontend developed with React.js
- Cloud-based storage and delivery using AWS S3 and CloudFront
- Load balancing with Nginx and Docker containers

## Technologies Used
- **Backend:** FastAPI, Python, Redis
- **Frontend:** React.js, HTML, CSS
- **Database:** PostgreSQL
- **Cloud Services:** AWS S3, AWS Lambda, CloudFront
- **Containerization:** Docker, Kubernetes

## Installation

### Prerequisites
- Python 3.8+
- Node.js 14+
- Docker & Docker Compose
- AWS CLI (configured with necessary permissions)

### Steps to Run Locally

1. **Clone the Repository**
   ```bash
   git clone https://github.com/jfs-rupesh/VideoSteamApplication_CSE512.git
   cd VideoSteamApplication_CSE512
   ```

2. **Set Up Backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

3. **Set Up Frontend**
   ```bash
   cd frontend
   npm install
   npm start
   ```

4. **Run with Docker**
   ```bash
   docker-compose up --build
   ```

## Usage
- Users can upload, stream, and manage videos.
- Adaptive bitrate streaming ensures smooth playback across different network conditions.
- Admin panel for managing videos and user access.

## Deployment
- Deployed on AWS using EC2 instances, S3 for storage, and CloudFront for distribution.
- CI/CD pipeline using GitHub Actions.

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a feature branch (`feature-new`).
3. Commit your changes.
4. Submit a pull request.


## Contact
For any queries, reach out to:
**Rupesh Nivrutti Barve**  
Email: rbarve1@asu.edu  
GitHub: [@jfs-rupesh](https://github.com/jfs-rupesh)

