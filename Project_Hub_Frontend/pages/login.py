import streamlit as st

from api_client import login as api_login
from session import (
    initialize_session,
    login_user,
    is_logged_in
)


# ============================================================
# INITIALIZE SESSION
# ============================================================

initialize_session()


# ============================================================
# LOGIN PAGE
# ============================================================

def show_login():

    # ========================================================
    # PAGE CSS
    # ========================================================

    st.markdown(
        """
        <style>

        /* ====================================================
           PAGE
           ==================================================== */

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


        /* ====================================================
           MAIN CONTAINER
           ==================================================== */

        .block-container {
            max-width: 520px;
            padding-top: 55px;
            padding-bottom: 40px;
            margin: auto;
        }


        /* ====================================================
           LOGO
           ==================================================== */

        .project-logo {
            text-align: center;
            font-size: 22px;
            font-weight: 800;
            letter-spacing: 3px;
            color: #172a22;
            margin-bottom: 38px;
        }


        .project-logo span {
            color: #3c9b72;
        }


        /* ====================================================
           TITLE
           ==================================================== */

        .login-title {
            text-align: center;
            font-size: 31px;
            font-weight: 750;
            color: #172a22;
            margin-bottom: 8px;
        }


        /* ====================================================
           SUBTITLE
           ==================================================== */

        .login-subtitle {
            text-align: center;
            color: #87958f;
            font-size: 14px;
            margin-bottom: 32px;
        }


        /* ====================================================
           INPUTS
           ==================================================== */

        div[data-baseweb="input"] {
            border-radius: 10px;
            background: #f0f3f7;
            border: 1px solid transparent;
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


        /* ====================================================
           INPUT LABEL
           ==================================================== */

        label {
            color: #172a22 !important;
            font-weight: 550 !important;
        }




        /* ====================================================
           LOGIN BUTTON
           ==================================================== */

        .login-button button {
            background: #263944 !important;
            color: #ffffff !important;
            border: none !important;
        }


        .login-button button:hover {
            background: #1d2d35 !important;
            color: #ffffff !important;
        }


        /* ====================================================
           FORGOT BUTTON
           ==================================================== */

        .forgot-button button {
            background: transparent !important;
            color: #3c9b72 !important;
            border: none !important;
            box-shadow: none !important;
            height: 30px !important;
            padding: 0 !important;
            font-size: 13px !important;
            font-weight: 500 !important;
        }


        .forgot-button button:hover {
            color: #287453 !important;
            background: transparent !important;
        }


        /* ====================================================
           DIVIDER
           ==================================================== */

        .divider {
            display: flex;
            align-items: center;
            gap: 12px;
            margin: 27px 0 20px 0;
            color: #9aa9a2;
            font-size: 13px;
        }


        .divider-line {
            flex: 1;
            height: 1px;
            background: #e1e6e3;
        }


        /* ====================================================
           REGISTER TEXT
           ==================================================== */

        .register-text {
            text-align: center;
            color: #8a9993;
            font-size: 14px;
            margin-bottom: 12px;
        }


        /* ====================================================
           REGISTER BUTTON
           ==================================================== */

        .register-button button {
            background: #ffffff !important;
            color: #263944 !important;
            border: 1px solid #d7e0dc !important;
        }


        .register-button button:hover {
            background: #f4faf7 !important;
            border-color: #3c9b72 !important;
            color: #263944 !important;
        }


        /* ====================================================
           FOOTER
           ==================================================== */

        .login-footer {
            text-align: center;
            color: #a3afa9;
            font-size: 11px;
            margin-top: 24px;
        }


        /* ====================================================
           ERROR / SUCCESS
           ==================================================== */

        [data-testid="stAlert"] {
            border-radius: 10px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # PROJECT HUB LOGO
    # ========================================================

    st.markdown(
        """
        <div class="project-logo">
            PROJECT <span>HUB</span>
        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # TITLE
    # ========================================================

    st.markdown(
        '<div class="login-title">Welcome Back</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # SUBTITLE
    # ========================================================

    st.markdown(
        """
        <div class="login-subtitle">
            Sign in to continue to Project Hub
        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # USERNAME
    # ========================================================

    username = st.text_input(
        "Username",
        placeholder="Enter your username",
        key="project_hub_login_username"
    )


    # ========================================================
    # PASSWORD
    # ========================================================

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter your password",
        key="project_hub_login_password"
    )


    # ========================================================
    # FORGOT PASSWORD
    # ========================================================

    st.markdown(
        '<div class="forgot-wrapper">',
        unsafe_allow_html=True
    )


    forgot_clicked = st.button(
        "Forgot password?",
        key="project_hub_forgot_password"
    )


    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


    if forgot_clicked:

        st.switch_page(
            "pages/forgotpassword.py"
        )


    # ========================================================
    # SIGN IN BUTTON
    # ========================================================

    st.markdown(
        '<div class="login-button">',
        unsafe_allow_html=True
    )


    login_clicked = st.button(
        "Sign In",
        key="project_hub_sign_in",
        use_container_width=True
    )


    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # LOGIN PROCESS
    # ========================================================

    if login_clicked:

        # ----------------------------------------------------
        # Validate username
        # ----------------------------------------------------

        if not username.strip():

            st.error(
                "Please enter your username."
            )


        # ----------------------------------------------------
        # Validate password
        # ----------------------------------------------------

        elif not password:

            st.error(
                "Please enter your password."
            )


        else:

            try:

                # ==================================================
                # CALL API CLIENT
                # ==================================================

                response = api_login(
                    username=username.strip(),
                    password=password
                )


                # ==================================================
                # LOGIN SUCCESS
                # ==================================================

                if response.status_code == 200:

                    data = response.json()


                    # ------------------------------------------------
                    # GET JWT
                    # ------------------------------------------------

                    access_token = data.get(
                        "access_token"
                    )


                    if not access_token:

                        st.error(
                            "Login succeeded, but the backend "
                            "did not return an access token."
                        )


                    else:

                        # ============================================
                        # STORE SESSION
                        # ============================================

                        login_user(
                            access_token=access_token,
                            username=username.strip()
                        )


                        # ============================================
                        # REFRESH APPLICATION
                        # ============================================

                        st.rerun()


                # ==================================================
                # LOGIN FAILED
                # ==================================================

                else:

                    try:

                        error_data = response.json()

                        detail = error_data.get(
                            "detail",
                            "Login failed."
                        )

                    except Exception:

                        detail = (
                            f"Login failed. "
                            f"HTTP {response.status_code}"
                        )


                    # ------------------------------------------------
                    # Show backend error
                    # ------------------------------------------------

                    if response.status_code == 404:

                        st.error(
                            "User not found."
                        )


                    elif response.status_code == 401:

                        st.error(
                            "Invalid password."
                        )


                    elif response.status_code == 403:

                        st.error(
                            "This user account is inactive."
                        )


                    else:

                        st.error(
                            detail
                        )


            # ==================================================
            # CONNECTION ERROR
            # ==================================================

            except Exception as e:

                st.error(
                    f"Unable to connect to backend: {e}"
                )


    # ========================================================
    # DIVIDER
    # ========================================================

    st.markdown(
        """
        <div class="divider">
            <div class="divider-line"></div>
            <span>or</span>
            <div class="divider-line"></div>
        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # REGISTER
    # ========================================================

    st.markdown(
        """
        <div class="register-text">
            New to Project Hub?
        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        '<div class="register-button">',
        unsafe_allow_html=True
    )


    register_clicked = st.button(
        "Create Employee Account",
        key="project_hub_create_employee",
        use_container_width=True
    )


    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


    if register_clicked:

        st.switch_page(
            "pages/register.py"
        )


    # ========================================================
    # FOOTER
    # ========================================================

    st.markdown(
        """
        <div class="login-footer">
            🔒 Secure JWT Authentication • Project Hub
        </div>
        """,
        unsafe_allow_html=True
    )