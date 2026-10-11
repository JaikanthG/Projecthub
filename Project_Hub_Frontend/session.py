import streamlit as st
import jwt


# ============================================================
# INITIALIZE SESSION
# ============================================================

def initialize_session():

    if "access_token" not in st.session_state:
        st.session_state.access_token = None

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "user" not in st.session_state:
        st.session_state.user = {}

    if "user_id" not in st.session_state:
        st.session_state.user_id = None

    if "username" not in st.session_state:
        st.session_state.username = None

    if "role" not in st.session_state:
        st.session_state.role = None

    if "project_role" not in st.session_state:
        st.session_state.project_role = None

    # --------------------------------------------------------
    # CURRENT PROJECT
    # --------------------------------------------------------

    if "current_project_id" not in st.session_state:
        st.session_state.current_project_id = None

    if "current_project" not in st.session_state:
        st.session_state.current_project = {}

    if "projects" not in st.session_state:
        st.session_state.projects = []


# ============================================================
# LOGIN USER
# ============================================================

def login_user(
    access_token: str,
    username: str
):

    try:

        # --------------------------------------------------------
        # Decode JWT
        # --------------------------------------------------------

        payload = jwt.decode(
            access_token,
            options={
                "verify_signature": False
            }
        )

        # --------------------------------------------------------
        # Store access token
        # --------------------------------------------------------

        st.session_state.access_token = access_token

        # --------------------------------------------------------
        # Store username
        # --------------------------------------------------------

        st.session_state.username = username

        # --------------------------------------------------------
        # Store complete JWT payload
        # --------------------------------------------------------

        st.session_state.user = payload

        # Make sure username exists
        st.session_state.user["username"] = username

        # --------------------------------------------------------
        # Get USER ID
        # --------------------------------------------------------

        user_id = (
            payload.get("user_id")
            or payload.get("id")
        )

        st.session_state.user_id = user_id

        # --------------------------------------------------------
        # Get SYSTEM ROLE
        # --------------------------------------------------------

        role = (
            payload.get("role")
            or payload.get("user_role")
            or payload.get("system_role")
        )

        if role:

            st.session_state.role = str(
                role
            ).strip().lower()

        else:

            st.session_state.role = None

        # --------------------------------------------------------
        # PROJECT ROLE
        #
        # Do not blindly trust an old project permission here.
        # Project permission should be determined after the
        # user selects the current project.
        # --------------------------------------------------------

        st.session_state.project_role = None

        # --------------------------------------------------------
        # Clear previous project selection on new login
        # --------------------------------------------------------

        st.session_state.current_project_id = None

        st.session_state.current_project = {}

        st.session_state.projects = []

        # --------------------------------------------------------
        # Login state
        # --------------------------------------------------------

        st.session_state.logged_in = True

    except Exception as e:

        # --------------------------------------------------------
        # Clear session if JWT processing fails
        # --------------------------------------------------------

        st.session_state.access_token = None

        st.session_state.username = None

        st.session_state.user = {}

        st.session_state.user_id = None

        st.session_state.role = None

        st.session_state.project_role = None

        st.session_state.current_project_id = None

        st.session_state.current_project = {}

        st.session_state.projects = []

        st.session_state.logged_in = False

        raise Exception(
            f"Unable to process login information: {e}"
        )


# ============================================================
# LOGOUT USER
# ============================================================

def logout_user():

    st.session_state.access_token = None

    st.session_state.username = None

    st.session_state.user = {}

    st.session_state.user_id = None

    st.session_state.role = None

    st.session_state.project_role = None

    st.session_state.current_project_id = None

    st.session_state.current_project = {}

    st.session_state.projects = []

    st.session_state.logged_in = False


# ============================================================
# CHECK LOGIN
# ============================================================

def is_logged_in():

    return st.session_state.get(
        "logged_in",
        False
    )