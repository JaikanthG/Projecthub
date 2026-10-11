import streamlit as st
import base64
import json

from session import (
    initialize_session,
    is_logged_in,
    logout_user
)

from api_client import (
    get_my_project_permission
)

from pages.login import show_login
from pages.dashboard import show_dashboard
from pages.projects import show_projects
from pages.project_members import show_project_members
from pages.knowledge import show_knowledge
from pages.tasks import show_tasks
from pages.bugs import show_bugs
from pages.documents import show_documents
from pages.activity import show_activity
from pages.notifications import show_notifications
from pages.search import show_search
from pages.rca_reports import show_rca_reports
from pages.ai_agent import show_ai_agent


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Project Hub",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# GLOBAL CSS
# ============================================================

st.markdown(
    """
    <style>

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }

    .stApp {
        background: #f5f7fb;
    }

    .main .block-container {
        max-width: 1450px;
        padding: 35px 45px 50px 45px;
    }

    [data-testid="stSidebar"] {
        background: #111827;
        min-width: 270px;
        max-width: 270px;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding: 20px 18px;
    }

    .brand-title {
        color: #ffffff !important;
        font-size: 25px;
        font-weight: 750;
        letter-spacing: -0.5px;
    }

    .brand-subtitle {
        color: #9ca3af !important;
        font-size: 12px;
        margin-top: 4px;
        margin-bottom: 24px;
    }

    .profile-box {
        background: #1f2937;
        border: 1px solid #374151;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 24px;
    }

    .profile-name-text {
        color: #ffffff !important;
        font-size: 15px;
        font-weight: 700;
        margin-bottom: 14px;
    }

    .profile-label-text {
        color: #9ca3af !important;
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-top: 8px;
    }

    .profile-value-text {
        color: #ffffff !important;
        font-size: 13px;
        font-weight: 600;
        margin-top: 2px;
    }

    .sidebar-title {
        color: #6b7280 !important;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] {
        color: #e5e7eb !important;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] label {
        color: #e5e7eb !important;
        background: transparent !important;
        border-radius: 9px;
        padding: 9px 10px;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] label p {
        color: #e5e7eb !important;
        font-size: 13px !important;
        font-weight: 500 !important;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] label div {
        color: #e5e7eb !important;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
        background: #1f2937 !important;
    }

    [data-testid="stSidebar"]
    [data-testid="stRadio"]
    label:has(input:checked) {
        background: #2563eb !important;
    }

    [data-testid="stSidebar"]
    [data-testid="stRadio"]
    label:has(input:checked) p {
        color: #ffffff !important;
        font-weight: 650 !important;
    }

    [data-testid="stSidebar"] .stButton button {
        width: 100%;
        height: 42px;
        border-radius: 9px;
        background: #1f2937;
        color: #e5e7eb !important;
        border: 1px solid #374151;
        font-weight: 600;
    }

    [data-testid="stSidebar"] .stButton button:hover {
        background: #374151;
        color: #ffffff !important;
    }

    .page-title {
        font-size: 34px;
        font-weight: 750;
        color: #111827 !important;
        letter-spacing: -1px;
        margin-bottom: 4px;
    }

    .page-subtitle {
        color: #6b7280 !important;
        font-size: 14px;
        margin-bottom: 30px;
    }

    .kpi-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 20px;
        min-height: 125px;
        box-shadow: 0 3px 12px rgba(15, 23, 42, 0.05);
    }

    .kpi-icon {
        font-size: 22px;
        margin-bottom: 10px;
    }

    .kpi-label {
        color: #6b7280 !important;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.4px;
    }

    .kpi-value {
        color: #111827 !important;
        font-size: 30px;
        font-weight: 750;
        margin-top: 5px;
    }

    .kpi-description {
        color: #9ca3af !important;
        font-size: 11px;
        margin-top: 4px;
    }

    .section-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 22px;
        box-shadow: 0 3px 12px rgba(15, 23, 42, 0.04);
    }

    .section-title {
        color: #111827 !important;
        font-size: 17px;
        font-weight: 700;
    }

    .section-subtitle {
        color: #6b7280 !important;
        font-size: 12px;
        margin-top: 3px;
    }

    [data-testid="stMetric"] {
        background: #f8fafc;
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        padding: 14px;
    }

    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
    }

    .stTextInput input,
    .stTextArea textarea,
    .stNumberInput input {
        border-radius: 8px;
    }

    [data-testid="stDataFrame"] {
        border-radius: 10px;
        overflow: hidden;
    }

    [data-testid="stAlert"] {
        border-radius: 9px;
    }

    .app-footer {
        margin-top: 45px;
        padding-top: 18px;
        border-top: 1px solid #e5e7eb;
        text-align: center;
        color: #9ca3af !important;
        font-size: 11px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SESSION INITIALIZATION
# ============================================================

initialize_session()


# ============================================================
# LOGIN CHECK
# ============================================================

if not is_logged_in():

    show_login()

    st.stop()


# ============================================================
# CURRENT USER
# ============================================================

current_user = st.session_state.get(
    "user",
    {}
)

if not isinstance(current_user, dict):
    current_user = {}


# ============================================================
# ACCESS TOKEN
# ============================================================

access_token = st.session_state.get(
    "access_token",
    ""
)


# ============================================================
# USERNAME
# ============================================================

username = (
    current_user.get("username")
    or st.session_state.get("username")
    or "User"
)


# ============================================================
# USER ID
# ============================================================

user_id = (
    current_user.get("user_id")
    or current_user.get("id")
    or st.session_state.get("user_id")
)


# ============================================================
# FALLBACK: EXTRACT USER ID FROM JWT
# ============================================================

if user_id is None and access_token:

    try:

        token_parts = access_token.split(".")

        if len(token_parts) == 3:

            payload = token_parts[1]

            payload += "=" * (
                -len(payload) % 4
            )

            decoded_payload = base64.urlsafe_b64decode(
                payload
            ).decode("utf-8")

            jwt_payload = json.loads(
                decoded_payload
            )

            user_id = (
                jwt_payload.get("user_id")
                or jwt_payload.get("id")
            )

            if user_id is not None:

                user_id = int(user_id)

                st.session_state["user_id"] = user_id

    except Exception:

        user_id = None


# ============================================================
# SAVE USER ID
# ============================================================

if user_id is not None:

    try:

        st.session_state["user_id"] = int(
            user_id
        )

    except Exception:

        pass


# ============================================================
# GLOBAL SYSTEM ROLE
# ============================================================

system_role = (
    current_user.get("role")
    or st.session_state.get("role")
    or "Employee"
)


# ============================================================
# CURRENT PROJECT
# ============================================================

# IMPORTANT:
# The selected project is stored by pages/projects.py.
# Never reset this value here.

current_project_id = st.session_state.get(
    "current_project_id",
    None
)

# Normalize project ID.
if current_project_id is not None:

    try:

        current_project_id = int(
            current_project_id
        )

        st.session_state[
            "current_project_id"
        ] = current_project_id

    except (TypeError, ValueError):

        current_project_id = None

        st.session_state[
            "current_project_id"
        ] = None


# ============================================================
# PROJECT ROLE
# ============================================================

# Global role:
#     User.role
#
# Project role:
#     ProjectMember.permission
#
# Admin:
#     Global access to every project.
#     Does NOT require ProjectMember.
#
# Employee:
#     Project role comes from ProjectMember.permission.
# ============================================================


# ============================================================
# NORMALIZE GLOBAL SYSTEM ROLE
# ============================================================

raw_system_role = str(
    system_role
).strip().lower()


# ============================================================
# RESOLVE PROJECT ROLE
# ============================================================

project_role = None


# ------------------------------------------------------------
# ADMIN
# ------------------------------------------------------------

if raw_system_role == "admin":

    # Admin has global access.
    #
    # IMPORTANT:
    # Never call get_my_project_permission()
    # for Admin.

    project_role = "admin"


# ------------------------------------------------------------
# EMPLOYEE
# ------------------------------------------------------------

elif (
    current_project_id is not None
    and user_id is not None
    and access_token
):

    try:

        fetched_permission = (
            get_my_project_permission(
                access_token,
                int(current_project_id),
                int(user_id)
            )
        )

        if fetched_permission is not None:

            fetched_permission = str(
                fetched_permission
            ).strip().lower()

            if fetched_permission in (
                "member",
                "contributor"
            ):

                project_role = (
                    fetched_permission
                )

    except Exception:

        project_role = None


# ============================================================
# DEFAULT PROJECT ROLE
# ============================================================

if project_role is None:

    if raw_system_role == "admin":

        project_role = "admin"

    else:

        project_role = "member"


# ============================================================
# SAVE PROJECT ROLE
# ============================================================

st.session_state[
    "project_role"
] = project_role


# ============================================================
# NORMALIZE ROLES
# ============================================================

raw_system_role = str(
    system_role
).strip().lower()

raw_project_role = str(
    project_role
).strip().lower()


# ============================================================
# DISPLAY ROLES
# ============================================================

display_system_role = (
    raw_system_role
    .replace("_", " ")
    .title()
)

display_project_role = (
    raw_project_role
    .replace("_", " ")
    .title()
)


# ============================================================
# SAVE DISPLAY VALUES
# ============================================================

st.session_state[
    "display_username"
] = username

st.session_state[
    "display_role"
] = display_system_role

st.session_state[
    "display_project_role"
] = display_project_role


# ============================================================
# DASHBOARD ACCESS
# ============================================================

dashboard_allowed = (

    raw_system_role == "admin"

    or (

        raw_system_role == "employee"

        and raw_project_role == "contributor"

    )
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    # --------------------------------------------------------
    # BRAND
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="brand-title">
            📊 Project Hub
        </div>

        <div class="brand-subtitle">
            Project Management System
        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # USER PROFILE
    # --------------------------------------------------------

    st.markdown(
        '<div class="profile-box">',
        unsafe_allow_html=True
    )


    st.markdown(
        f'<div class="profile-name-text">'
        f'👤 {username}'
        f'</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # GLOBAL ROLE
    # --------------------------------------------------------

    st.markdown(
        '<div class="profile-label-text">'
        'ROLE'
        '</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        f'<div class="profile-value-text">'
        f'{display_system_role}'
        f'</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # PROJECT ROLE
    # --------------------------------------------------------

    st.markdown(
        '<div class="profile-label-text">'
        'PROJECT ROLE'
        '</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        f'<div class="profile-value-text">'
        f'{display_project_role}'
        f'</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # CURRENT PROJECT
    # --------------------------------------------------------

    if current_project_id is not None:

        st.markdown(
            '<div class="profile-label-text">'
            'CURRENT PROJECT'
            '</div>',
            unsafe_allow_html=True
        )


        st.markdown(
            f'<div class="profile-value-text">'
            f'Project {current_project_id}'
            f'</div>',
            unsafe_allow_html=True
        )


    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # WORKSPACE
    # --------------------------------------------------------

    st.markdown(
        '<div class="sidebar-title">'
        'Workspace'
        '</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # NAVIGATION OPTIONS
    # --------------------------------------------------------

    navigation_options = []


    if dashboard_allowed:

        navigation_options.append(
            "📊 Dashboard"
        )


    navigation_options.extend(
        [
            "📁 Projects",
            "👥 Project Members",
            "📚 Knowledge",
            "✅ Tasks",
            "🐞 Bugs",
            "📄 Documents",
            "📋 Activity Log",
            "🔔 Notifications",
            "🔎 Search",
            "🧾 RCA Reports",
            "🤖 AI Agent"
        ]
    )


    # --------------------------------------------------------
    # NAVIGATION
    # --------------------------------------------------------

    page = st.radio(
        "Navigation",
        navigation_options,
        label_visibility="collapsed"
    )


    # --------------------------------------------------------
    # ACCOUNT
    # --------------------------------------------------------

    st.markdown(
        "<br>",
        unsafe_allow_html=True
    )


    st.markdown(
        '<div class="sidebar-title">'
        'Account'
        '</div>',
        unsafe_allow_html=True
    )


    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        logout_user()

        st.rerun()


# ============================================================
# PAGE ROUTING
# ============================================================

if page == "📊 Dashboard":

    if dashboard_allowed:

        show_dashboard()

    else:

        show_projects()


elif page == "📁 Projects":

    show_projects()


elif page == "👥 Project Members":

    show_project_members()


elif page == "📚 Knowledge":

    show_knowledge()


elif page == "✅ Tasks":

    show_tasks()


elif page == "🐞 Bugs":

    show_bugs()


elif page == "📄 Documents":

    show_documents()


elif page == "📋 Activity Log":

    show_activity()


elif page == "🔔 Notifications":

    show_notifications()


elif page == "🔎 Search":

    show_search()


elif page == "🧾 RCA Reports":

    show_rca_reports()


elif page == "🤖 AI Agent":

    show_ai_agent()