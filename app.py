import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier 

# --- Load dataset ---
data = pd.read_csv("food_packaging_defects.csv")
X = data[['pressure', 'speed', 'weight']]
y = data['defect']

# --- Train model ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
model = RandomForestClassifier(random_state=42)
model.fit(X_train_scaled, y_train)

# --- App Title ---
st.title("📊 Food Packaging Defect Detection")

# --- Navigation Tabs ---
tab1, tab2, tab3 = st.tabs(["Analysis", "Prediction", "History"])

# --- Analysis Tab ---
with tab1:
    st.header("Analysis of Predictions")
    if "history" in st.session_state and st.session_state["history"]:
        history_df = pd.DataFrame(st.session_state["history"])
        st.bar_chart(history_df["result"].value_counts())
    else:
        st.info("No data available yet. Make some predictions first!")

# --- Prediction Tab ---
with tab2:
    st.header("Make a Prediction")
    pressure = st.slider("Sealing Pressure", 90, 140, 120)
    speed = st.slider("Machine Speed", 55, 100, 80)
    weight = st.slider("Product Weight", 460, 530, 500)

    input_data = scaler.transform([[pressure, speed, weight]])
    prediction = model.predict(input_data)[0]

    if prediction == 1:
        st.error("⚠️ Defective Package Detected")
    else:
        st.success("✅ Package is Good")

    # Save prediction to history with limit of 15
    if "history" not in st.session_state:
        st.session_state["history"] = []

    new_entry = {
        "pressure": pressure,
        "speed": speed,
        "weight": weight,
        "result": "Defective" if prediction == 1 else "Good"
    }

    # Insert new entry at the top
    st.session_state["history"].insert(0, new_entry)

    # Keep only the latest 15 entries
    if len(st.session_state["history"]) > 15:
        st.session_state["history"] = st.session_state["history"][:15]

# --- History Tab ---
with tab3:
    st.header("Prediction History")
    if "history" in st.session_state and st.session_state["history"]:
        st.table(st.session_state["history"])
    else:
        st.info("No predictions made yet.")
