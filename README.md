# Rainfall Prediction App

This is a Flask-based web application that predicts the likelihood of rainfall using a pre-trained Random Forest machine learning model.

## Features

*   **Machine Learning Model:** Utilizes a Random Forest classifier (`rf_model.pkl`) to make accurate predictions based on a comprehensive set of weather and geographical features.
*   **Web Interface:** A user-friendly web interface to easily input current weather metrics and receive real-time predictions.
*   **API Endpoint:** A RESTful API endpoint (`/predict`) that accepts JSON payloads with weather features and returns a prediction along with its probability.
*   **Deployment Ready:** Configured with a `Procfile` and `gunicorn` for seamless deployment on platforms like Heroku.

## Input Features

The model expects the following 25 features for prediction:

*   **Weather Metrics:** Temperature (°C), Humidity (%), Pressure (hPa), Wind Speed (m/s), Cloud Cover (%)
*   **Geographical Data:** Altitude (m), Distance to Sea (km), Latitude (deg)
*   **Solar & Water Data:** Solar Radiation, Evaporation (mm), Soil Moisture (%)
*   **Historical Data:** Rain Lag (1 day, 3 days, 7 days), Rain Trend
*   **Indices & Interactions:** Monsoon Index, El Nino Index, Climate Zone, Heat Index, Moisture Pressure, Wind-Cloud Interaction, Climate Interaction, Altitude-Distance Ratio
*   **Temporal Features:** sin_day, cos_day

## Installation and Setup

### Prerequisites

*   Python 3.8+
*   pip (Python package installer)

### Local Setup

1.  **Clone or navigate to the repository:**
    ```bash
    cd "rainfall pred"
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    venv\Scripts\activate  # On Windows
    # source venv/bin/activate  # On macOS/Linux
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Flask development server:**
    ```bash
    python app.py
    ```

5.  **Access the application:**
    Open your web browser and navigate to `http://127.0.0.1:5000/`.

## API Usage

You can interact with the prediction model programmatically via the `/predict` endpoint.

**Endpoint:** `POST /predict`
**Content-Type:** `application/json`

**Example Request:**
```json
{
  "temperature_c": 28.5,
  "humidity_pct": 75.0,
  "pressure_hpa": 1012.0,
  "wind_speed_ms": 5.2,
  "cloud_cover_pct": 60.0,
  "altitude_m": 150.0,
  "distance_to_sea_km": 50.0,
  "latitude_deg": 35.0,
  "solar_radiation": 400.0,
  "evaporation_mm": 5.0,
  "rain_lag_1": 0.0,
  "rain_lag_3": 12.0,
  "rain_lag_7": 25.0,
  "soil_moisture_pct": 45.0,
  "monsoon_index": 0.5,
  "el_nino_index": 0.1,
  "climate_zone": 2.0,
  "sin_day": 0.8,
  "cos_day": 0.6,
  "heat_index": 30.0,
  "moisture_pressure": 15.0,
  "wind_cloud_interaction": 300.0,
  "climate_interaction": 5.0,
  "altitude_distance_ratio": 3.0,
  "rain_trend": 0.2
}
```

**Example Response:**
```json
{
  "message": "Rain likely",
  "prediction": 1,
  "probability": 0.85
}
```

## Technologies Used

*   **Backend Framework:** Flask
*   **Machine Learning:** scikit-learn, joblib, NumPy, Pandas
*   **Frontend:** HTML, CSS, JavaScript (via `templates/index.html`)
*   **Production Server:** Gunicorn
