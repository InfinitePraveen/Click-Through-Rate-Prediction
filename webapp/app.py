from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import joblib
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)

# Load model and scaler
model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models', 'ctr_model.pkl')
scaler_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models', 'scaler.pkl')

try:
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    print("Model and scaler loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    # Create a dummy model if not found (for demo purposes)
    from sklearn.ensemble import RandomForestClassifier
    model = RandomForestClassifier()
    scaler = None

# Feature names
feature_names = [
    'Age', 'Income', 'Time_on_Site', 'Previous_Clicks',
    'Device_Type_Num', 'Is_Tech_Ad', 'Is_Male', 'Is_Evening',
    'Engagement_Score', 'Is_Active_User', 'Is_High_Income',
    'Time_Clicks_Interaction', 'Age_Income_Ratio'
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get form data
        age = float(request.form.get('age', 35))
        income = float(request.form.get('income', 70000))
        time_on_site = float(request.form.get('time_on_site', 12.5))
        previous_clicks = float(request.form.get('previous_clicks', 25))
        device_type = int(request.form.get('device_type', 1))  # 1 for Mobile, 0 for Desktop
        ad_category = int(request.form.get('ad_category', 1))  # 1 for Tech, 0 for Lifestyle
        gender = int(request.form.get('gender', 1))  # 1 for Male, 0 for Female
        time_of_day = int(request.form.get('time_of_day', 1))  # 1 for Evening, 0 for Morning
        
        # Feature engineering
        engagement_score = time_on_site * 0.3 + previous_clicks * 0.7
        is_active_user = 1 if previous_clicks > 20 else 0
        is_high_income = 1 if income > 80000 else 0
        time_clicks_interaction = time_on_site * previous_clicks
        age_income_ratio = age / (income / 1000) if income > 0 else 0
        
        # Create feature vector
        features = pd.DataFrame([[
            age, income, time_on_site, previous_clicks,
            device_type, ad_category, gender, time_of_day,
            engagement_score, is_active_user, is_high_income,
            time_clicks_interaction, age_income_ratio
        ]], columns=feature_names)
        
        # Scale features
        if scaler:
            numerical_cols = ['Age', 'Income', 'Time_on_Site', 'Previous_Clicks', 
                              'Engagement_Score', 'Time_Clicks_Interaction', 'Age_Income_Ratio']
            features[numerical_cols] = scaler.transform(features[numerical_cols])
        
        # Predict
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0][1]
        
        # Create explanation
        explanation = generate_explanation(features, prediction, probability)
        
        return jsonify({
            'success': True,
            'prediction': int(prediction),
            'probability': round(probability * 100, 2),
            'click_probability': round(probability * 100, 2),
            'explanation': explanation
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

def generate_explanation(features, prediction, probability):
    """Generate human-readable explanation for prediction"""
    explanation = []
    
    # Get feature values
    age = features['Age'].values[0]
    income = features['Income'].values[0]
    time_on_site = features['Time_on_Site'].values[0]
    previous_clicks = features['Previous_Clicks'].values[0]
    device_type = 'Mobile' if features['Device_Type_Num'].values[0] == 1 else 'Desktop'
    ad_category = 'Technology' if features['Is_Tech_Ad'].values[0] == 1 else 'Lifestyle'
    gender = 'Male' if features['Is_Male'].values[0] == 1 else 'Female'
    time_of_day = 'Evening' if features['Is_Evening'].values[0] == 1 else 'Morning'
    
    # Build explanation
    if prediction == 1:
        explanation.append("✓ Likely to click on the ad")
    else:
        explanation.append("✗ Unlikely to click on the ad")
    
    explanation.append(f"📊 Click probability: {probability:.1%}")
    
    # Key factors
    factors = []
    if previous_clicks > 20:
        factors.append(f"High previous clicks ({previous_clicks})")
    if time_on_site > 15:
        factors.append(f"High time on site ({time_on_site} min)")
    if device_type == 'Mobile':
        factors.append("Using mobile device")
    if time_of_day == 'Evening':
        factors.append("Evening time (higher engagement)")
    if ad_category == 'Technology' and age < 40:
        factors.append("Tech ads appeal to younger users")
    if income > 80000 and ad_category == 'Technology':
        factors.append("High income + Tech ads = good match")
    
    if factors:
        explanation.append("Key factors influencing this prediction:")
        for factor in factors[:3]:  # Show top 3 factors
            explanation.append(f"  • {factor}")
    
    return explanation

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'model_loaded': model is not None})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)