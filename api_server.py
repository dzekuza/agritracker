from flask_cors import CORS
from flask import Flask, jsonify
print("✅ Starting API script...")
try:
    from scraper import (
        fetch_wheat_prices, fetch_corn_prices, fetch_rapeseed_prices,
        fetch_cme_wheat_prices, fetch_cme_corn_prices, fetch_cme_rapeseed_prices
    )
    print("✅ scraper.py imported successfully")
except Exception as e:
    print("❌ Failed to import scraper.py:", str(e))

app = Flask(__name__)
CORS(app)
data_cache = {
    "wheat": [],
    "corn": [],
    "rapeseed": [],
    "cme_wheat": [],
    "cme_corn": [],
    "cme_rapeseed": []
}
print("🔄 Initial data fetch...")
try:
    data_cache["wheat"] = fetch_wheat_prices()
    print(f"✅ Wheat cache loaded: {len(data_cache['wheat'])} records")
except Exception as e:
    print("❌ Wheat fetch failed:", e)

try:
    data_cache["corn"] = fetch_corn_prices()
    print(f"✅ Corn cache loaded: {len(data_cache['corn'])} records")
except Exception as e:
    print("❌ Corn fetch failed:", e)

try:
    data_cache["rapeseed"] = fetch_rapeseed_prices()
    print(f"✅ Rapeseed cache loaded: {len(data_cache['rapeseed'])} records")
except Exception as e:
    print("❌ Rapeseed fetch failed:", e)

try:
    data_cache["cme_wheat"] = fetch_cme_wheat_prices()
    print(f"✅ CME Wheat cache loaded: {len(data_cache['cme_wheat'])} records")
except Exception as e:
    print("❌ CME Wheat fetch failed:", e)

try:
    data_cache["cme_corn"] = fetch_cme_corn_prices()
    print(f"✅ CME Corn cache loaded: {len(data_cache['cme_corn'])} records")
except Exception as e:
    print("❌ CME Corn fetch failed:", e)

try:
    data_cache["cme_rapeseed"] = fetch_cme_rapeseed_prices()
    print(f"✅ CME Rapeseed cache loaded: {len(data_cache['cme_rapeseed'])} records")
except Exception as e:
    print("❌ CME Rapeseed fetch failed:", e)

@app.route("/api/wheat", methods=["GET"])
def get_wheat_data():
    return jsonify(data_cache["wheat"])

@app.route("/api/corn", methods=["GET"])
def get_corn_data():
    return jsonify(data_cache["corn"])

@app.route("/api/rapeseed", methods=["GET"])
def get_rapeseed_data():
    return jsonify(data_cache["rapeseed"])

@app.route("/api/cme/wheat", methods=["GET"])
def get_cme_wheat_data():
    return jsonify(data_cache["cme_wheat"])

@app.route("/api/cme/corn", methods=["GET"])
def get_cme_corn_data():
    return jsonify(data_cache["cme_corn"])

@app.route("/api/cme/rapeseed", methods=["GET"])
def get_cme_rapeseed_data():
    return jsonify(data_cache["cme_rapeseed"])

@app.route("/api/update", methods=["POST"])
def update_data():
    print("🔄 Updating cache...")
    try:
        data_cache["wheat"] = fetch_wheat_prices()
        data_cache["corn"] = fetch_corn_prices()
        data_cache["rapeseed"] = fetch_rapeseed_prices()
        data_cache["cme_wheat"] = fetch_cme_wheat_prices()
        data_cache["cme_corn"] = fetch_cme_corn_prices()
        data_cache["cme_rapeseed"] = fetch_cme_rapeseed_prices()
        return jsonify({
            "status": "updated",
            "wheat": len(data_cache["wheat"]),
            "corn": len(data_cache["corn"]),
            "rapeseed": len(data_cache["rapeseed"]),
            "cme_wheat": len(data_cache["cme_wheat"]),
            "cme_corn": len(data_cache["cme_corn"]),
            "cme_rapeseed": len(data_cache["cme_rapeseed"])
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    print("🚀 API server running at http://localhost:5000")
    app.run(debug=True, host="0.0.0.0", port=5050)
