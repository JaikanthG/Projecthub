import streamlit as st

from api_client import (
    create_knowledge,
    get_knowledge,
    get_knowledge_by_id,
    update_knowledge,
    delete_knowledge
)


# ============================================================
# KNOWLEDGE MANAGEMENT PAGE
# ============================================================

def show_knowledge():

    st.title("Knowledge Management")

    # ========================================================
    # AUTHENTICATION
    # ========================================================

    access_token = st.session_state.get("access_token")

    if not access_token:
        st.error("Authentication token not found.")
        return

    # ========================================================
    # CURRENT PROJECT
    # ========================================================

    current_project_id = st.session_state.get(
        "current_project_id"
    )

    if current_project_id is None:
        st.warning(
            "Please select and set a current project from the Projects page."
        )
        return

    try:
        current_project_id = int(current_project_id)
    except (TypeError, ValueError):
        st.error("Invalid current project ID.")
        return

    # ========================================================
    # GLOBAL ROLE
    # ========================================================

    global_role = str(
        st.session_state.get(
            "role",
            ""
        )
    ).strip().lower()

    # ========================================================
    # PROJECT ROLE
    #
    # Admin       -> Full knowledge control
    # Contributor -> View + Create + Update
    # Member      -> View only
    # ========================================================

    project_role = str(
        st.session_state.get(
            "project_role",
            "member"
        )
    ).strip().lower()

    # --------------------------------------------------------
    # Admin is always allowed.
    # Employee permission comes from project role.
    # --------------------------------------------------------

    is_admin = global_role == "admin"
    is_contributor = project_role == "contributor"
    is_member = project_role == "member"

    # ========================================================
    # CURRENT PROJECT DISPLAY
    # ========================================================

    st.info(
        f"Current Project: Project {current_project_id} "
        f" | Project Role: {project_role.title()}"
    )

    # ========================================================
    # KNOWLEDGE ACTIONS
    # ========================================================

    if is_admin:

        knowledge_actions = [
            "View Knowledge",
            "View Knowledge by ID",
            "Create Knowledge",
            "Update Knowledge",
            "Delete Knowledge"
        ]

    elif is_contributor:

        knowledge_actions = [
            "View Knowledge",
            "View Knowledge by ID",
            "Create Knowledge",
            "Update Knowledge"
        ]

    else:

        knowledge_actions = [
            "View Knowledge",
            "View Knowledge by ID"
        ]

    # ========================================================
    # NAVIGATION
    # ========================================================

    action = st.selectbox(
        "Knowledge Action",
        knowledge_actions
    )

    # ========================================================
    # VIEW CURRENT PROJECT KNOWLEDGE
    # ========================================================

    if action == "View Knowledge":

        st.subheader(
            f"Knowledge Repository - Project {current_project_id}"
        )

        if st.button(
            "Load Knowledge",
            key="load_current_project_knowledge"
        ):

            try:

                # IMPORTANT:
                # Always send current_project_id.
                # This prevents loading knowledge from
                # other projects.

                response = get_knowledge(
                    access_token,
                    current_project_id
                )

                if response.status_code == 200:

                    data = response.json()

                    st.success(
                        "Current project knowledge loaded successfully."
                    )

                    st.json(data)

                elif response.status_code == 401:

                    st.error(
                        "Authentication failed. Please login again."
                    )

                elif response.status_code == 403:

                    st.error(
                        "You do not have permission to view "
                        "this project's knowledge."
                    )

                else:

                    try:

                        error_data = response.json()

                        st.error(
                            error_data.get(
                                "detail",
                                "Failed to load project knowledge."
                            )
                        )

                    except Exception:

                        st.error(
                            f"Backend error: {response.status_code}"
                        )

            except Exception as e:

                st.error(
                    f"Unable to connect to backend: {e}"
                )

    # ========================================================
    # VIEW KNOWLEDGE BY ID
    # ========================================================

    elif action == "View Knowledge by ID":

        st.subheader(
            f"View Knowledge - Project {current_project_id}"
        )

        knowledge_id = st.number_input(
            "Knowledge ID",
            min_value=1,
            step=1,
            key="knowledge_view_id"
        )

        if st.button(
            "Get Knowledge",
            key="get_current_project_knowledge"
        ):

            try:

                # ------------------------------------------------
                # IMPORTANT:
                # Do NOT directly call get_knowledge_by_id().
                #
                # First load only the current project's knowledge
                # and verify that the requested ID belongs to it.
                # ------------------------------------------------

                project_response = get_knowledge(
                    access_token,
                    current_project_id
                )

                if project_response.status_code != 200:

                    try:

                        error_data = project_response.json()

                        st.error(
                            error_data.get(
                                "detail",
                                "Unable to load current project knowledge."
                            )
                        )

                    except Exception:

                        st.error(
                            f"Backend error: "
                            f"{project_response.status_code}"
                        )

                    return

                project_data = project_response.json()

                # ------------------------------------------------
                # Handle response formats:
                #
                # 1. List
                # 2. {"data": [...]}
                # ------------------------------------------------

                if isinstance(project_data, list):

                    knowledge_items = project_data

                elif isinstance(project_data, dict):

                    knowledge_items = project_data.get(
                        "data",
                        []
                    )

                    if not isinstance(
                        knowledge_items,
                        list
                    ):
                        knowledge_items = []

                else:

                    knowledge_items = []

                # ------------------------------------------------
                # Find knowledge only inside current project
                # ------------------------------------------------

                selected_knowledge = None

                for item in knowledge_items:

                    try:

                        item_id = int(
                            item.get("id")
                        )

                    except (TypeError, ValueError):

                        continue

                    if item_id == int(knowledge_id):

                        selected_knowledge = item
                        break

                # ------------------------------------------------
                # Knowledge does not belong to current project
                # ------------------------------------------------

                if selected_knowledge is None:

                    st.error(
                        f"Knowledge ID {int(knowledge_id)} "
                        f"does not belong to Project "
                        f"{current_project_id}."
                    )

                    return

                # ------------------------------------------------
                # Display current project knowledge
                # ------------------------------------------------

                st.success(
                    "Knowledge retrieved successfully."
                )

                st.json(
                    selected_knowledge
                )

            except Exception as e:

                st.error(
                    f"Unable to connect to backend: {e}"
                )

    # ========================================================
    # CREATE KNOWLEDGE
    # ========================================================

    elif action == "Create Knowledge":

        if not (
            is_admin
            or is_contributor
        ):

            st.error(
                "Only Admin or Contributor can create knowledge."
            )

            return

        st.subheader(
            f"Create Knowledge - Project {current_project_id}"
        )

        # ----------------------------------------------------
        # Project ID is automatically taken from current project.
        # User cannot accidentally create knowledge in another
        # project from this page.
        # ----------------------------------------------------

        st.text_input(
            "Project",
            value=f"Project {current_project_id}",
            disabled=True
        )

        title = st.text_input(
            "Title",
            key="knowledge_create_title"
        )

        content = st.text_area(
            "Content",
            key="knowledge_create_content"
        )

        tags = st.text_input(
            "Tags",
            key="knowledge_create_tags"
        )

        version = st.text_input(
            "Version",
            value="1.0",
            key="knowledge_create_version"
        )

        status = st.selectbox(
            "Status",
            [
                "draft",
                "published"
            ],
            key="knowledge_create_status"
        )

        if st.button(
            "Create Knowledge",
            key="create_current_project_knowledge"
        ):

            if not title.strip():

                st.error(
                    "Title is required."
                )

                return

            if not content.strip():

                st.error(
                    "Content is required."
                )

                return

            knowledge_data = {

                "project_id": int(
                    current_project_id
                ),

                "title": title,

                "content": content,

                "tags": tags,

                "version": version,

                "status": status
            }

            try:

                response = create_knowledge(
                    access_token,
                    knowledge_data
                )

                if response.status_code in [
                    200,
                    201
                ]:

                    st.success(
                        "Knowledge created successfully "
                        f"for Project {current_project_id}."
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
                        "You do not have permission to create "
                        "knowledge in this project."
                    )

                else:

                    try:

                        error_data = response.json()

                        st.error(
                            error_data.get(
                                "detail",
                                "Failed to create knowledge."
                            )
                        )

                    except Exception:

                        st.error(
                            f"Backend error: {response.status_code}"
                        )

            except Exception as e:

                st.error(
                    f"Unable to connect to backend: {e}"
                )

    # ========================================================
    # UPDATE KNOWLEDGE
    # ========================================================

    elif action == "Update Knowledge":

        if not (
            is_admin
            or is_contributor
        ):

            st.error(
                "Only Admin or Contributor can update knowledge."
            )

            return

        st.subheader(
            f"Update Knowledge - Project {current_project_id}"
        )

        knowledge_id = st.number_input(
            "Knowledge ID",
            min_value=1,
            step=1,
            key="knowledge_update_id"
        )

        title = st.text_input(
            "Title",
            key="knowledge_update_title"
        )

        content = st.text_area(
            "Content",
            key="knowledge_update_content"
        )

        tags = st.text_input(
            "Tags",
            key="knowledge_update_tags"
        )

        version = st.text_input(
            "Version",
            key="knowledge_update_version"
        )

        status = st.selectbox(
            "Status",
            [
                "draft",
                "published"
            ],
            key="knowledge_update_status"
        )

        if st.button(
            "Update Knowledge",
            key="update_current_project_knowledge"
        ):

            try:

                # ------------------------------------------------
                # First verify that the knowledge belongs to the
                # currently selected project.
                # ------------------------------------------------

                project_response = get_knowledge(
                    access_token,
                    current_project_id
                )

                if project_response.status_code != 200:

                    try:

                        error_data = project_response.json()

                        st.error(
                            error_data.get(
                                "detail",
                                "Unable to verify project knowledge."
                            )
                        )

                    except Exception:

                        st.error(
                            f"Backend error: "
                            f"{project_response.status_code}"
                        )

                    return

                project_data = project_response.json()

                if isinstance(
                    project_data,
                    list
                ):

                    knowledge_items = project_data

                elif isinstance(
                    project_data,
                    dict
                ):

                    knowledge_items = project_data.get(
                        "data",
                        []
                    )

                    if not isinstance(
                        knowledge_items,
                        list
                    ):
                        knowledge_items = []

                else:

                    knowledge_items = []

                knowledge_exists = False

                for item in knowledge_items:

                    try:

                        item_id = int(
                            item.get("id")
                        )

                    except (TypeError, ValueError):

                        continue

                    if item_id == int(knowledge_id):

                        knowledge_exists = True
                        break

                if not knowledge_exists:

                    st.error(
                        f"Knowledge ID {int(knowledge_id)} "
                        f"does not belong to Project "
                        f"{current_project_id}."
                    )

                    return

                # ------------------------------------------------
                # Update
                # ------------------------------------------------

                knowledge_data = {

                    "title": title,

                    "content": content,

                    "tags": tags,

                    "version": version,

                    "status": status
                }

                response = update_knowledge(
                    access_token,
                    int(knowledge_id),
                    knowledge_data
                )

                if response.status_code == 200:

                    st.success(
                        "Knowledge updated successfully."
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
                        "You do not have permission to update "
                        "knowledge in this project."
                    )

                elif response.status_code == 404:

                    st.error(
                        "Knowledge not found."
                    )

                else:

                    try:

                        error_data = response.json()

                        st.error(
                            error_data.get(
                                "detail",
                                "Failed to update knowledge."
                            )
                        )

                    except Exception:

                        st.error(
                            f"Backend error: {response.status_code}"
                        )

            except Exception as e:

                st.error(
                    f"Unable to connect to backend: {e}"
                )

    # ========================================================
    # DELETE KNOWLEDGE
    # ========================================================

    elif action == "Delete Knowledge":

        if not is_admin:

            st.error(
                "Only Admin can delete knowledge."
            )

            return

        st.subheader(
            f"Delete Knowledge - Project {current_project_id}"
        )

        knowledge_id = st.number_input(
            "Knowledge ID",
            min_value=1,
            step=1,
            key="knowledge_delete_id"
        )

        if st.button(
            "Delete Knowledge",
            key="delete_current_project_knowledge"
        ):

            try:

                # ------------------------------------------------
                # Verify knowledge belongs to current project
                # before allowing deletion.
                # ------------------------------------------------

                project_response = get_knowledge(
                    access_token,
                    current_project_id
                )

                if project_response.status_code != 200:

                    try:

                        error_data = project_response.json()

                        st.error(
                            error_data.get(
                                "detail",
                                "Unable to verify project knowledge."
                            )
                        )

                    except Exception:

                        st.error(
                            f"Backend error: "
                            f"{project_response.status_code}"
                        )

                    return

                project_data = project_response.json()

                if isinstance(
                    project_data,
                    list
                ):

                    knowledge_items = project_data

                elif isinstance(
                    project_data,
                    dict
                ):

                    knowledge_items = project_data.get(
                        "data",
                        []
                    )

                    if not isinstance(
                        knowledge_items,
                        list
                    ):
                        knowledge_items = []

                else:

                    knowledge_items = []

                knowledge_exists = False

                for item in knowledge_items:

                    try:

                        item_id = int(
                            item.get("id")
                        )

                    except (TypeError, ValueError):

                        continue

                    if item_id == int(knowledge_id):

                        knowledge_exists = True
                        break

                if not knowledge_exists:

                    st.error(
                        f"Knowledge ID {int(knowledge_id)} "
                        f"does not belong to Project "
                        f"{current_project_id}."
                    )

                    return

                # ------------------------------------------------
                # Delete
                # ------------------------------------------------

                response = delete_knowledge(
                    access_token,
                    int(knowledge_id)
                )

                if response.status_code in [
                    200,
                    204
                ]:

                    st.success(
                        "Knowledge deleted successfully."
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
                        "Only Admin can delete knowledge."
                    )

                elif response.status_code == 404:

                    st.error(
                        "Knowledge not found."
                    )

                else:

                    try:

                        error_data = response.json()

                        st.error(
                            error_data.get(
                                "detail",
                                "Failed to delete knowledge."
                            )
                        )

                    except Exception:

                        st.error(
                            f"Backend error: {response.status_code}"
                        )

            except Exception as e:

                st.error(
                    f"Unable to connect to backend: {e}"
                )