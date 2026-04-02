from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import pandas as pd
import os

app = Flask(__name__)

# Load IMPROVED model with better parameters
with open("hospital_stay_model.pkl", "rb") as file:
    model = pickle.load(file)

# Load features
with open("model_features.pkl", "rb") as file:
    feature_names = pickle.load(file)

# Load scaler
with open("model_scaler.pkl", "rb") as file:
    scaler = pickle.load(file)

print("✅ IMPROVED Model loaded! (Better predictions)")
print(f"📊 Features ({len(feature_names)}): {feature_names}")

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/predictor")
def predictor():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get input values
        age = int(request.form.get("age", 50))
        severity = int(request.form.get("severity", 2))
        admission_type = int(request.form.get("admission", 2))
        deposit = float(request.form.get("deposit", 2000))
        visitors = int(request.form.get("visitors", 2))
        
        # Additional features
        bed_grade = int(request.form.get("bed_grade", 2))
        extra_rooms = int(request.form.get("available_extra_rooms", 10))
        department = int(request.form.get("department", 1))
        ward_type = int(request.form.get("ward_type", 1))
        city_code_patient = float(request.form.get("city_code_patient", 1.0))
        
        # Feature engineering
        severity_admission = severity * admission_type
        age_severity = age * severity
        deposit_per_visitor = deposit / (visitors + 1)
        visitor_age_ratio = visitors / ((age / 20) + 1)
        room_bed_ratio = extra_rooms / (bed_grade + 1)
        
        # Create feature dict
        features_dict = {
            'Age': age,
            'Severity_of_Illness': severity,
            'Type_of_Admission': admission_type,
            'Visitors_with_Patient': visitors,
            'Admission_Deposit': deposit,
            'Bed_Grade': bed_grade,
            'Available_Extra_Rooms_in_Hospital': extra_rooms,
            'Department': department,
            'Ward_Type': ward_type,
            'City_Code_Patient': city_code_patient,
            'Severity_Admission': severity_admission,
            'Age_Severity': age_severity,
            'Deposit_per_Visitor': deposit_per_visitor,
            'Visitor_Age_Ratio': visitor_age_ratio,
            'Room_Bed_Ratio': room_bed_ratio
        }
        
        # Convert to DataFrame
        features_df = pd.DataFrame([features_dict])[feature_names]
        
        # Scale features
        features_scaled = scaler.transform(features_df)
        
        # Predict
        prediction = model.predict(features_scaled)[0]
        
        # CLIP to realistic range [0, 100]
        prediction = np.clip(prediction, 0, 100)
        
        # Round to nearest integer
        prediction = int(round(prediction))
        
        # Ensure minimum 1 day
        prediction = max(1, prediction)
        
        return render_template("result.html", prediction=prediction)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route("/analytics")
def analytics():
    return render_template("analytics_enhanced.html")

@app.route("/api/analytics-data")
def analytics_data():
    try:
        df = pd.read_csv("HospitalSynthetic1_cleaned (1).csv")
        data = {
            'stay_distribution': df['Stay'].value_counts().to_dict(),
            'severity_stay': df.groupby('Severity_of_Illness')['Stay'].mean().to_dict(),
            'admission_stay': df.groupby('Type_of_Admission')['Stay'].mean().to_dict(),
            'age_distribution': df['Age'].tolist(),
            'deposit_stay_correlation': df[['Admission_Deposit', 'Stay']].to_dict('records'),
            'visitors_stay': df.groupby('Visitors_with_Patient')['Stay'].mean().to_dict(),
            'total_records': len(df),
            'avg_stay': float(df['Stay'].mean()),
            'min_stay': int(df['Stay'].min()),
            'max_stay': int(df['Stay'].max())
        }
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/about")
def about():
    return render_template("about.html")

@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template("500.html"), 500

if __name__ == "__main__":
    # Get port from environment variable or default to 5000
    port = int(os.environ.get("PORT", 5000))
    is_production = os.environ.get("FLASK_ENV") == "production"
    # Run on all network interfaces (0.0.0.0) so mobile can connect
    app.run(host="0.0.0.0", port=port, debug=not is_production)
