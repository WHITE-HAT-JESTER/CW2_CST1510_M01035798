import streamlit as st
# from streamlit_authenticator import authenticator as sta
# from streamlit_authenticator.utilities import LoginError
from services.user_service import login_user, register_user
st.set_page_config(page_title="Login / Register", page_icon="🔑", layout="centered")

# ---------- Initialise session state ----------
if "users" not in st.session_state:
    # Very simple in-memory "database": {username: password}
    st.session_state.users = {}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

st.title("🔐 Hello, Welcome.")

# If already logged in, go straight to dashboard (optional)
if st.session_state.logged_in:
    st.success(f"Access Granted **{st.session_state.username}**.")
    if st.button("Dashboards"):
        # Use the official navigation API to switch pages
        st.switch_page("pages/2_Dashboard.py")  # path is relative to Home.py :contentReference[oaicite:1]{index=1}
    st.stop()


# ---------- Tabs: Login / Register ----------
tab_login, tab_register = st.tabs(["Login", "Register"])

# ----- LOGIN TAB -----
with tab_login:
    st.subheader("Login")

    login_username = st.text_input("Username", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Log in", type="primary"):
        # Simple credential check (for teaching only – not secure!)
        users = st.session_state.login_user(login_username, login_password)
        if login_user in users and users[login_username] == login_password:

            st.session_state.logged_in = True
            st.session_state.username = login_username
            st.success(f"Welcome back, {login_username}! ")

            # Redirect to dashboard page
            st.switch_page("Pages/2_Dashboard.py")
        else:
            st.error("Invalid username or password.")
            st.info("Tip: Password must be at least 8 characters long, contain "
                    "at least one uppercase, one lowercase and one number.")



# ----- REGISTER TAB -----
with tab_register:
    st.subheader("Register")

    new_username = st.text_input("Choose a username", key="register_username")
    new_password = st.text_input("Choose a password", type="password", key="register_password")
    confirm_password = st.text_input("Confirm password", type="password", key="register_confirm")

    if st.button("Create account"):
        # Basic checks
        if not new_username or not new_password:
            st.warning("Please fill in all fields.")
        elif new_password != confirm_password:
            st.error("Passwords do not match.")
        elif len(new_password) < 8:
            st.warning("Password must be at least 8 characters long.")
        elif new_username in st.session_state.users:
            st.error("Username already exists. Choose another one.")
        else:
            # "Save" user in our simple in-memory store
            st.session_state.users[new_username] = new_password

            st.success("Account created!")
            st.switch_page("Pages/2_Dashboard.py")


