# --- Run App ---
if not st.session_state["authenticated"]:
    if st.session_state["signup"]:
        signup_page()
    else:
        login_page()
else:
    # After login, show dashboard
    if st.session_state["current_user"] in ADMIN_USERS:
        # Admins see Analysis, Prediction, History, and ADMIN tab
        app_dashboard()
    else:
        # Normal users see Analysis, Prediction, History tabs only
        st.title("📊 Food Packaging Defect Detection Dashboard")

        # Logout button
        if st.button("Logout"):
            st.session_state["authenticated"] = False
            st.session_state["current_user"] = None
            st.success("You have been logged out.")

        # Tabs navigation for normal users
        tab1, tab2, tab3 = st.tabs(["Analysis", "Prediction", "History"])

        with tab1:
            st.header("Analysis of Predictions")
            if "history" in st.session_state and st.session_state["history"]:
                history_df = pd.DataFrame(st.session_state["history"])
                st.bar_chart(history_df["result"].value_counts())
            else:
                st.info("No data available yet. Make some predictions first!")

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

        with tab3:
            st.header("Prediction History")
            if "history" in st.session_state and st.session_state["history"]:
                st.table(st.session_state["history"])
            else:
                st.info("No predictions made yet.")
