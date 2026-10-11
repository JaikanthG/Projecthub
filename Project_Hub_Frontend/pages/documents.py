import streamlit as st

from api_client import (
    upload_document,
    get_documents,
    get_document,
    delete_document
)


# ==========================================
# Document Management Page
# ==========================================

def show_documents():

    st.title("Document Management")

    # ==========================================
    # ACCESS TOKEN
    # ==========================================

    access_token = st.session_state.get(
        "access_token"
    )

    if not access_token:

        st.error(
            "Authentication token not found."
        )

        return

    # ==========================================
    # CURRENT PROJECT
    # ==========================================

    current_project_id = st.session_state.get(
        "current_project_id"
    )

    if current_project_id is None:

        st.warning(
            "Please select a current project from Projects page."
        )

        return

    current_project_id = int(
        current_project_id
    )

    # ==========================================
    # GLOBAL ROLE
    # ==========================================

    global_role = str(
        st.session_state.get(
            "role",
            ""
        )
    ).strip().lower()

    # ==========================================
    # PROJECT ROLE
    #
    # Project role is different from global role.
    #
    # Example:
    # Global Role  = employee
    # Project Role = contributor
    # ==========================================

    project_role = str(
        st.session_state.get(
            "project_role",
            "member"
        )
    ).strip().lower()

    # ==========================================
    # DISPLAY CURRENT PROJECT
    # ==========================================

    st.info(
        f"Current Project ID: {current_project_id}"
    )

    # ==========================================
    # DOCUMENT ACTIONS
    #
    # Admin:
    #   View
    #   View By ID
    #   Upload
    #   Delete
    #
    # Contributor:
    #   View
    #   View By ID
    #   Upload
    #
    # Member:
    #   View
    #   View By ID
    # ==========================================

    if global_role == "admin":

        document_actions = [
            "View Documents",
            "View Document by ID",
            "Upload Document",
            "Delete Document"
        ]

    elif project_role == "contributor":

        document_actions = [
            "View Documents",
            "View Document by ID",
            "Upload Document"
        ]

    elif project_role == "member":

        document_actions = [
            "View Documents",
            "View Document by ID"
        ]

    else:

        document_actions = [
            "View Documents",
            "View Document by ID"
        ]

    # ==========================================
    # NAVIGATION
    # ==========================================

    action = st.selectbox(
        "Document Action",
        document_actions
    )

    # ==========================================
    # VIEW DOCUMENTS
    # ==========================================

    if action == "View Documents":

        st.subheader("Documents")

        if st.button(
            "Load Documents",
            key="load_documents_button"
        ):

            try:

                # ----------------------------------
                # IMPORTANT:
                # Send current project ID
                # ----------------------------------

                response = get_documents(
                    access_token,
                    current_project_id
                )

                if response.status_code == 200:

                    st.success(
                        "Documents loaded successfully."
                    )

                    data = response.json()

                    st.json(
                        data
                    )

                elif response.status_code == 401:

                    st.error(
                        "Authentication failed. "
                        "Please login again."
                    )

                elif response.status_code == 403:

                    st.error(
                        "You do not have access to this project."
                    )

                elif response.status_code == 404:

                    st.error(
                        "Project not found."
                    )

                else:

                    try:

                        data = response.json()

                        st.error(
                            data.get(
                                "detail",
                                "Failed to load documents."
                            )
                        )

                    except Exception:

                        st.error(
                            f"Error: {response.status_code}"
                        )

            except Exception as e:

                st.error(
                    f"Unable to connect to backend: {e}"
                )

    # ==========================================
    # VIEW DOCUMENT BY ID
    # ==========================================

    elif action == "View Document by ID":

        st.subheader("View Document")

        document_id = st.number_input(
            "Document ID",
            min_value=1,
            step=1,
            key="view_document_id"
        )

        if st.button(
            "Get Document",
            key="get_document_button"
        ):

            try:

                response = get_document(
                    access_token,
                    int(document_id)
                )

                if response.status_code == 200:

                    st.success(
                        "Document retrieved successfully."
                    )

                    st.json(
                        response.json()
                    )

                elif response.status_code == 401:

                    st.error(
                        "Authentication failed. "
                        "Please login again."
                    )

                elif response.status_code == 403:

                    st.error(
                        "You do not have access to this document's project."
                    )

                elif response.status_code == 404:

                    st.error(
                        "Document not found."
                    )

                else:

                    try:

                        data = response.json()

                        st.error(
                            data.get(
                                "detail",
                                "Failed to retrieve document."
                            )
                        )

                    except Exception:

                        st.error(
                            f"Error: {response.status_code}"
                        )

            except Exception as e:

                st.error(
                    f"Unable to connect to backend: {e}"
                )

    # ==========================================
    # UPLOAD DOCUMENT
    # ==========================================

    elif action == "Upload Document":

        # --------------------------------------
        # Permission:
        #
        # Admin
        # Contributor
        #
        # Member cannot upload.
        # --------------------------------------

        if (
            global_role != "admin"
            and project_role != "contributor"
        ):

            st.error(
                "Only Admin or Contributor can upload documents."
            )

            return

        st.subheader(
            "Upload Document"
        )

        # --------------------------------------
        # CURRENT PROJECT
        #
        # No manual project ID.
        # --------------------------------------

        st.text_input(
            "Project ID",
            value=str(current_project_id),
            disabled=True
        )

        uploaded_file = st.file_uploader(
            "Choose a document",
            key="document_uploader"
        )

        if st.button(
            "Upload Document",
            key="upload_document_button"
        ):

            if uploaded_file is None:

                st.warning(
                    "Please select a document."
                )

                return

            try:

                response = upload_document(
                    access_token,
                    current_project_id,
                    uploaded_file
                )

                if response.status_code in [
                    200,
                    201
                ]:

                    st.success(
                        "Document uploaded successfully."
                    )

                    try:

                        st.json(
                            response.json()
                        )

                    except Exception:

                        pass

                elif response.status_code == 401:

                    st.error(
                        "Authentication failed. "
                        "Please login again."
                    )

                elif response.status_code == 403:

                    st.error(
                        "You do not have permission to upload documents "
                        "to this project."
                    )

                elif response.status_code == 404:

                    st.error(
                        "Project not found."
                    )

                else:

                    try:

                        data = response.json()

                        st.error(
                            data.get(
                                "detail",
                                "Failed to upload document."
                            )
                        )

                    except Exception:

                        st.error(
                            f"Error: {response.status_code}"
                        )

            except Exception as e:

                st.error(
                    f"Unable to connect to backend: {e}"
                )

    # ==========================================
    # DELETE DOCUMENT
    # ==========================================

    elif action == "Delete Document":

        # --------------------------------------
        # Only global Admin
        # --------------------------------------

        if global_role != "admin":

            st.error(
                "Only Admin can delete documents."
            )

            return

        st.subheader(
            "Delete Document"
        )

        document_id = st.number_input(
            "Document ID",
            min_value=1,
            step=1,
            key="delete_document_id"
        )

        if st.button(
            "Delete Document",
            key="delete_document_button"
        ):

            try:

                response = delete_document(
                    access_token,
                    int(document_id)
                )

                if response.status_code in [
                    200,
                    204
                ]:

                    st.success(
                        "Document deleted successfully."
                    )

                    if response.text:

                        try:

                            st.json(
                                response.json()
                            )

                        except Exception:

                            pass

                elif response.status_code == 401:

                    st.error(
                        "Authentication failed. "
                        "Please login again."
                    )

                elif response.status_code == 403:

                    st.error(
                        "Only Admin can delete documents."
                    )

                elif response.status_code == 404:

                    st.error(
                        "Document not found."
                    )

                else:

                    try:

                        data = response.json()

                        st.error(
                            data.get(
                                "detail",
                                "Failed to delete document."
                            )
                        )

                    except Exception:

                        st.error(
                            f"Error: {response.status_code}"
                        )

            except Exception as e:

                st.error(
                    f"Unable to connect to backend: {e}"
                )