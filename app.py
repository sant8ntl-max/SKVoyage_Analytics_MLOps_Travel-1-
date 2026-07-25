"""Flask REST API serving the flight price prediction model."""
import pickle
import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)

with open("artifacts/flight_price_model.pkl", "rb") as f:
    artifact = pickle.load(f)

model = artifact["model"]
encoders = artifact["encoders"]
feature_cols = artifact["feature_cols"]


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/predict", methods=["POST"])
def predict():
    """
    Expected JSON body:
    {
      "from": "Recife (PE)", "to": "Florianopolis (SC)",
      "flightType": "firstClass", "agency": "FlyingDrops",
      "time": 1.76, "distance": 676.53,
      "month": 9, "dayofweek": 3
    }
    """
    payload = request.get_json(force=True)
    try:
        row = {
            "time": payload["time"],
            "distance": payload["distance"],
            "from_enc": encoders["from"].transform([payload["from"]])[0],
            "to_enc": encoders["to"].transform([payload["to"]])[0],
            "flightType_enc": encoders["flightType"].transform([payload["flightType"]])[0],
            "agency_enc": encoders["agency"].transform([payload["agency"]])[0],
            "month": payload["month"],
            "dayofweek": payload["dayofweek"],
        }
        X = pd.DataFrame([row])[feature_cols]
        price = float(model.predict(X)[0])
        return jsonify({"predicted_price": round(price, 2)})
    except KeyError as e:
        return jsonify({"error": f"Missing field: {e}"}), 400
    except ValueError as e:
        return jsonify({"error": f"Unknown category: {e}"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
