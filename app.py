import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

# Load dataset
data = pd.read_csv("food_packaging_defects.csv")
X = data[['pressure', 'speed', 'weight']]
y = data['defect']

# Train model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = RandomForestClassifier(random_state=42)
model.fit(X_train_scaled, y_train)

# Sidebar navigation (Analysis first, then Prediction, then History)
section = st.sidebar.radio("Navigate", ["Analysis", "Prediction", "History"])

# Analysis Section
if section == "Analysis":
    st.title("Analysis of Predictions")
    if "history" in st.session_state and st.session_state["history"]:
        history_df = pd.DataFrame(st.session_state["history"])
        st.write("Distribution of Predictions:")
        st.bar_chart(history_df["result"].value_counts())
    else:
        st.info("No data available for analysis yet. Make some predictions first!")

# Prediction Section
elif section == "Prediction":
    st.title("Food Packaging Defect Detection")
    st.subheader("Make a Prediction")

    pressure = st.slider("Sealing Pressure", 90, 140, 120)
    speed = st.slider("Machine Speed", 55, 100, 80)
    weight = st.slider("Product Weight", 460, 530, 500)

    input_data = scaler.transform([[pressure, speed, weight]])
    prediction = model.predict(input_data)[0]

    if prediction == 1:
        st.error("⚠️ Defective Package Detected")
    else:
        st.success("✅ Package is Good")

    # Save prediction to history
    if "history" not in st.session_state:
        st.session_state["history"] = []
    st.session_state["history"].append(
        {"pressure": pressure, "speed": speed, "weight": weight, "result": "Defective" if prediction == 1 else "Good"}
    )

# History Section
elif section == "History":
    st.title("Prediction History")
    if "history" in st.session_state and st.session_state["history"]:
        st.table(st.session_state["history"])
    else:
        st.info("No predictions made yet.")
