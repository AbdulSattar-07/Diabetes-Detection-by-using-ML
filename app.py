import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import accuracy_score
import streamlit as st

# Collecting Data
dataset = pd.read_csv("diabetes.csv")

X = dataset.drop(columns="Outcome", axis=1)
Y = dataset["Outcome"]

scaler = StandardScaler()
scaler.fit(X)
X = scaler.transform(X)

# Train test split data
X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, test_size=0.2, stratify=Y, random_state=2
)

classifier = svm.SVC(kernel="linear")
classifier.fit(X_train, Y_train)

# ------------------ Streamlit App ------------------

st.title("🩺 Diabetes Prediction System")

st.write("### ℹ️ Please enter the following 8 medical values to check diabetes prediction.")

# 8 input fields with sample ranges
Pregnancies = st.number_input("Pregnancies (e.g., 0 - 17)", min_value=0, max_value=20, step=1)
Glucose = st.number_input("Glucose Level (mg/dL) (e.g., 70 - 200)", min_value=0, max_value=300, step=1)
BloodPressure = st.number_input("Blood Pressure (mm Hg) (e.g., 60 - 120)", min_value=0, max_value=200, step=1)
SkinThickness = st.number_input("Skin Thickness (mm) (e.g., 10 - 50)", min_value=0, max_value=100, step=1)
Insulin = st.number_input("Insulin Level (mu U/ml) (e.g., 15 - 276)", min_value=0, max_value=900, step=1)
BMI = st.number_input("BMI (Body Mass Index) (e.g., 18 - 50)", min_value=0.0, max_value=70.0, step=0.1, format="%.1f")
DiabetesPedigree = st.number_input("Diabetes Pedigree Function (e.g., 0.1 - 2.5)", min_value=0.0, max_value=3.0, step=0.01, format="%.2f")
Age = st.number_input("Age (years) (e.g., 21 - 80)", min_value=0, max_value=120, step=1)

# Store history
if "history" not in st.session_state:
    st.session_state["history"] = []

if st.button("🔍 Predict Diabetes"):
    input_data = [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigree, Age]
    input_data_as_array = np.asarray(input_data).reshape(1, -1)
    std_input_data = scaler.transform(input_data_as_array)
    
    prediction = classifier.predict(std_input_data)
    
    if prediction[0] == 0:
        result = "🟢 The person is **Non-Diabetic**"
    else:
        result = "🔴 The person is **Diabetic**"
    
    st.success(result)
    
    # Save history
    st.session_state["history"].append({"Input": input_data, "Result": result})

# Show history
if st.session_state["history"]:
    st.write("### 📜 Prediction History")
    for idx, entry in enumerate(st.session_state["history"], 1):
        st.write(f"**{idx}. Input:** {entry['Input']} → **{entry['Result']}**")

# streamlit run app.py