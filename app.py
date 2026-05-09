from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd
import numpy as np
import os

app = Flask(__name__)

# Load the model
try:
    model = joblib.load('rf_model.pkl')
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if not model:
        return jsonify({'error': 'Model not loaded correctly.'})

    try:
        # Get data from request
        data = request.json
        
        # Expected features in exact order
        features = ['temperature_c', 'humidity_pct', 'pressure_hpa', 'wind_speed_ms',
                    'cloud_cover_pct', 'altitude_m', 'distance_to_sea_km', 'latitude_deg',
                    'solar_radiation', 'evaporation_mm', 'rain_lag_1', 'rain_lag_3', 'rain_lag_7',
                    'soil_moisture_pct', 'monsoon_index', 'el_nino_index', 'climate_zone',
                    'sin_day', 'cos_day', 'heat_index', 'moisture_pressure',
                    'wind_cloud_interaction', 'climate_interaction', 'altitude_distance_ratio',
                    'rain_trend']
        
        # Create input array
        input_data = []
        for feature in features:
            val = float(data.get(feature, 0.0))
            input_data.append(val)
            
        # Reshape for prediction
        input_array = np.array(input_data).reshape(1, -1)
        
        # Make prediction
        prediction = model.predict(input_array)
        probability = model.predict_proba(input_array)[0][1] if hasattr(model, "predict_proba") else None
        
        result = {
            'prediction': int(prediction[0]),
            'probability': float(probability) if probability is not None else None,
            'message': 'Rain likely' if int(prediction[0]) == 1 else 'No rain expected'
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
