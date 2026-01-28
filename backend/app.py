import os
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
import bcrypt
import jwt
import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.config["JWT_SECRET"] = os.getenv("JWT_SECRET")
mongo = PyMongo(app)

# --- AUTH LOGIC ---
@app.route('/auth/signup', methods=['POST'])
def signup():
    data = request.json
    hashed_pw = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    
    user_id = mongo.db.users.insert_one({
        "name": data['name'],
        "email": data['email'],
        "password": hashed_pw,
        "created_at": datetime.datetime.utcnow()
    }).inserted_id
    
    return jsonify({"message": "User created", "id": str(user_id)}), 201

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.json
    user = mongo.db.users.find_one({"email": data['email']})
    
    if user and bcrypt.checkpw(data['password'].encode('utf-8'), user['password']):
        token = jwt.encode({
            "user_id": str(user['_id']),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, app.config["JWT_SECRET"], algorithm="HS256")
        
        return jsonify({"token": token, "name": user['name'], "email": user['email']})
    
    return jsonify({"error": "Invalid credentials"}), 401

# --- VIDEO DASHBOARD (The "Thin Client" Logic) ---
@app.route('/dashboard', methods=['GET'])
def get_dashboard():
    # Fetch from MongoDB and limit to 2 as per JD [cite: 31, 65]
    videos_cursor = mongo.db.videos.find({"is_active": True}).limit(2)
    
    videos = []
    for doc in videos_cursor:
        videos.append({
            "id": str(doc["_id"]),
            "title": doc["title"],
            "description": doc["description"],
            "youtube_id": doc["youtube_id"], # Masking logic [cite: 69-71]
            "thumbnail_url": doc["thumbnail_url"]
        })
    return jsonify(videos)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)