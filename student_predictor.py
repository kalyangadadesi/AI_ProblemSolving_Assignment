import streamlit as st
import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error

DATA_FILE = "student_data.csv"

def generate_synthetic_data():
    """Generates synthetic student performance data with 4 features and 1 target."""
    np.random.seed(42)
    n_samples = 200
    
    # 4 Input Features
    hours_studied = np.random.uniform(1, 10, n_samples)
    attendance_rate = np.random.uniform(50, 100, n_samples)
    previous_score = np.random.uniform(40, 100, n_samples)
    assignments_completed = np.random.randint(0, 10, n_samples)
    
    # Introduce some random missing values to test preprocessing
    for i in range(10):
        hours_studied[np.random.randint(0, n_samples)] = np.nan
        attendance_rate[np.random.randint(0, n_samples)] = np.nan
        
    # Target Variable: Exam Score
    # Base formula with some noise
    exam_score = (
        (hours_studied * 3.5) + 
        (attendance_rate * 0.3) + 
        (previous_score * 0.4) + 
        (assignments_completed * 1.5) + 
        np.random.normal(0, 5, n_samples)
    )
    
    # Cap scores at 100
    exam_score = np.clip(exam_score, 0, 100)
    
    df = pd.DataFrame({
        "Hours_Studied": hours_studied,
        "Attendance_Rate": attendance_rate,
        "Previous_Score": previous_score,
        "Assignments_Completed": assignments_completed,
        "Exam_Score": exam_score
    })
    
    df.to_csv(DATA_FILE, index=False)
    return df

st.set_page_config(page_title="Student Performance Predictor", layout="wide", page_icon="📈")

# === VIBRANT DASHBOARD CSS ===
st.markdown("""
<style>
    /* Sci-Fi Dashboard Background */
    .stApp {
        background: radial-gradient(circle at top right, #0a0a2a, #000000);
        color: #e0e6ed;
        font-family: 'Inter', sans-serif;
    }
    
    /* Neon Gradient Titles */
    h1 {
        background: -webkit-linear-gradient(45deg, #00f2fe, #4facfe, #00f2fe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900 !important;
        text-shadow: 0px 0px 15px rgba(0, 242, 254, 0.3);
    }
    h2, h3 {
        color: #4facfe !important;
        text-shadow: 0px 0px 10px rgba(79, 172, 254, 0.2);
    }
    
    /* Glowing Metrics Cards */
    div[data-testid="metric-container"] {
        background: rgba(0, 242, 254, 0.05);
        border: 1px solid rgba(79, 172, 254, 0.4);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 0 20px rgba(0, 242, 254, 0.15), inset 0 0 10px rgba(0, 242, 254, 0.05);
        transition: transform 0.3s ease;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 25px rgba(0, 242, 254, 0.3);
    }
    
    /* Glowing Buttons */
    div.stButton > button, div[data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(45deg, #4facfe, #00f2fe) !important;
        color: #000 !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        box-shadow: 0 8px 25px rgba(0, 242, 254, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    div.stButton > button:hover, div[data-testid="stFormSubmitButton"] > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 30px rgba(0, 242, 254, 0.6) !important;
        color: #000 !important;
    }
    
    /* Input Fields */
    div[data-testid="stNumberInput"] input {
        border-radius: 8px !important;
        border: 1px solid rgba(79, 172, 254, 0.5) !important;
        background-color: rgba(10, 10, 42, 0.8) !important;
        color: #00f2fe !important;
        font-weight: bold !important;
    }
    div[data-testid="stNumberInput"] input:focus {
        box-shadow: 0 0 15px rgba(0, 242, 254, 0.5) !important;
        border-color: #00f2fe !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("📈 Student Performance Predictor (ML)")

st.markdown("""
<div style="padding: 15px; border-left: 5px solid #00f2fe; background: rgba(0,242,254,0.1); border-radius: 0 10px 10px 0; margin-bottom: 2rem;">
This advanced AI dashboard predicts student exam scores based on 4 features: 
<b style="color:#00f2fe;">Hours Studied</b>, <b style="color:#00f2fe;">Attendance Rate</b>, <b style="color:#00f2fe;">Previous Score</b>, and <b style="color:#00f2fe;">Assignments Completed</b>.
</div>
""", unsafe_allow_html=True)

# --- 1. Data Loading & Preprocessing ---
st.header("1. Dataset")
uploaded_file = st.file_uploader("Upload your own CSV dataset (optional)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("Custom dataset loaded successfully!")
else:
    if not os.path.exists(DATA_FILE):
        df = generate_synthetic_data()
    else:
        df = pd.read_csv(DATA_FILE)
    st.info("Using default synthetic dataset.")

st.write("Edit the Raw Data below (changes will instantly retrain the ML model!):")
df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

# Preprocessing
st.subheader("Data Preprocessing")
initial_missing = df.isnull().sum().sum()
if initial_missing > 0:
    st.warning(f"Found {initial_missing} missing values. Handling them by filling with column means...")
    df.fillna(df.mean(), inplace=True)
    st.success("Missing values handled.")
else:
    st.success("No missing values found in the dataset.")

# Ensure required columns exist
required_features = ["Hours_Studied", "Attendance_Rate", "Previous_Score", "Assignments_Completed"]
target = "Exam_Score"

if not all(col in df.columns for col in required_features + [target]):
    st.error(f"Dataset must contain the following columns: {required_features + [target]}")
    st.stop()

# --- 2. Model Training ---
st.header("2. Model Training")

X = df[required_features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predictions & Metrics
y_pred = model.predict(X_test)
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)

col1, col2 = st.columns(2)
col1.metric("R² Score", f"{r2:.4f}", help="Closer to 1 is better.")
col2.metric("Mean Absolute Error", f"{mae:.2f}", help="Lower is better.")

st.write("Model trained successfully using Random Forest Regressor!")

# --- 3. Predictions ---
st.header("3. Predict Student Score")
st.write("Input student details to predict their final exam score.")

with st.form("prediction_form"):
    c1, c2 = st.columns(2)
    with c1:
        hours = st.number_input("Hours Studied (per week)", min_value=0.0, max_value=40.0, value=5.0)
        attendance = st.number_input("Attendance Rate (%)", min_value=0.0, max_value=100.0, value=85.0)
    with c2:
        prev_score = st.number_input("Previous Score", min_value=0.0, max_value=100.0, value=75.0)
        assignments = st.number_input("Assignments Completed", min_value=0, max_value=20, value=5)
        
    submit = st.form_submit_button("Predict Exam Score")
    
if submit:
    input_data = pd.DataFrame({
        "Hours_Studied": [hours],
        "Attendance_Rate": [attendance],
        "Previous_Score": [prev_score],
        "Assignments_Completed": [assignments]
    })
    
    prediction = model.predict(input_data)[0]
    prediction = min(max(prediction, 0), 100) # Clamp between 0-100
    
    st.success(f"### Predicted Exam Score: {prediction:.2f} / 100")
