import streamlit as st
import plotly.graph_objects as go

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
sugar = st.number_input("Fasting Blood Sugar (mg/dL)", 70, 200, 90)
waist = st.number_input("Waist Circumference (cm)", 50, 150, 90)

smoking = st.selectbox("Do you smoke?", ["No", "Yes"])
diabetes = st.selectbox("Diabetic?", ["No", "Yes"])
activity = st.selectbox("Physical Activity Level", ["Low", "Moderate", "High"])
family_history = st.selectbox("Family History of CVD?", ["No", "Yes"])

# Derived metrics
bmi = weight / (height ** 2)
waist_height_ratio = waist / (height * 100)

# Binary encodings
sex_binary = 1 if sex == "Male" else 0
smoking_val = 1 if smoking == "Yes" else 0
diabetes_val = 1 if diabetes == "Yes" else 0
family_val = 1 if family_history == "Yes" else 0
physical_moderate = 1 if activity == "Moderate" else 0
physical_high = 1 if activity == "High" else 0

# CVD Risk Score Calculation
cvd_score = (
    0.334 +
    (0.001 * age) +
    (0.005 * sex_binary) +
    (0.190 * bmi) +
    (0.281 * waist_height_ratio) +
    (0.001 * height * 100) +  # Convert height from m to cm
    (0.048 * sbp) +
    (0.001 * dbp) +
    (0.011 * chol) +
    (0.009 * hdl) +
    (0.008 * ldl) +
    (0.000 * sugar) +
    (-0.012 * smoking_val) +
    (-0.012 * family_val) +
    (1.946 * diabetes_val) +
    (-0.014 * physical_moderate) +
    (-0.012 * physical_high)
)

# Classification thresholds
if cvd_score < 25:
    risk_level = "LOW"
elif 25 <= cvd_score < 75:
    risk_level = "INTERMEDIARY"
else:
    risk_level = "HIGH"

# Show results on button click
if st.button("💡 Predict My Risk Level"):
    st.markdown("### 🧮 Your Calculated CVD Risk Score:")
    st.info(f"**Score: {cvd_score:.2f}**")

    st.markdown("### 🧠 Your Predicted CVD Risk Level:")
    st.success(f"➡️ **{risk_level}**")

    # Color and value mapping
    color_map = {"LOW": "green", "INTERMEDIARY": "orange", "HIGH": "red"}
    #fixed_value_map = {"LOW": 25, "INTERMEDIARY": 75, "HIGH": 100}
    display_value = cvd_score

    # Gauge chart
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=display_value,
        title={'text': "CVD Risk Level Meter", 'font': {'size': 20}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkgray"},
            'bar': {'color': color_map[risk_level]},
            'steps': [
                {'range': [0, 50], 'color': 'lightgreen'},
                {'range': [50, 85], 'color': 'lightyellow'},
                {'range': [85, 100], 'color': 'lightcoral'}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': display_value
            }
        }
    ))

    st.plotly_chart(fig, use_container_width=True)
    st.caption(f"🔢 Raw score used for classification: {cvd_score:.2f}")
