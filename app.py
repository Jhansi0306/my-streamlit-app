import streamlit as st
import pandas as pd
import os
import hashlib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

# --- File to store user credentials ---
USER_FILE = "users.csv"

# Initialize user file if not exists
if not os.path.exists(USER_FILE):
    pd.DataFrame(columns=["username", "password"]).to_csv(USER_FILE, index=False)

# --- Helper functions ---
def hash_password(password):
    """Hash a password using SHA256."""
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    return pd.read_csv(USER_FILE)

def save_user(username, password):
    users = load_users()
    if username in users["username"].values:
        return False  # user already exists
    new_user = pd.DataFrame([[username, hash_password(password)]], columns=["username", "password"])
    users = pd.concat([users, new_user], ignore_index=True)
    users.to_csv(USER_FILE, index=False)
    return True

def authenticate(username, password):
    users = load_users()
    hashed_pw = hash_password(password)
    match = users[(users["username"] == username) & (users["password"] == hashed_pw)]
    return not match.empty

# --- Authentication state ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "current_user" not in st.session_state:
    st.session_state["current_user"] = None
if "signup" not in st.session_state:
    st.session_state["signup"] = False

# --- Special users (admins) ---
ADMIN_USERS = ["manne", "teammate"]  # replace with your actual usernames

# --- Login Page ---
def login_page():
    st.title("🔐 Login to Access the App")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticate(username, password):
            st.session_state["authenticated"] = True
            st.session_state["current_user"] = username
            st.success("Login successful! 🎉")
        else:
            st.error("Invalid username or password")

    st.write("Don't have an account?")
    if st.button("Go to Sign Up"):
        st.session_state["signup"] = True

# --- Sign Up Page ---
def signup_page():
    st.title("📝 Sign Up")
    new_username = st.text_input("Choose a Username")
    new_password = st.text_input("Choose a Password", type="password")
    if st.button("Sign Up"):
        if save_user(new_username, new_password):
            st.success("Account created successfully! Please log in.")
            st.session_state["signup"] = False
        else:
            st.error("Username already exists. Please choose another.")

    if st.button("Back to Login"):
        st.session_state["signup"] = False

# --- Dashboard ---
def app_dashboard():
    st.title("📊 Food Packaging Defect Detection Dashboard")

    # Logout button
    if st.button("Logout"):
        st.session_state["authenticated"] = False
        st.session_state["current_user"] = None
        st.success("You have been logged out.")

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
    if st.session_state["signup"]:
        signup_page()
    else:
        login_page()
else:
    # Restrict dashboard access
    if st.session_state["current_user"] in ADMIN_USERS:
        app_dashboard()
    else:
        st.warning("You are logged in, but only admins can view the dashboard.")
