import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

# --- Dummy user database ---
USER_CREDENTIALS = {
    "admin": "password123",
    "user": "mypassword"
}

# --- Authentication ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

def login():
    st.title("🔐 Login to Access the App")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state["authenticated"] = True
            st.success("Login successful! 🎉")
        else:
            st.error("Invalid username or password")

def app_dashboard():
    st.title("📊 Food Packaging Defect Detection Dashboard")

    # Tabs navigation
    tab1, tab2, tab3 = st.tabs(["Analysis", "Prediction", "History"])

    # Analysis Tab
    with tab1:
        st.header("Analysis of Predictions")
        if "history" in st.session_state and st.session_state["history"]:
            history_df = pd.DataFrame(st.session_state["history"])
            st.bar_chart(history_df["result"].value_counts())
        else:
            st.info("No data available yet. Make some predictions first!")

    # Prediction Tab
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

        if "history" not in st.session_state:
            st.session_state["history"] = []
        st.session_state["history"].append(
            {"pressure": pressure, "speed": speed, "weight": weight,
             "result": "Defective" if prediction == 1 else "Good"}
        )

    # History Tab
    with tab3:
        st.header("Prediction History")
        if "history" in st.session_state and st.session_state["history"]:
            st.table(st.session_state["history"])
        else:
            st.info("No predictions made yet.")

# --- ML Model Setup ---
data = pd.read_csv("food_packaging_defects.csv")
X = data[['pressure', 'speed', 'weight']]
y = data['defect']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
model = RandomForestClassifier(random_state=42)
model.fit(X_train_scaled, y_train)

# --- Run App ---
if not st.session_state["authenticated"]:
    login()
else:
    app_dashboard()
