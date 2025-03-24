from flask import Flask, jsonify, request
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from flask_pymongo import PyMongo  # ✅ Correct


# Load environment variables
load_dotenv()
MONGO_PASSWORD = os.getenv("1IwDBUjEaTYe7Ptz")
MONGO_URI = f"mongodb://sriaharshana:<1IwDBUjEaTYe7Ptz>@evchargingcluster-shard-00-00.alka3.mongodb.net:27017,evchargingcluster-shard-00-01.alka3.mongodb.net:27017,evchargingcluster-shard-00-02.alka3.mongodb.net:27017/?replicaSet=atlas-l53nj6-shard-0&ssl=true&authSource=admin&retryWrites=true&w=majority&appName=EVChargingCluster"

MONGO_URI="mongodb://sriaharshana:<1IwDBUjEaTYe7Ptz>@evchargingcluster-shard-00-00.alka3.mongodb.net:27017,evchargingcluster-shard-00-01.alka3.mongodb.net:27017,evchargingcluster-shard-00-02.alka3.mongodb.net:27017/?replicaSet=atlas-l53nj6-shard-0&ssl=true&authSource=admin&retryWrites=true&w=majority&appName=EVChargingCluster"
app = Flask(__name__)
app.config["MONGO_URI"] = MONGO_URI
mongo = PyMongo(app)
@app.route('/')
def index():
    return "MongoDB connection successful!"

if __name__ == "__main__":
    app.run(debug=True)

@app.route('/test_db')
def test_db():
    test_collection = mongo.db.test  # Replace 'test' with your actual collection name
    data = test_collection.find_one()  # Fetch one document
    return {"data": data}, 200

@app.route('/get_stations', methods=['GET'])
def get_stations():
    stations = mongo.db.stations.find()
    result = []
    for station in stations:
        station['_id'] = str(station['_id'])  # Convert ObjectId to string
        result.append(station)
    return {"stations": result}, 200


# MongoDB Connection
# MONGO_URI = "mongodb+srv://sriaharshana:<db_password>@evchargingcluster-shard-00-00.alka3.mongodb.net/?retryWrites=true&w=majority"
# MONGO_URI = MONGO_URI.replace("<db_password>", os.getenv("MONGO_DB_PASSWORD"))

client = MongoClient(MONGO_URI)
db = client["EVChargingDB"]
stations_collection = db["stations"]

@app.route('/')
def home():
    return jsonify({"message": "EV Charging API is running!"})

# API to get all charging stations
# @app.route('/stations', methods=['GET'])
# def get_stations():
#     stations = list(stations_collection.find({}, {"_id": 0}))
#     return jsonify(stations)

# API to add a new charging station
@app.route('/stations', methods=['POST'])
def add_station():
    data = request.json
    stations_collection.insert_one(data)
    return jsonify({"message": "Charging station added successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
