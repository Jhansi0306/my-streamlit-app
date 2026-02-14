
import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Title
st.title("Food Packaging Defect Detection")
st.write("This app uses machine learning to detect defects in food packaging based on pressure, speed, and weight.")

# Load dataset
data = pd.read_csv("food_packaging_defects.csv")
st.subheader("Dataset Preview")
st.write(data.head())

# Split features and labels
X = data[['pressure', 'speed', 'weight']]
y = data['defect']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train Random Forest
model = RandomForestClassifier(random_state=42)
model.fit(X_train_scaled, y_train)

# Evaluate
y_pred = model.predict(X_test_scaled)
st.subheader("Model Performance")
st.text(classification_report(y_test, y_pred))

# User input for prediction
st.subheader("Try Your Own Values")
pressure = st.slider("Sealing Pressure", 90, 140, 120)
speed = st.slider("Machine Speed", 55, 100, 80)
weight = st.slider("Product Weight", 460, 530, 500)

input_data = scaler.transform([[pressure, speed, weight]])
prediction = model.predict(input_data)[0]

if prediction == 1:
    st.error("⚠️ Defective Package Detected")
else:
    st.success("✅ Package is Good")
