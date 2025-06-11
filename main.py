from flask import Flask, request, jsonify, render_template
import pandas as pd
import joblib
from predict_request import PredictRequest
from pydantic import ValidationError
from flask_cors import CORS
import os

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Load model and classes
model = joblib.load("model/lightgbm_model.pkl")
with open("model/class.txt", "r") as f:
    class_names = [line.strip() for line in f.readlines()]

@app.route("/api/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the model API!"})

@app.route("/api/predict/", methods=["POST"])
def predict():
    try:
        input_data = request.json

        # Validate request using Pydantic
        validated = PredictRequest(**input_data)
        input_data = validated.dict()

        # Base features
        age = input_data["age"]
        height = input_data["height"]
        weight = input_data["weight"]
        fcvc = float(input_data["fcvc"])
        ncp = float(input_data["ncp"])
        ch2o = float(input_data["ch2o"])
        faf = float(input_data["faf"])
        tue = float(input_data["tue"])

        # Derived features
        bmi = weight / ((height / 100) ** 2)
        meal_habit = fcvc * ncp
        activity_balance = faf - tue

        # One-hot encoding
        gender_male = 1 if input_data["gender"] == "Male" else 0
        family_history_yes = 1 if input_data["is_family_history_with_overweight"] else 0
        favc_yes = 1 if input_data["favc"] else 0
        smoke_yes = 1 if input_data["smoke"] else 0
        scc_yes = 1 if input_data["scc"] else 0

        caec_frequently = 1 if input_data["caec"] == "Frequently" else 0
        caec_sometimes = 1 if input_data["caec"] == "Sometimes" else 0
        caec_no = 1 if input_data["caec"] == "no" else 0

        calc_frequently = 1 if input_data["calc"] == "Frequently" else 0
        calc_sometimes = 1 if input_data["calc"] == "Sometimes" else 0
        calc_no = 1 if input_data["calc"] == "no" else 0

        mtrans_bike = 1 if input_data["mtrans"] == "Bike" else 0
        mtrans_motorbike = 1 if input_data["mtrans"] == "Motorbike" else 0
        mtrans_public_transportation = 1 if input_data["mtrans"] == "Public Transportation" else 0
        mtrans_walking = 1 if input_data["mtrans"] == "Walking" else 0

        model_input = {
            "Age": age,
            "FCVC": fcvc,
            "NCP": ncp,
            "CH2O": ch2o,
            "FAF": faf,
            "TUE": tue,
            "Meal_Habit": meal_habit,
            "Activity_Balance": activity_balance,
            "BMI": bmi,

            "Gender_Male": gender_male,
            "family_history_with_overweight_yes": family_history_yes,
            "FAVC_yes": favc_yes,
            "CAEC_Frequently": caec_frequently,
            "CAEC_Sometimes": caec_sometimes,
            "CAEC_no": caec_no,
            "SMOKE_yes": smoke_yes,
            "SCC_yes": scc_yes,
            "CALC_Frequently": calc_frequently,
            "CALC_Sometimes": calc_sometimes,
            "CALC_no": calc_no,
            "MTRANS_Bike": mtrans_bike,
            "MTRANS_Motorbike": mtrans_motorbike,
            "MTRANS_Public_Transportation": mtrans_public_transportation,
            "MTRANS_Walking": mtrans_walking,
        }

        df_input = pd.DataFrame([model_input])
        prediction = model.predict(df_input)[0]
        class_name = class_names[prediction]
        probabilities = model.predict_proba(df_input)[0]

        return jsonify({
            "success": True,
            "data": {
                "predicted_class": int(prediction),
                "class_name": class_name,
                "class_probabilities": probabilities.tolist()
            }
        })

    except ValidationError as e:
        return jsonify({"success": False, "error": e.errors()}), 422
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=False, use_reloader=False, host="0.0.0.0", port=port)
