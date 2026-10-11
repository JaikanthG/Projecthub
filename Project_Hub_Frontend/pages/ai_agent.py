import streamlit as st

from api_client import chat_with_ai


# ============================================================
# AI AGENT PAGE
# ============================================================

def show_ai_agent():

    access_token = st.session_state.get(
        "access_token"
    )

    if not access_token:
        st.error(
            "Authentication token not found."
        )
        return

    # ========================================================
    # CURRENT PROJECT
    # ========================================================

    current_project_id = st.session_state.get(
        "current_project_id"
    )

    if current_project_id is None:
        st.warning(
            "Please select a project before using the AI Agent."
        )
        return

    # ========================================================
    # PAGE HEADER
    # ========================================================

    st.markdown(
        """
        <div class="page-title">
            🤖 AI Agent
        </div>

        <div class="page-subtitle">
            Ask Project Hub AI about your projects,
            knowledge, bugs, tasks, and engineering information.
        </div>
        """,
        unsafe_allow_html=True
    )

    # ========================================================
    # INITIALIZE CHAT HISTORY
    # ========================================================

    if "ai_chat_history" not in st.session_state:
        st.session_state.ai_chat_history = []

    # ========================================================
    # CLEAR CHAT
    # ========================================================

    col1, col2 = st.columns(
        [6, 1]
    )

    with col2:

        if st.button(
            "🗑️ Clear",
            use_container_width=True
        ):

            st.session_state.ai_chat_history = []

            st.rerun()

    # ========================================================
    # CHAT HISTORY
    # ========================================================

    for chat in st.session_state.ai_chat_history:

        role = chat.get(
            "role"
        )

        content = chat.get(
            "content",
            ""
        )

        if role == "user":

            with st.chat_message(
                "user"
            ):

                st.write(
                    content
                )

        else:

            with st.chat_message(
                "assistant"
            ):

                st.write(
                    content
                )

    # ========================================================
    # CHAT INPUT
    # ========================================================

    message = st.chat_input(
        "Ask Project Hub AI..."
    )

    if not message:
        return

    # ========================================================
    # USER MESSAGE
    # ========================================================

    st.session_state.ai_chat_history.append(
        {
            "role": "user",
            "content": message
        }
    )

    with st.chat_message(
        "user"
    ):

        st.write(
            message
        )

    # ========================================================
    # AI RESPONSE
    # ========================================================

    with st.chat_message(
        "assistant"
    ):

        with st.spinner(
            "AI Agent is thinking..."
        ):

            try:

                response = chat_with_ai(
                    access_token,
                    message,
                    current_project_id
                )

                # ------------------------------------------------
                # AUTHENTICATION ERROR
                # ------------------------------------------------

                if response.status_code == 401:

                    st.error(
                        "Your session has expired. "
                        "Please login again."
                    )

                    return

                # ------------------------------------------------
                # FORBIDDEN
                # ------------------------------------------------

                if response.status_code == 403:

                    st.error(
                        "You are not authorized to use "
                        "the AI Agent for this project."
                    )

                    return

                # ------------------------------------------------
                # SUCCESS
                # ------------------------------------------------

                if response.status_code == 200:

                    try:

                        data = response.json()

                    except Exception:

                        data = {}

                    ai_response = (
                        data.get("response")
                        or data.get("message")
                        or data.get("answer")
                        or "AI Agent returned an empty response."
                    )

                    st.write(
                        ai_response
                    )

                    st.session_state.ai_chat_history.append(
                        {
                            "role": "assistant",
                            "content": ai_response
                        }
                    )

                # ------------------------------------------------
                # OTHER API ERROR
                # ------------------------------------------------

                else:

                    try:

                        error_data = response.json()

                        detail = error_data.get(
                            "detail",
                            "AI Agent request failed."
                        )

                    except Exception:

                        detail = (
                            f"AI Agent request failed "
                            f"with status {response.status_code}."
                        )

                    st.error(
                        detail
                    )

            except Exception as e:

                st.error(
                    f"Unable to connect to AI Agent: {e}"
                )