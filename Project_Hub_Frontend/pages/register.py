import requests
import streamlit as st

from api_client import register_employee


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Create Employee Account",
    page_icon="👤",
    layout="centered"
)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at 10% 20%,
                rgba(190, 240, 210, 0.35),
                transparent 35%
            ),
            radial-gradient(
                circle at 90% 80%,
                rgba(190, 230, 240, 0.30),
                transparent 35%
            ),
            #f5fbf7;
    }

    .block-container {
        max-width: 520px;
        padding-top: 55px;
        padding-bottom: 40px;
        margin: auto;
    }

    .register-card {
        background: #ffffff;
        border: 1px solid #e1e8e4;
        border-radius: 22px;
        padding: 40px 42px 34px 42px;
        box-shadow:
            0 20px 50px rgba(31, 60, 48, 0.10);
    }

    .project-logo {
        text-align: center;
        font-size: 22px;
        font-weight: 800;
        letter-spacing: 3px;
        color: #172a22;
        margin-bottom: 32px;
    }

    .project-logo span {
        color: #3c9b72;
    }

    .register-title {
        text-align: center;
        font-size: 30px;
        font-weight: 750;
        color: #172a22;
        margin-bottom: 8px;
    }

    .register-subtitle {
        text-align: center;
        color: #87958f;
        font-size: 14px;
        margin-bottom: 30px;
    }

    div[data-baseweb="input"] {
        border-radius: 10px;
        background: #f0f3f7;
        border: none;
    }

    div[data-baseweb="input"] input {
        background: #f0f3f7;
        border-radius: 10px;
        padding: 13px;
        font-size: 15px;
    }

    div[data-baseweb="input"]:focus-within {
        border: 1px solid #3c9b72;
        box-shadow: 0 0 0 1px #3c9b72;
    }

    .stButton > button {
        width: 100%;
        height: 48px;
        border-radius: 10px;
        font-weight: 600;
    }

    .register-note {
        text-align: center;
        color: #8a9993;
        font-size: 12px;
        margin-top: 20px;
        line-height: 1.5;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# CARD
# ============================================================

st.markdown(
    '<div class="register-card">',
    unsafe_allow_html=True
)


# ============================================================
# LOGO
# ============================================================

st.markdown(
    """
    <div class="project-logo">
        PROJECT <span>HUB</span>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# TITLE
# ============================================================

st.markdown(
    '<div class="register-title">Create Account</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="register-subtitle">
        Create your Project Hub employee account
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# FORM
# ============================================================

full_name = st.text_input(
    "Full Name",
    placeholder="Enter your full name",
    key="register_full_name"
)

username = st.text_input(
    "Username",
    placeholder="Choose a username",
    key="register_username"
)

email = st.text_input(
    "Email",
    placeholder="Enter your email",
    key="register_email"
)

password = st.text_input(
    "Password",
    type="password",
    placeholder="Create a password",
    key="register_password"
)

confirm_password = st.text_input(
    "Confirm Password",
    type="password",
    placeholder="Re-enter your password",
    key="register_confirm_password"
)


# ============================================================
# CREATE ACCOUNT
# ============================================================

if st.button(
    "Create Employee Account",
    type="primary",
    use_container_width=True
):

    # --------------------------------------------------------
    # Validation
    # --------------------------------------------------------

    if not full_name.strip():

        st.error(
            "Please enter your full name."
        )

    elif not username.strip():

        st.error(
            "Please enter a username."
        )

    elif not email.strip():

        st.error(
            "Please enter your email."
        )

    elif not password:

        st.error(
            "Please enter a password."
        )

    elif len(password) < 6:

        st.error(
            "Password must contain at least 6 characters."
        )

    elif password != confirm_password:

        st.error(
            "Passwords do not match."
        )

    else:

        # ----------------------------------------------------
        # Backend request
        # ----------------------------------------------------

        try:

            response = register_employee(
                username=username.strip(),
                full_name=full_name.strip(),
                email=email.strip(),
                password=password
            )

            # ------------------------------------------------
            # SUCCESS
            # ------------------------------------------------

            if response.status_code in (200, 201):

                st.success(
                    "Employee account created successfully!"
                )

                st.info(
                    "You can now login with your username "
                    "and password."
                )

                # Clear fields safely.
                # We don't modify widget state after creation.
                st.session_state["register_success"] = True

            # ------------------------------------------------
            # BACKEND ERROR
            # ------------------------------------------------

            else:

                try:

                    error_data = response.json()

                    detail = error_data.get(
                        "detail",
                        "Registration failed."
                    )

                    # Handle FastAPI validation errors
                    if isinstance(detail, list):

                        messages = []

                        for error in detail:

                            if isinstance(error, dict):

                                messages.append(
                                    str(
                                        error.get(
                                            "msg",
                                            error
                                        )
                                    )
                                )

                            else:

                                messages.append(
                                    str(error)
                                )

                        detail = "\n".join(
                            messages
                        )

                except Exception:

                    detail = (
                        f"Registration failed. "
                        f"HTTP {response.status_code}"
                    )

                st.error(
                    detail
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "Unable to connect to backend. "
                "Make sure FastAPI is running on port 3000."
            )

        except requests.exceptions.Timeout:

            st.error(
                "Backend request timed out."
            )

        except requests.exceptions.RequestException as e:

            st.error(
                f"Backend request failed: {e}"
            )

        except Exception as e:

            st.error(
                f"Unexpected registration error: {e}"
            )


# ============================================================
# BACK TO LOGIN
# ============================================================

if st.button(
    "← Back to Login",
    use_container_width=True
):

    st.switch_page(
        "app.py"
    )


# ============================================================
# NOTE
# ============================================================

st.markdown(
    """
    <div class="register-note">
        Your password is securely hashed before being stored.
        <br>
        New accounts are automatically assigned the Employee role.
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# CLOSE CARD
# ============================================================

st.markdown(
    "</div>",
    unsafe_allow_html=True
)