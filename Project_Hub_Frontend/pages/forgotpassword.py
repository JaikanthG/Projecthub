import requests
import streamlit as st

from api_client import (
    forgot_password,
    reset_password
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Forgot Password",
    page_icon="🔐",
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

    .forgot-title {
        text-align: center;
        font-size: 30px;
        font-weight: 750;
        color: #172a22;
        margin-bottom: 8px;
    }

    .forgot-subtitle {
        text-align: center;
        color: #87958f;
        font-size: 14px;
        margin-bottom: 30px;
        line-height: 1.5;
    }

    .dev-warning {
        color: #8b6f27;
        background: #fff9e8;
        border: 1px solid #f0dfaa;
        border-radius: 9px;
        padding: 11px;
        font-size: 12px;
        margin-top: 12px;
        margin-bottom: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# CARD
# ============================================================

st.markdown(
    "</div>",
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
    '<div class="forgot-title">Forgot Password?</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="forgot-subtitle">
        Enter your registered email address to generate
        a password reset token.
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# EMAIL
# ============================================================

email = st.text_input(
    "Email",
    placeholder="Enter your registered email",
    key="forgot_password_email"
)


# ============================================================
# GENERATE RESET TOKEN
# ============================================================

if st.button(
    "Generate Reset Token",
    type="primary",
    use_container_width=True
):

    # --------------------------------------------------------
    # Validate email
    # --------------------------------------------------------

    if not email.strip():

        st.error(
            "Please enter your email address."
        )

    else:

        try:

            # ------------------------------------------------
            # Call backend API
            # ------------------------------------------------

            response = forgot_password(
                email=email.strip()
            )

            # ------------------------------------------------
            # SUCCESS
            # ------------------------------------------------

            if response.status_code == 200:

                data = response.json()

                # Get token from backend
                reset_token = data.get(
                    "reset_token"
                )

                if reset_token:

                    # ------------------------------------------------
                    # Store token in session state
                    # ------------------------------------------------

                    st.session_state[
                        "password_reset_token"
                    ] = reset_token

                    st.success(
                        "Reset token generated."
                    )

                    # ------------------------------------------------
                    # Display ONLY the token
                    # ------------------------------------------------

                    st.markdown(
                        "### Your Reset Token"
                    )

                    st.code(
                        reset_token,
                        language=None
                    )

                    st.markdown(
                        """
                        <div class="dev-warning">
                            Development mode: this token is
                            displayed here. In production,
                            it should be sent to the user's
                            email instead.
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                else:

                    st.info(
                        data.get(
                            "message",
                            "If the email exists, "
                            "a reset token has been generated."
                        )
                    )


            # ------------------------------------------------
            # BACKEND ERROR
            # ------------------------------------------------

            else:

                try:

                    error_data = response.json()

                    detail = error_data.get(
                        "detail",
                        "Unable to generate reset token."
                    )

                except Exception:

                    detail = (
                        f"Request failed. "
                        f"HTTP {response.status_code}"
                    )

                st.error(
                    detail
                )


        # ----------------------------------------------------
        # CONNECTION ERROR
        # ----------------------------------------------------

        except requests.exceptions.ConnectionError:

            st.error(
                "Unable to connect to backend. "
                "Make sure FastAPI is running on port 8000."
            )


        # ----------------------------------------------------
        # TIMEOUT
        # ----------------------------------------------------

        except requests.exceptions.Timeout:

            st.error(
                "Backend request timed out."
            )


        # ----------------------------------------------------
        # REQUEST ERROR
        # ----------------------------------------------------

        except requests.exceptions.RequestException as e:

            st.error(
                f"Backend request failed: {e}"
            )


        # ----------------------------------------------------
        # UNKNOWN ERROR
        # ----------------------------------------------------

        except Exception as e:

            st.error(
                f"Unexpected error: {e}"
            )


# ============================================================
# RESET PASSWORD SECTION
# ============================================================

st.markdown(
    "<br>",
    unsafe_allow_html=True
)

st.markdown(
    "### Reset Password"
)


# ============================================================
# RESET TOKEN
# ============================================================

reset_token = st.text_area(
    "Reset Token",
    value=st.session_state.get(
        "password_reset_token",
        ""
    ),
    placeholder="Paste your reset token here",
    height=120,
    key="forgot_reset_token"
)


# ============================================================
# NEW PASSWORD
# ============================================================

new_password = st.text_input(
    "New Password",
    type="password",
    placeholder="Enter your new password",
    key="forgot_new_password"
)


# ============================================================
# CONFIRM NEW PASSWORD
# ============================================================

confirm_password = st.text_input(
    "Confirm New Password",
    type="password",
    placeholder="Confirm your new password",
    key="forgot_confirm_password"
)


# ============================================================
# RESET PASSWORD BUTTON
# ============================================================

if st.button(
    "Reset Password",
    use_container_width=True
):

    # --------------------------------------------------------
    # Validate token
    # --------------------------------------------------------

    if not reset_token.strip():

        st.error(
            "Please enter the reset token."
        )

    # --------------------------------------------------------
    # Validate new password
    # --------------------------------------------------------

    elif not new_password:

        st.error(
            "Please enter a new password."
        )

    elif len(new_password) < 6:

        st.error(
            "Password must contain at least 6 characters."
        )

    # --------------------------------------------------------
    # Confirm password
    # --------------------------------------------------------

    elif new_password != confirm_password:

        st.error(
            "Passwords do not match."
        )

    else:

        try:

            # ------------------------------------------------
            # Call backend API
            # ------------------------------------------------

            response = reset_password(
                token=reset_token.strip(),
                new_password=new_password
            )

            # ------------------------------------------------
            # SUCCESS
            # ------------------------------------------------

            if response.status_code == 200:

                st.success(
                    "Password reset successfully."
                )

                st.info(
                    "Your password has been changed. "
                    "You can now login."
                )

                # ------------------------------------------------
                # Clear reset token
                # ------------------------------------------------

                st.session_state[
                    "password_reset_token"
                ] = ""

                # ------------------------------------------------
                # Go to login
                # ------------------------------------------------

                if st.button(
                    "Go to Login",
                    use_container_width=True
                ):

                    st.switch_page(
                        "app.py"
                    )


            # ------------------------------------------------
            # BACKEND ERROR
            # ------------------------------------------------

            else:

                try:

                    error_data = response.json()

                    detail = error_data.get(
                        "detail",
                        "Password reset failed."
                    )

                except Exception:

                    detail = (
                        f"Password reset failed. "
                        f"HTTP {response.status_code}"
                    )

                st.error(
                    detail
                )


        # ----------------------------------------------------
        # CONNECTION ERROR
        # ----------------------------------------------------

        except requests.exceptions.ConnectionError:

            st.error(
                "Unable to connect to backend. "
                "Make sure FastAPI is running on port 8000."
            )


        # ----------------------------------------------------
        # TIMEOUT
        # ----------------------------------------------------

        except requests.exceptions.Timeout:

            st.error(
                "Backend request timed out."
            )


        # ----------------------------------------------------
        # REQUEST ERROR
        # ----------------------------------------------------

        except requests.exceptions.RequestException as e:

            st.error(
                f"Backend request failed: {e}"
            )


        # ----------------------------------------------------
        # UNKNOWN ERROR
        # ----------------------------------------------------

        except Exception as e:

            st.error(
                f"Unexpected error: {e}"
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
# CLOSE CARD
# ============================================================

st.markdown(
    "</div>",
    unsafe_allow_html=True
)