import json
import os
import joblib
import numpy as np

FEATURES = [
    'temperature_c', 'humidity_pct', 'pressure_hpa', 'wind_speed_ms',
    'cloud_cover_pct', 'altitude_m', 'distance_to_sea_km', 'latitude_deg',
    'solar_radiation', 'evaporation_mm', 'rain_lag_1', 'rain_lag_3', 'rain_lag_7',
    'soil_moisture_pct', 'monsoon_index', 'el_nino_index', 'climate_zone',
    'sin_day', 'cos_day', 'heat_index', 'moisture_pressure',
    'wind_cloud_interaction', 'climate_interaction', 'altitude_distance_ratio',
    'rain_trend'
]

MODEL_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'rf_model.pkl'))
model = None
load_error = None


def load_model():
    global model, load_error
    if model is not None or load_error is not None:
        return

    try:
        model = joblib.load(MODEL_PATH)
    except Exception as exc:
        model = None
        load_error = str(exc)


def parse_body(request):
    if hasattr(request, 'json'):
        try:
            return request.json or {}
        except Exception:
            pass

    try:
        body = request.get_data().decode('utf-8')
        return json.loads(body or '{}')
    except Exception:
        return {}


def handler(request):
    load_model()
    if load_error:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': f'Model load failed: {load_error}'})
        }

    data = parse_body(request)
    if request.method == 'GET':
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'message': 'Send a POST request with JSON fields to predict.'})
        }

    try:
        input_data = [float(data.get(feature, 0.0) or 0.0) for feature in FEATURES]
        input_array = np.array(input_data).reshape(1, -1)
        prediction = model.predict(input_array)
        probability = None
        if hasattr(model, 'predict_proba'):
            probability = float(model.predict_proba(input_array)[0][1])

        result = {
            'prediction': int(prediction[0]),
            'probability': probability,
            'message': 'Rain likely' if int(prediction[0]) == 1 else 'No rain expected'
        }

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(result)
        }
    except Exception as exc:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(exc)})
        }
