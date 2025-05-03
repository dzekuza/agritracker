from flask_cors import CORS
from flask import Flask, jsonify
print("✅ Starting API script...")
try:
    from scraper import fetch_wheat_prices
    print("✅ scraper.py imported successfully")
except Exception as e:
    print("❌ Failed to import scraper.py:", str(e))

app = Flask(__name__)
CORS(app)
data_cache = {
    "wheat": []
}

@app.route("/api/wheat", methods=["GET"])
def get_wheat_data():
    return jsonify(data_cache["wheat"])

@app.route("/api/update", methods=["POST"])
def update_data():
    print("🔄 Updating cache...")
    try:
        data_cache["wheat"] = fetch_wheat_prices()
        return jsonify({"status": "updated", "count": len(data_cache["wheat"])})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    print("🚀 API server running at http://localhost:5000")
    app.run(debug=True, host="0.0.0.0", port=5050)