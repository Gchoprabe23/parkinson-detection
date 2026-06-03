# import streamlit as st
# import requests
# import pandas as pd

# BACKEND_URL = "https://parkinson-project-1.onrender.com"
# st.set_page_config(page_title="Parkinson's AI System", page_icon="🧠")

# if 'token' not in st.session_state:
#     st.session_state.token = None
# if 'role' not in st.session_state:
#     st.session_state.role = None


# def login_user(username, password):
#     try:
#         data = {"username": username, "password": password}
#         response = requests.post(f"{BACKEND_URL}/token", data=data)
#         if response.status_code == 200:
#             token_data = response.json()
#             st.session_state.token = token_data["access_token"]
#             st.session_state.role = token_data["role"]  # <--- Save Role
#             st.success(f"Login successful as {token_data['role'].upper()}")
#             st.rerun()
#         else:
#             st.error("Invalid credentials")
#     except Exception as e:
#         st.error(f"Error: {e}")


# def register_user(username, password):
#     try:
#         # We send the role to the backend
#         data = {"username": username, "password": password}
#         response = requests.post(f"{BACKEND_URL}/register", data=data)
#         if response.status_code == 200:
#             st.success("Account created! Please login.")
#         else:
#             st.error(response.json()['detail'])
#     except Exception as e:
#         st.error(f"Error: {e}")


# # --- DOCTOR DASHBOARD ---
# def doctor_dashboard():
#     st.sidebar.title("Doctor Menu")
#     if st.sidebar.button("Logout"):
#         st.session_state.token = None
#         st.rerun()

#     tab1, tab2 = st.tabs(["New Diagnosis", "Patient History"])

#     headers = {"Authorization": f"Bearer {st.session_state.token}"}

#     with tab1:
#         st.header("New Diagnosis")
#         p_name = st.text_input("Patient Name")
#         p_age = st.number_input("Age", 0, 120)
#         uploaded_file = st.file_uploader("Upload Spiral/Wave Image", type=["jpg", "png"])

#         if st.button("Analyze"):
#             if uploaded_file:
#                 files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
#                 data = {"patient_name": p_name, "patient_age": p_age}
#                 res = requests.post(f"{BACKEND_URL}/predict", files=files, data=data, headers=headers)
#                 if res.status_code == 200:
#                     r = res.json()
#                     st.success(f"Result: {r['prediction']}")
#                     st.info(f"Confidence: {r['confidence']}%")

#     with tab2:
#         st.header("History")
#         res = requests.get(f"{BACKEND_URL}/history", headers=headers)
#         if res.status_code == 200:
#             st.dataframe(pd.DataFrame(res.json()))


# # --- ADMIN DASHBOARD (Matches your Diagrams) ---
# def admin_dashboard():
#     st.sidebar.title("Admin Menu")
#     if st.sidebar.button("Logout"):
#         st.session_state.token = None
#         st.rerun()

#     st.title("System Statistics")

#     headers = {"Authorization": f"Bearer {st.session_state.token}"}
#     res = requests.get(f"{BACKEND_URL}/admin/stats", headers=headers)

#     if res.status_code == 200:
#         data = res.json()

#         col1, col2 = st.columns(2)
#         col1.metric("Total Users", data['total_users'])
#         col2.metric("Total Predictions", data['total_predictions'])

#         st.divider()
#         st.subheader("Disease Distribution")
#         chart_data = pd.DataFrame({
#             "Category": ["Healthy", "Parkinson"],
#             "Count": [data['healthy_cases'], data['parkinson_cases']]
#         })
#         st.bar_chart(chart_data.set_index("Category"))
#     else:
#         st.error("Failed to fetch stats.")


# # --- MAIN APP ---
# if not st.session_state.token:
#     st.title("Parkinson's AI System")
#     tab1, tab2 = st.tabs(["Login", "Register"])

#     with tab1:
#         u = st.text_input("Username")
#         p = st.text_input("Password", type="password")
#         if st.button("Login"):
#             login_user(u, p)

#     with tab2:
#         u_reg = st.text_input("New Username")
#         p_reg = st.text_input("New Password", type="password")
#         # Allow selecting role for demo purposes
#         #role = st.selectbox("Role", ["doctor", "admin"])
#         if st.button("Register"):
#             register_user(u_reg, p_reg)
# else:
#     # ROUTING BASED ON ROLE
#     if st.session_state.role == "admin":
#         admin_dashboard()
#     else:
#         doctor_dashboard()

import streamlit as st
import requests
import pandas as pd
import re
import os
from datetime import datetime

# Get backend URL from environment or use default
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(
    page_title="Parkinson's AI System",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom styling
st.markdown("""
<style>
    .main { padding: 2rem; }
    .stButton > button { width: 100%; padding: 0.5rem; border-radius: 0.5rem; }
    h1 { color: #1f77b4; text-align: center; margin-bottom: 2rem; }
</style>
""", unsafe_allow_html=True)

# Session state initialization
if 'token' not in st.session_state:
    st.session_state.token = None
if 'role' not in st.session_state:
    st.session_state.role = None
if 'guest_mode' not in st.session_state:
    st.session_state.guest_mode = False
if 'username' not in st.session_state:
    st.session_state.username = None


# Validation function
def is_valid_username(username):
    """Validate username format: 4-20 alphanumeric characters and underscores"""
    return re.match(r"^[a-zA-Z0-9_]{4,20}$", username) is not None


# Login function
def login_user(username, password):
    """Authenticate user with backend"""
    if not is_valid_username(username):
        st.error("❌ Invalid username format (4-20 characters, alphanumeric & underscores only).")
        return

    try:
        data = {"username": username, "password": password}
        response = requests.post(f"{BACKEND_URL}/token", data=data, timeout=10)

        if response.status_code == 200:
            token_data = response.json()
            st.session_state.token = token_data["access_token"]
            st.session_state.role = token_data["role"]
            st.session_state.username = username
            st.session_state.guest_mode = False
            st.success(f"✅ Welcome, {username}! Login successful.")
            st.rerun()
        elif response.status_code == 401:
            st.error("❌ Incorrect password. Please try again.")
        else:
            st.error("❌ User not found. Please register first.")

    except requests.exceptions.Timeout:
        st.error("⏱️ Connection timed out. Please try again.")
    except requests.exceptions.ConnectionError:
        st.error("🔌 Cannot connect to server. Please check your connection.")
    except Exception as e:
        st.error(f"⚠️ Error: {str(e)}")


# Registration function
def register_user(username, password, confirm_password):
    """Register a new user"""
    # Validation
    if len(password) > 72:
        st.error("❌ Password too long. Maximum 72 characters.")
        return
    
    if password != confirm_password:
        st.error("❌ Passwords do not match.")
        return

    if not is_valid_username(username):
        st.error("❌ Invalid username format (4-20 characters, alphanumeric & underscores only).")
        return
    
    if len(password) < 6:
        st.error("❌ Password must be at least 6 characters.")
        return

    try:
        data = {"username": username, "password": password}
        response = requests.post(f"{BACKEND_URL}/register", data=data, timeout=10)

        if response.status_code == 200:
            st.success("✅ Account created successfully! Please log in.")
            st.balloons()
        else:
            error_detail = response.json().get("detail", "Registration failed")
            st.error(f"❌ {error_detail}")

    except requests.exceptions.ConnectionError:
        st.error("🔌 Cannot connect to server.")
    except Exception as e:
        st.error(f"⚠️ Error: {str(e)}")


# Guest prediction function
def guest_prediction():
    """Allow guest users to make predictions without login"""
    st.header("🔬 Quick Prediction (Guest Mode)")
    st.info("📝 Make a prediction without creating an account. Results are not saved.")
    
    col1, col2 = st.columns(2)
    with col1:
        p_name = st.text_input("Patient Name (optional)", value="Guest Patient")
        p_age = st.number_input("Age", 0, 150, value=0)
    
    with col2:
        uploaded_file = st.file_uploader(
            "Upload Spiral/Wave Image",
            type=["jpg", "png", "jpeg"],
            help="Upload a clear image of the spiral test"
        )
    
    if st.button("🚀 Analyze Image", use_container_width=True):
        if uploaded_file is None:
            st.error("❌ Please upload an image.")
            return
        
        if uploaded_file.size > 10 * 1024 * 1024:
            st.error("❌ File too large (max 10MB).")
            return
        
        files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
        data = {"patient_name": p_name, "patient_age": p_age}
        
        with st.spinner("🔄 Processing image..."):
            try:
                res = requests.post(
                    f"{BACKEND_URL}/predict",
                    files=files,
                    data=data,
                    timeout=60
                )
                
                if res.status_code == 200:
                    result = res.json()
                    
                    # Primary prediction result
                    col1, col2 = st.columns(2)
                    with col1:
                        if result['prediction'] == 'Healthy':
                            st.success(f"✅ Prediction: **{result['prediction']}**")
                        else:
                            st.error(f"⚠️ Prediction: **{result['prediction']}**")
                    with col2:
                        st.info(f"📊 Confidence: **{result['confidence']}%**")
                    
                    # Dual confidence breakdown for medical decision-making
                    st.markdown("**Detailed Analysis:**")
                    col1, col2 = st.columns(2)
                    with col1:
                        healthy_conf = result.get('healthy_confidence', 0)
                        st.metric("Healthy Confidence", f"{healthy_conf}%")
                        st.progress(min(healthy_conf / 100, 1.0))
                    with col2:
                        parkinson_conf = result.get('parkinson_confidence', 0)
                        st.metric("Parkinson Confidence", f"{parkinson_conf}%")
                        st.progress(min(parkinson_conf / 100, 1.0))
                else:
                    st.error(f"❌ Prediction failed: {res.status_code}")
            
            except requests.exceptions.Timeout:
                st.error("⏱️ Request timed out. Please try again.")
            except requests.exceptions.ConnectionError:
                st.error("🔌 Server is offline. Please try later.")
            except Exception as e:
                st.error(f"⚠️ Error: {str(e)}")


# Doctor Dashboard
def doctor_dashboard():
    """Dashboard for authenticated doctors"""
    st.sidebar.title(f"👨‍⚕️ Doctor Panel")
    st.sidebar.write(f"Logged in as: **{st.session_state.username}**")
    
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.token = None
        st.session_state.role = None
        st.session_state.guest_mode = False
        st.session_state.username = None
        st.success("✅ Logged out successfully.")
        st.rerun()

    tab1, tab2, tab3 = st.tabs(["🔬 New Diagnosis", "📋 Prediction History", "📊 Stats"])
    
    headers = {"Authorization": f"Bearer {st.session_state.token}"}

    # TAB 1: Make prediction
    with tab1:
        st.header("Make a New Diagnosis")
        
        col1, col2 = st.columns(2)
        with col1:
            p_name = st.text_input("Patient Name")
            p_age = st.number_input("Patient Age", 0, 150, value=0)
        
        with col2:
            uploaded_file = st.file_uploader(
                "Upload Spiral/Wave Test Image",
                type=["jpg", "png", "jpeg"],
                help="Upload a clear image of the spiral test"
            )

        if st.button("🚀 Analyze Image", use_container_width=True, key="doc_analyze"):
            if not p_name:
                st.error("❌ Please enter patient name.")
                return
            
            if uploaded_file is None:
                st.error("❌ Please upload an image.")
                return

            if uploaded_file.size > 10 * 1024 * 1024:
                st.error("❌ File too large (max 10MB).")
                return

            files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            data = {"patient_name": p_name, "patient_age": p_age}

            with st.spinner("🔄 Processing..."):
                try:
                    res = requests.post(
                        f"{BACKEND_URL}/predict",
                        files=files,
                        data=data,
                        headers=headers,
                        timeout=60
                    )

                    if res.status_code == 200:
                        result = res.json()
                        
                        # Primary prediction result
                        col1, col2 = st.columns(2)
                        with col1:
                            if result['prediction'] == 'Healthy':
                                st.success(f"✅ Result: **{result['prediction']}**")
                            else:
                                st.error(f"⚠️ Result: **{result['prediction']}**")
                        with col2:
                            st.info(f"📊 Confidence: **{result['confidence']}%**")
                        
                        # Dual confidence breakdown for medical decision-making
                        st.markdown("**Detailed Analysis:**")
                        col1, col2 = st.columns(2)
                        with col1:
                            healthy_conf = result.get('healthy_confidence', 0)
                            st.metric("Healthy Confidence", f"{healthy_conf}%")
                            st.progress(min(healthy_conf / 100, 1.0))
                        with col2:
                            parkinson_conf = result.get('parkinson_confidence', 0)
                            st.metric("Parkinson Confidence", f"{parkinson_conf}%")
                            st.progress(min(parkinson_conf / 100, 1.0))
                    else:
                        st.error(f"❌ Error: {res.status_code}")

                except requests.exceptions.Timeout:
                    st.error("⏱️ Request timed out.")
                except requests.exceptions.ConnectionError:
                    st.error("🔌 Server offline.")
                except Exception as e:
                    st.error(f"⚠️ Error: {str(e)}")

    # TAB 2: Prediction history
    with tab2:
        st.header("Prediction History")
        try:
            res = requests.get(f"{BACKEND_URL}/history", headers=headers, timeout=10)
            if res.status_code == 200:
                predictions = res.json()
                if predictions:
                    df = pd.DataFrame(predictions)
                    df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d %H:%M')
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("📭 No predictions yet.")
            else:
                st.error("❌ Failed to fetch history.")
        except Exception as e:
            st.error(f"⚠️ Error: {str(e)}")
    
    # TAB 3: Quick stats
    with tab3:
        st.header("Your Stats")
        try:
            res = requests.get(f"{BACKEND_URL}/history", headers=headers, timeout=10)
            if res.status_code == 200:
                predictions = res.json()
                if predictions:
                    total = len(predictions)
                    healthy = sum(1 for p in predictions if p['label'] == 'Healthy')
                    parkinson = sum(1 for p in predictions if p['label'] == 'Parkinson')
                    
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Total Predictions", total)
                    col2.metric("Healthy Cases", healthy)
                    col3.metric("Parkinson Cases", parkinson)
                    
                    # Chart
                    chart_data = pd.DataFrame({
                        "Category": ["Healthy", "Parkinson"],
                        "Count": [healthy, parkinson]
                    })
                    st.bar_chart(chart_data.set_index("Category"))
                else:
                    st.info("📭 No data yet.")
        except Exception as e:
            st.error(f"⚠️ Error: {str(e)}")


# Admin Dashboard
def admin_dashboard():
    """Dashboard for admin users"""
    st.sidebar.title(f"👨‍💼 Admin Panel")
    st.sidebar.write(f"Logged in as: **{st.session_state.username}**")
    
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.token = None
        st.session_state.role = None
        st.session_state.guest_mode = False
        st.session_state.username = None
        st.success("✅ Logged out successfully.")
        st.rerun()

    st.header("📊 System Statistics")
    headers = {"Authorization": f"Bearer {st.session_state.token}"}

    try:
        res = requests.get(f"{BACKEND_URL}/admin/stats", headers=headers, timeout=10)

        if res.status_code == 200:
            data = res.json()

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("👥 Total Users", data['total_users'])
            col2.metric("📋 Total Predictions", data['total_predictions'])
            col3.metric("✅ Healthy Cases", data['healthy_cases'])
            col4.metric("🔴 Parkinson Cases", data['parkinson_cases'])

            st.divider()
            st.subheader("Disease Distribution")
            chart_data = pd.DataFrame({
                "Category": ["Healthy", "Parkinson"],
                "Count": [data['healthy_cases'], data['parkinson_cases']]
            })
            st.bar_chart(chart_data.set_index("Category"))
        else:
            st.error("❌ Failed to fetch statistics.")

    except requests.exceptions.ConnectionError:
        st.error("🔌 Cannot connect to server.")
    except Exception as e:
        st.error(f"⚠️ Error: {str(e)}")


# Guest mode navigation
if st.session_state.guest_mode:
    st.title("🧠 Parkinson's AI System")
    col1, col2 = st.columns([5, 1])
    with col2:
        if st.button("🔐 Login/Register", use_container_width=True):
            st.session_state.guest_mode = False
            st.rerun()
    guest_prediction()

# Authentication routing
elif not st.session_state.token:
    st.title("🧠 Parkinson's AI System")
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["🔐 Login", "📝 Register", "👤 Guest Mode"])

    with tab1:
        st.subheader("User Login")
        u = st.text_input("Username", key="login_user")
        p = st.text_input("Password", type="password", key="login_pass")
        
        if st.button("🔓 Login", use_container_width=True, key="login_btn"):
            login_user(u, p)

    with tab2:
        st.subheader("Create New Account")
        u_reg = st.text_input("Choose a Username", key="reg_user")
        p_reg = st.text_input("Password", type="password", key="reg_pass")
        p_reg_confirm = st.text_input("Confirm Password", type="password", key="reg_pass_confirm")
        
        if st.button("✍️ Register", use_container_width=True, key="reg_btn"):
            register_user(u_reg, p_reg, p_reg_confirm)
    
    with tab3:
        st.subheader("Continue as Guest")
        st.info(
            "🏃 **Guest Mode:**\\n"
            "✓ No account needed\\n"
            "✓ Quick predictions\\n"
            "✓ Instant results\\n\\n"
            "⚠️ Results are not saved - create an account to maintain history."
        )
        
        if st.button("👤 Continue as Guest", use_container_width=True, key="guest_btn"):
            st.session_state.guest_mode = True
            st.rerun()

else:
    # Authenticated dashboard
    if st.session_state.role == "admin":
        admin_dashboard()
    else:
        doctor_dashboard()
