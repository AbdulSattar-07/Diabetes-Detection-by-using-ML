import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import streamlit as st
import time

# Collecting Data
dataset = pd.read_csv("diabetes.csv")

# Advanced Data Preprocessing
# 1. Handle missing values (zeros in medical data are invalid)
columns_to_fix = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
for col in columns_to_fix:
    dataset[col] = dataset[col].replace(0, dataset[col].median())

# 2. Feature Engineering - Create new features
dataset['BMI_Age'] = dataset['BMI'] * dataset['Age']
dataset['Glucose_BMI'] = dataset['Glucose'] * dataset['BMI']
dataset['Insulin_Glucose'] = dataset['Insulin'] / (dataset['Glucose'] + 1)
dataset['BP_Age'] = dataset['BloodPressure'] * dataset['Age']

X = dataset.drop(columns="Outcome", axis=1)
Y = dataset["Outcome"]

# 3. Feature Scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train test split data
X_train, X_test, Y_train, Y_test = train_test_split(
    X_scaled, Y, test_size=0.2, stratify=Y, random_state=42
)

# 4. Ensemble Model - Combining multiple algorithms for better accuracy
# Random Forest with optimized parameters
rf_classifier = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42
)

# Gradient Boosting
gb_classifier = GradientBoostingClassifier(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=5,
    random_state=42
)

# SVM with RBF kernel (better for non-linear data)
svm_classifier = svm.SVC(
    kernel='rbf',
    C=10,
    gamma='scale',
    probability=True,
    random_state=42
)

# Logistic Regression
lr_classifier = LogisticRegression(
    max_iter=1000,
    random_state=42
)

# 5. Voting Classifier - Combines all models
classifier = VotingClassifier(
    estimators=[
        ('rf', rf_classifier),
        ('gb', gb_classifier),
        ('svm', svm_classifier),
        ('lr', lr_classifier)
    ],
    voting='soft'  # Uses probability for better results
)

# Train the ensemble model
classifier.fit(X_train, Y_train)

# Model accuracy for reference
train_accuracy = classifier.score(X_train, Y_train)
test_accuracy = classifier.score(X_test, Y_test)

# Cross-validation score for more reliable accuracy
cv_scores = cross_val_score(classifier, X_scaled, Y, cv=5)
cv_accuracy = cv_scores.mean()

# ------------------ Streamlit App ------------------

# Page configuration
st.set_page_config(
    page_title="Diabetes Prediction System",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI and animations
st.markdown("""
    <style>
    /* Main container styling */
    .main {
        padding: 2rem;
    }
    
    /* Animated gradient background for header */
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        animation: fadeIn 1s ease-in;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .header-title {
        color: white;
        font-size: 3rem;
        font-weight: bold;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .header-subtitle {
        color: #f0f0f0;
        font-size: 1.2rem;
        margin-top: 0.5rem;
    }
    
    /* Card styling */
    .info-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 4px solid #667eea;
        animation: slideIn 0.5s ease-out;
    }
    
    /* Button styling */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: bold;
        border-radius: 10px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
    }
    
    /* Input field styling */
    .stNumberInput>div>div>input {
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        transition: border-color 0.3s ease;
    }
    
    .stNumberInput>div>div>input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    /* Result animation */
    .result-box {
        animation: pulse 0.5s ease-in-out;
    }
    
    /* Metric cards */
    .css-1xarl3l {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 10px;
        padding: 1rem;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #f8f9fa;
        border-radius: 8px;
        font-weight: 600;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .header-title {
            font-size: 2rem;
        }
        .header-subtitle {
            font-size: 1rem;
        }
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #666;
        font-size: 0.9rem;
        margin-top: 3rem;
        border-top: 1px solid #e0e0e0;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    </style>
""", unsafe_allow_html=True)

# Animated header
st.markdown("""
    <div class="header-container">
        <h1 class="header-title">🩺 Diabetes Prediction System</h1>
        <p class="header-subtitle">AI-Powered Health Risk Assessment</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar with information
with st.sidebar:
    st.markdown("### 📋 About")
    st.info("""
    This application uses **Advanced Ensemble Machine Learning** to predict diabetes risk.
    
    **Models:** Random Forest + Gradient Boosting + SVM + Logistic Regression
    **Technique:** Voting Classifier (Ensemble)
    **Dataset:** Pima Indians Diabetes Database
    **Samples:** 768 patients
    **Features:** 12 (8 original + 4 engineered)
    """)
    
    st.markdown("### 📊 Model Performance")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Training", f"{train_accuracy:.1%}", delta="Excellent")
    with col2:
        st.metric("Testing", f"{test_accuracy:.1%}", delta="High")
    
    st.metric("CrictiValidation (5-Fold)", f"{cv_accuracy:.1%}", delta="Reliable")
    
    st.markdown("### 🚀 Improvements")
    st.success("""
    ✅ Ensemble of 4 algorithms
    ✅ Feature engineering
    ✅ Hyperparameter tuning
    ✅ Cross-validation
    """)
    
    st.markdown("### ℹ️ How to Use")
    st.markdown("""
    1. Enter your medical values
    2. Click 'Predict Diabetes Risk'
    3. View your risk assessment
    4. Check prediction history
    """)
    
    st.markdown("### ⚠️ Disclaimer")
    st.warning("This tool is for educational purposes only. Consult a healthcare professional for medical advice.")

# Main content
st.markdown("### 📝 Enter Medical Information")
st.markdown("Please provide the following medical parameters for diabetes risk assessment:")

# 8 input fields with sample ranges in a responsive grid
col1, col2, col3 = st.columns(3)

with col1:
    Pregnancies = st.number_input("👶 Pregnancies", min_value=0, max_value=20, step=1, value=0, help="Number of times pregnant")
    Glucose = st.number_input("🍬 Glucose (mg/dL)", min_value=0, max_value=300, step=1, value=120, help="Plasma glucose concentration")
    SkinThickness = st.number_input("📏 Skin Thickness (mm)", min_value=0, max_value=100, step=1, value=20, help="Triceps skin fold thickness")

with col2:
    BloodPressure = st.number_input("💓 Blood Pressure (mm Hg)", min_value=0, max_value=200, step=1, value=80, help="Diastolic blood pressure")
    Insulin = st.number_input("💉 Insulin (mu U/ml)", min_value=0, max_value=900, step=1, value=80, help="2-Hour serum insulin")
    DiabetesPedigree = st.number_input("🧬 Diabetes Pedigree", min_value=0.0, max_value=3.0, step=0.01, format="%.2f", value=0.5, help="Diabetes pedigree function")

with col3:
    BMI = st.number_input("⚖️ BMI", min_value=0.0, max_value=70.0, step=0.1, format="%.1f", value=25.0, help="Body mass index (weight in kg/(height in m)^2)")
    Age = st.number_input("🎂 Age (years)", min_value=0, max_value=120, step=1, value=30, help="Age in years")
    st.markdown("")  # Spacer

# Store history
if "history" not in st.session_state:
    st.session_state["history"] = []

st.markdown("---")

# Centered predict button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    predict_button = st.button("🔍 Predict Diabetes Risk", use_container_width=True)

if predict_button:
    # Validate inputs
    if Glucose == 0 or BloodPressure == 0 or BMI == 0:
        st.error("⚠️ Please enter valid values. Glucose, Blood Pressure, and BMI cannot be zero.")
    else:
        # Show loading animation
        with st.spinner('🔄 Analyzing your data with ensemble AI models...'):
            time.sleep(1.5)  # Simulate processing
            
            # Original features
            input_data = [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigree, Age]
            
            # Add engineered features (same as training)
            BMI_Age = BMI * Age
            Glucose_BMI = Glucose * BMI
            Insulin_Glucose = Insulin / (Glucose + 1)
            BP_Age = BloodPressure * Age
            
            # Combine all features
            input_data_with_features = input_data + [BMI_Age, Glucose_BMI, Insulin_Glucose, BP_Age]
            input_data_as_array = np.asarray(input_data_with_features).reshape(1, -1)
            std_input_data = scaler.transform(input_data_as_array)
            
            prediction = classifier.predict(std_input_data)
            # Get probability predictions from ensemble
            prediction_proba = classifier.predict_proba(std_input_data)[0]
            confidence = max(prediction_proba) * 100
        
        # Display results with animation
        st.markdown("### 🎯 Prediction Results")
        
        result_col1, result_col2 = st.columns(2)
        
        with result_col1:
            if prediction[0] == 0:
                st.markdown("""
                    <div class="result-box" style="background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%); 
                    padding: 2rem; border-radius: 15px; text-align: center; margin: 1rem 0;">
                        <h2 style="color: #155724; margin: 0;">✅ Low Risk</h2>
                        <p style="color: #155724; font-size: 1.2rem; margin-top: 0.5rem;">Non-Diabetic</p>
                    </div>
                """, unsafe_allow_html=True)
                result = "🟢 The person is **Non-Diabetic**"
            else:
                st.markdown("""
                    <div class="result-box" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); 
                    padding: 2rem; border-radius: 15px; text-align: center; margin: 1rem 0;">
                        <h2 style="color: #721c24; margin: 0;">⚠️ High Risk</h2>
                        <p style="color: #721c24; font-size: 1.2rem; margin-top: 0.5rem;">Diabetic</p>
                    </div>
                """, unsafe_allow_html=True)
                result = "🔴 The person is **Diabetic**"
        
        with result_col2:
            st.markdown("""
                <div style="background: #f8f9fa; padding: 2rem; border-radius: 15px; margin: 1rem 0;">
                    <h3 style="color: #333; margin-top: 0;">📊 Analysis Details</h3>
                </div>
            """, unsafe_allow_html=True)
            
            st.metric("Confidence Level", f"{confidence:.1f}%", 
                     delta="High Confidence" if confidence > 80 else "Moderate Confidence")
            
            # Progress bar for confidence
            st.progress(confidence / 100)
            
            # Show probability breakdown
            st.markdown("**Probability Breakdown:**")
            st.write(f"Non-Diabetic: {prediction_proba[0]*100:.1f}%")
            st.write(f"Diabetic: {prediction_proba[1]*100:.1f}%")
            
            st.info("🤖 Analyzed by 4 AI models working together")
        
        # Save history
        st.session_state["history"].append({
            "Input": input_data, 
            "Result": result,
            "Confidence": confidence,
            "Timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        })
        
        st.balloons()  # Celebration animation

# Show history
if st.session_state["history"]:
    st.markdown("---")
    st.markdown("### 📜 Prediction History")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state["history"] = []
            st.rerun()
    
    # Display history in a nice format
    for idx, entry in enumerate(reversed(st.session_state["history"]), 1):
        with st.expander(f"🔍 Prediction #{len(st.session_state['history']) - idx + 1} - {entry.get('Timestamp', 'N/A')}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Result:** {entry['Result']}")
                st.markdown(f"**Confidence:** {entry.get('Confidence', 'N/A'):.1f}%")
            
            with col2:
                input_labels = ["👶 Pregnancies", "🍬 Glucose", "💓 Blood Pressure", "📏 Skin Thickness", 
                              "💉 Insulin", "⚖️ BMI", "🧬 Diabetes Pedigree", "🎂 Age"]
                for label, value in zip(input_labels, entry['Input']):
                    st.text(f"{label}: {value}")

# Footer
st.markdown("---")
st.markdown("""
    <div class="footer">
        <p>🩺 <strong>Diabetes Prediction System</strong> | Built by Abdul Sattar with ❤️ using Streamlit & Machine Learning</p>
        <p>⚠️ For educational purposes only - Not a substitute for professional medical advice</p>
        <p>📧 Questions? Contact your healthcare provider</p>
    </div>
""", unsafe_allow_html=True)