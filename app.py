import streamlit as st
import pandas as pd
import os
import hashlib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

# --- Initialize session state safely ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "current_user" not in st.session_state:
    st.session_state["current_user"] = None
if "signup" not in st.session_state:
    st.session_state["signup"] = False
if "history" not in st.session_state:
    st.session_state["history"] = []

# --- File to store user credentials ---
USER_FILE = "users.csv"

# Initialize user file if not exists
if not os.path.exists(USER_FILE):
    pd.DataFrame(columns=["username", "password"]).to_csv(USER_FILE, index=False)

# (rest of your helper functions and dashboard code here...)
