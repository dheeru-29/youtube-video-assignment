ASSIGMENT
 Overview
This project is a full-stack video platform built to demonstrate Architecture Maturity and Clean Engineering. It follows a strict Thin Client pattern where the mobile app is a stateless rendering layer, and all business logic resides in a Headless Flask API.


 Technical Architecture
* Frontend: React Native (Expo) - A "dumb" client using Expo Router for dynamic navigation.
* Backend: Flask (Python) - A stateless REST API handling Auth and Data Masking.
* Database: MongoDB Atlas - Cloud-hosted NoSQL for flexible data modeling.
 Key Requirements 
1. The Masking Strategy (Security Awareness)
To fulfill the requirement of hiding video sources, I implemented a Video Wrapper Strategy. The backend only sends a unique youtube_id to the client. The frontend code never interacts with a raw youtube.com URL, ensuring the content source is abstracted and secure.
2. Thin-Client Logic
The mobile app contains no hardcoded video data. It relies entirely on the /dashboard endpoint. This allows for instant content updates via MongoDB without requiring a new app build or deployment.
3. JWT Stateless Authentication
Secure User Auth is handled via:
* Hashing: bcrypt for secure password storage.
* Tokens: PyJWT for stateless session management.
* Persistence: expo-secure-store for native device security with a localStorage fallback for web debugging.
* Logout: A functional logout mechanism that revokes access by clearing the local JWT.
 Project Structure
* /backend: Flask server, database models, and environment config.
* /frontend: React Native source code and assets.
Getting Started
Prerequisites
* Python 3.x
* Node.js & npm
* Expo Go app (for mobile testing)
1. Backend Setup
Navigate to the backend directory:
cd backend
1. Create and activate a virtual environment:
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
2. Install dependencies:
pip install -r requirements.txt
3. Create a .env file and add your credentials:
MONGO_URI=your_mongodb_connection_string
JWT_SECRET=your_secret_key
4. Start the server:
python app.py
5. 2. Frontend Setup
Navigate to the frontend directory:
cd frontend
1. Install dependencies:
npm install
2. 3. Important: Open app/index.tsx and update the BASE_URL to match your laptop's local IPv4 address (found via ipconfig) to ensure the mobile app can connect.
       4.Start the Expo development server:
           npx expo start