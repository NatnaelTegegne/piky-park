from flask import Flask, jsonify, request
from flask_cors import CORS
from Vision.prediction import load_model, analyze_frame

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Global State
parking_config = {} 
parking_status = {}

# LOAD MODEL ON STARTUP 
ai_model = load_model()

# ====================================================
# HELPER: TRANSLATE STATUS TO INTEGER
# ====================================================
def get_mapbox_data():
    spot_list = []
    total_available = 0
    
    # 1. Get the list of IDs from the CONFIG 
    # If a spot is in config but not in status, assume it's free
    all_spots = parking_config.keys()

    for spot_id in all_spots:
        # Get info from config
        info = parking_config[spot_id]
        
        # Get status from AI (default to free)
        status_str = parking_status.get(spot_id, "free")
        status_int = 1 if status_str == "free" else 0
        
        total_available += status_int
        
        spot_list.append({
            "id": spot_id,
            "name": info.get("name", f"Spot {spot_id}"),
            "lat": info.get("lat"),
            "lng": info.get("lng"),
            "status": status_int,
            "price": "$5.00/hr"
        })
        
    return {
        "total_available": total_available,
        "spots": spot_list
    }


# CONFIG ENDPOINT

@app.route('/config', methods=['POST'])
def set_config():
    global parking_config
    parking_config = request.json
    print(f"✅ Configuration Received: {len(parking_config)} spots.")
    return jsonify({"message": "Configured"}), 200


# AI DETECTION ENDPOINT

@app.route('/detect_frame', methods=['POST'])
def detect_frame():
    global parking_status
    
    if 'frame' not in request.files:
        return jsonify({"error": "No frame"}), 400
        
    if not parking_config:
        return jsonify({"error": "System not configured yet. Run Admin Console."}), 400

    # 1. CALL YOUR ML FUNCTION
    # We pass the image file + the coordinates (parking_config) + the loaded model
    new_results = analyze_frame(request.files['frame'], parking_config, ai_model)
    
    # 2. Update the Database
    parking_status.update(new_results)
    
    print(f"AI Update: {new_results}")
    
    return jsonify(new_results)

# MAP ENDPOINT

@app.route('/mapbox-data', methods=['GET'])
def mapbox_data():
    return jsonify(get_mapbox_data())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)