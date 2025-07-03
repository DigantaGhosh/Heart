
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go

# Load model and encoders
clf = joblib.load("cvd_classifier_model.pkl")
label_encoder = joblib.load("risk_level_encoder.pkl")
feature_order = joblib.load("feature_order.pkl")

st.set_page_config(page_title="CVD Risk Predictor", layout="centered")
st.title("🫀 CVD Risk Level Predictor")
st.markdown("Quickly check your cardiovascular risk based on medical & lifestyle inputs.")
st.markdown("----")

# User inputs
st.subheader("🔍 Enter Your Details")
age = st.number_input("Age", 18, 100, 45)
sex = st.selectbox("Sex", ["Male", "Female"])
weight = st.number_input("Weight (kg)", 30.0, 150.0, 70.0)
height = st.number_input("Height (m)", 1.3, 2.2, 1.7)
sbp = st.number_input("Systolic BP", 90, 200, 120)
dbp = st.number_input("Diastolic BP", 60, 130, 80)
chol = st.number_input("Total Cholesterol (mg/dL)", 100, 400, 190)
hdl = st.number_input("HDL (mg/dL)", 20, 100, 45)
ldl = st.number_input("Estimated LDL (mg/dL)", 50, 250, 130)
sugar = st.number_input("Fasting Blood Sugar", 70, 200, 90)
waist = st.number_input("Waist Circumference (cm)", 50, 150, 90)

smoking = st.selectbox("Do you smoke?", ["No", "Yes"])
diabetes = st.selectbox("Diabetic?", ["No", "Yes"])
activity = st.selectbox("Physical Activity Level", ["Low", "Moderate", "High"])
family_history = st.selectbox("Family History of CVD?", ["No", "Yes"])

# Derived metrics
bmi = weight / (height ** 2)
waist_height_ratio = waist / (height * 100)

# Prepare input
input_dict = {
    "Age": age,
    "Sex": 1 if sex == "Male" else 0,
    "Weight (kg)": weight,
    "Height (m)": height,
    "Systolic BP": sbp,
    "Diastolic BP": dbp,
    "Total Cholesterol (mg/dL)": chol,
    "HDL (mg/dL)": hdl,
    "Fasting Blood Sugar (mg/dL)": sugar,
    "Smoking Status": 1 if smoking == "Yes" else 0,
    "Diabetes Status": 1 if diabetes == "Yes" else 0,
    "Physical Activity Level": {"Low": 0, "Moderate": 1, "High": 2}[activity],
    "Family History of CVD": 1 if family_history == "Yes" else 0,
    "Abdominal Circumference (cm)": waist,
    "Estimated LDL (mg/dL)": ldl,
    "BMI": bmi,
    "Waist-to-Height Ratio": waist_height_ratio
}

input_df = pd.DataFrame([input_dict])
input_df = input_df.reindex(columns=feature_order)

# Predict
if st.button("💡 Predict My Risk Level"):
    pred = clf.predict(input_df)[0]
    result = label_encoder.inverse_transform([pred])[0]
    st.markdown("### 🧠 Your Predicted CVD Risk Level:")
    st.success(f"➡️ **{result}**")

    # Risk meter
    color_map = {"LOW": "green", "INTERMEDIARY": "orange", "HIGH": "red"}
    value_map = {"LOW": 25, "INTERMEDIARY": 50, "HIGH": 85}
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value_map.get(result.upper(), 50),
        title={'text': "Risk Meter", 'font': {'size': 20}},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': color_map.get(result.upper(), "gray")},
            'steps': [
                {'range': [0, 35], 'color': 'lightgreen'},
                {'range': [35, 70], 'color': 'lightyellow'},
                {'range': [70, 100], 'color': 'lightcoral'}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': value_map.get(result.upper(), 50)
            }
        }
    ))
    st.plotly_chart(fig, use_container_width=True)
