# --- Run App ---
if not st.session_state["authenticated"]:
    if st.session_state["signup"]:
        signup_page()
    else:
        login_page()
else:
    # After login, show dashboard for everyone
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
            speed = st.slider
