import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Scorecard",
    layout="wide"
)

# Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


def login_page():
    st.title("🍺 Ambev Scorecard")

    with st.form("login"):
        username = st.text_input("User")
        password = st.text_input("Password", type="password")

        submitted = st.form_submit_button("Login")

        if submitted:
            # Replace with your authentication logic
            if username == USERNAME and password == PASSWORD:
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid credentials")


def main_app():
    st.title("📊 Scorecard")

    with open("scorecard.html", "r", encoding="utf-8") as f:
        html_content = f.read()

    components.html(
        html_content,
        height=2000,
        scrolling=True
    )


if st.session_state.logged_in:
    main_app()
else:
    login_page()
