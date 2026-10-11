import base64
import json

import streamlit as st

from api_client import (
    get_projects,
    create_project,
    update_project,
    delete_project,
    get_my_project_permission
)


# ============================================================
# HELPER
# ============================================================

def get_authenticated_user_id(access_token, current_user):
    """
    Get the user_id belonging to the CURRENT login.

    Priority:
        1. Current JWT user_id
        2. current_user dictionary
        3. session_state user_id

    JWT is preferred because session_state can contain
    stale data after switching between accounts.
    """

    # --------------------------------------------------------
    # 1. READ USER ID FROM CURRENT JWT
    # --------------------------------------------------------

    if access_token:

        try:
            token_parts = access_token.split(".")

            if len(token_parts) == 3:

                payload = token_parts[1]

                payload += "=" * (-len(payload) % 4)

                decoded_payload = base64.urlsafe_b64decode(
                    payload
                ).decode("utf-8")

                jwt_payload = json.loads(
                    decoded_payload
                )

                jwt_user_id = jwt_payload.get(
                    "user_id"
                )

                if jwt_user_id is not None:

                    user_id = int(jwt_user_id)

                    # Keep session synchronized with
                    # the currently authenticated account.
                    st.session_state[
                        "user_id"
                    ] = user_id

                    return user_id

        except Exception:
            pass

    # --------------------------------------------------------
    # 2. FALLBACK TO CURRENT USER OBJECT
    # --------------------------------------------------------

    if isinstance(current_user, dict):

        user_id = (
            current_user.get("user_id")
            or current_user.get("id")
        )

        if user_id is not None:

            try:
                user_id = int(user_id)

                st.session_state[
                    "user_id"
                ] = user_id

                return user_id

            except (TypeError, ValueError):
                pass

    # --------------------------------------------------------
    # 3. LAST FALLBACK: SESSION STATE
    # --------------------------------------------------------

    user_id = st.session_state.get(
        "user_id"
    )

    if user_id is not None:

        try:
            return int(user_id)

        except (TypeError, ValueError):
            pass

    return None


# ============================================================
# PROJECT MANAGEMENT PAGE
# ============================================================

def show_projects():

    st.title("Project Management")

    # ========================================================
    # ACCESS TOKEN
    # ========================================================

    access_token = st.session_state.get(
        "access_token"
    )

    if not access_token:

        st.error(
            "Authentication token not found. "
            "Please login again."
        )

        return

    # ========================================================
    # CURRENT USER
    # ========================================================

    current_user = st.session_state.get(
        "user",
        {}
    )

    if not isinstance(current_user, dict):

        current_user = {}

    # ========================================================
    # GLOBAL ROLE
    # ========================================================

    current_role = str(
        current_user.get(
            "role",
            st.session_state.get(
                "role",
                ""
            )
        )
    ).strip().lower()

    # ========================================================
    # PROJECT ACTIONS
    # ========================================================

    if current_role == "admin":

        project_actions = [
            "View Projects",
            "Create Project",
            "Update Project",
            "Delete Project"
        ]

    else:

        project_actions = [
            "View Projects"
        ]

    # ========================================================
    # SELECT ACTION
    # ========================================================

    project_action = st.selectbox(
        "Project Action",
        project_actions
    )

    # ============================================================
    # VIEW PROJECTS
    # ============================================================

    if project_action == "View Projects":

        st.subheader("Projects")

        # --------------------------------------------------------
        # LOAD PROJECTS
        # --------------------------------------------------------

        if st.button(
            "Load Projects",
            key="load_projects_button"
        ):

            try:

                response = get_projects(
                    access_token
                )

                # ------------------------------------------------
                # SUCCESS
                # ------------------------------------------------

                if response.status_code == 200:

                    data = response.json()

                    if isinstance(data, dict):

                        projects = data.get(
                            "projects",
                            []
                        )

                    elif isinstance(data, list):

                        projects = data

                    else:

                        projects = []

                    st.session_state[
                        "projects"
                    ] = projects

                    if projects:

                        st.success(
                            f"{len(projects)} "
                            "projects loaded successfully."
                        )

                    else:

                        st.info(
                            "No projects available."
                        )

                # ------------------------------------------------
                # UNAUTHORIZED
                # ------------------------------------------------

                elif response.status_code == 401:

                    st.error(
                        "Authentication failed. "
                        "Please login again."
                    )

                # ------------------------------------------------
                # FORBIDDEN
                # ------------------------------------------------

                elif response.status_code == 403:

                    st.error(
                        "You do not have permission "
                        "to view projects."
                    )

                # ------------------------------------------------
                # OTHER ERROR
                # ------------------------------------------------

                else:

                    try:

                        error_data = response.json()

                        st.error(
                            error_data.get(
                                "detail",
                                "Failed to load projects."
                            )
                        )

                    except Exception:

                        st.error(
                            f"Backend error: "
                            f"{response.status_code}"
                        )

            except Exception as e:

                st.error(
                    f"Unable to connect to backend: {e}"
                )

        # --------------------------------------------------------
        # GET PROJECTS FROM SESSION
        # --------------------------------------------------------

        projects = st.session_state.get(
            "projects",
            []
        )

        # --------------------------------------------------------
        # PROJECT SELECTION
        # --------------------------------------------------------

        if projects:

            project_options = {}

            for project in projects:

                if not isinstance(project, dict):
                    continue

                project_id = project.get(
                    "id"
                )

                project_name = project.get(
                    "project_name",
                    f"Project {project_id}"
                )

                if project_id is not None:

                    display_name = (
                        f"{project_name} "
                        f"(ID: {project_id})"
                    )

                    project_options[
                        display_name
                    ] = project

            if project_options:

                option_names = list(
                    project_options.keys()
                )

                # ------------------------------------------------
                # PRESERVE CURRENT PROJECT
                # ------------------------------------------------

                current_project_id = (
                    st.session_state.get(
                        "current_project_id"
                    )
                )

                default_index = 0

                if current_project_id is not None:

                    for index, option_name in enumerate(
                        option_names
                    ):

                        project = project_options[
                            option_name
                        ]

                        try:

                            if int(
                                project.get("id")
                            ) == int(
                                current_project_id
                            ):

                                default_index = index
                                break

                        except (
                            TypeError,
                            ValueError
                        ):

                            continue

                # ------------------------------------------------
                # SELECT PROJECT
                # ------------------------------------------------

                selected_project_name = st.selectbox(
                    "Select Current Project",
                    option_names,
                    index=default_index,
                    key="selected_current_project"
                )

                selected_project = project_options[
                    selected_project_name
                ]

                selected_project_id = int(
                    selected_project["id"]
                )

                # ------------------------------------------------
                # PROJECT DETAILS
                # ------------------------------------------------

                st.markdown(
                    "### Selected Project"
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.write(
                        f"**Project ID:** "
                        f"{selected_project.get('id', '-')}"
                    )

                    st.write(
                        f"**Project Name:** "
                        f"{selected_project.get('project_name', '-')}"
                    )

                    st.write(
                        f"**Status:** "
                        f"{selected_project.get('status', '-')}"
                    )

                with col2:

                    st.write(
                        f"**Technology:** "
                        f"{selected_project.get('technology_stack', '-')}"
                    )

                    st.write(
                        f"**Created By:** "
                        f"{selected_project.get('created_by', '-')}"
                    )

                # ====================================================
                # SET CURRENT PROJECT
                # ====================================================

                if st.button(
                    "Set Current Project",
                    type="primary",
                    key="set_current_project_button"
                ):

                    # =================================================
                    # ADMIN PROJECT ACCESS
                    # =================================================

                    if current_role == "admin":

                        # Admin has global access.
                        # Admin does not need a ProjectMember record.

                        st.session_state[
                            "current_project_id"
                        ] = selected_project_id

                        st.session_state[
                            "current_project"
                        ] = selected_project

                        st.session_state[
                            "project_role"
                        ] = "admin"

                        st.rerun()

                    # =================================================
                    # EMPLOYEE PROJECT ACCESS
                    # =================================================

                    current_user_id = (
                        get_authenticated_user_id(
                            access_token,
                            current_user
                        )
                    )

                    if current_user_id is None:

                        st.error(
                            "Unable to determine the currently "
                            "logged-in user. Please logout and "
                            "login again."
                        )

                        return

                    # ------------------------------------------------
                    # GET PROJECT PERMISSION
                    # ------------------------------------------------

                    try:

                        permission = (
                            get_my_project_permission(
                                access_token,
                                selected_project_id,
                                current_user_id
                            )
                        )

                    except Exception as e:

                        st.error(
                            "Unable to check project permission: "
                            f"{e}"
                        )

                        return

                    # ------------------------------------------------
                    # NOT ASSIGNED
                    # ------------------------------------------------

                    if permission is None:

                        st.error(
                            "You are not assigned to this project."
                        )

                        return

                    # ------------------------------------------------
                    # NORMALIZE PERMISSION
                    # ------------------------------------------------

                    permission = str(
                        permission
                    ).strip().lower()

                    # Only valid project permissions
                    # should be stored.
                    if permission not in [
                        "member",
                        "contributor"
                    ]:

                        st.error(
                            "Invalid project permission returned "
                            f"by backend: {permission}"
                        )

                        return

                    # ------------------------------------------------
                    # SAVE CURRENT PROJECT
                    # ------------------------------------------------

                    st.session_state[
                        "current_project_id"
                    ] = selected_project_id

                    st.session_state[
                        "current_project"
                    ] = selected_project

                    # ------------------------------------------------
                    # SAVE PROJECT ROLE
                    # ------------------------------------------------

                    st.session_state[
                        "project_role"
                    ] = permission

                    # ------------------------------------------------
                    # RERUN
                    # ------------------------------------------------

                    st.rerun()

                # ====================================================
                # CURRENT PROJECT STATUS
                # ====================================================

                current_project_id = (
                    st.session_state.get(
                        "current_project_id"
                    )
                )

                current_project_role = (
                    st.session_state.get(
                        "project_role"
                    )
                )

                if current_project_id is not None:

                    st.success(
                        f"Current Project ID: "
                        f"{current_project_id}"
                    )

                    if current_project_role:

                        st.info(
                            "Project Role: "
                            f"{str(current_project_role).capitalize()}"
                        )

            else:

                st.info(
                    "No valid project records were returned."
                )

        else:

            st.info(
                "Click 'Load Projects' to load available projects."
            )

    # ============================================================
    # CREATE PROJECT
    # ============================================================

    elif project_action == "Create Project":

        if current_role != "admin":

            st.error(
                "Only Admin can create projects."
            )

            return

        st.subheader(
            "Create Project"
        )

        project_name = st.text_input(
            "Project Name",
            key="create_project_name"
        )

        description = st.text_area(
            "Description",
            key="create_project_description"
        )

        technology_stack = st.text_input(
            "Technology Stack",
            key="create_project_technology"
        )

        status = st.selectbox(
            "Status",
            [
                "active",
                "completed",
                "on_hold"
            ],
            key="create_project_status"
        )

        if st.button(
            "Create Project",
            key="create_project_button"
        ):

            if not project_name.strip():

                st.warning(
                    "Project name is required."
                )

                return

            if not description.strip():

                st.warning(
                    "Description is required."
                )

                return

            if not technology_stack.strip():

                st.warning(
                    "Technology stack is required."
                )

                return

            project_data = {

                "project_name":
                    project_name.strip(),

                "description":
                    description.strip(),

                "technology_stack":
                    technology_stack.strip(),

                "status":
                    status
            }

            try:

                response = create_project(
                    access_token,
                    project_data
                )

                if response.status_code in [
                    200,
                    201
                ]:

                    st.success(
                        "Project created successfully."
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
                        "Only Admin can create projects."
                    )

                else:

                    try:

                        error_data = response.json()

                        st.error(
                            error_data.get(
                                "detail",
                                "Failed to create project."
                            )
                        )

                    except Exception:

                        st.error(
                            f"Backend error: "
                            f"{response.status_code}"
                        )

            except Exception as e:

                st.error(
                    f"Unable to connect to backend: {e}"
                )

    # ============================================================
    # UPDATE PROJECT
    # ============================================================

    elif project_action == "Update Project":

        if current_role != "admin":

            st.error(
                "Only Admin can update projects."
            )

            return

        st.subheader(
            "Update Project"
        )

        project_id = st.number_input(
            "Project ID",
            min_value=1,
            step=1,
            key="update_project_id"
        )

        project_name = st.text_input(
            "Project Name",
            key="update_project_name"
        )

        description = st.text_area(
            "Description",
            key="update_project_description"
        )

        technology_stack = st.text_input(
            "Technology Stack",
            key="update_project_technology"
        )

        status = st.selectbox(
            "Status",
            [
                "active",
                "completed",
                "on_hold"
            ],
            key="update_project_status"
        )

        if st.button(
            "Update Project",
            key="update_project_button"
        ):

            if not project_name.strip():

                st.warning(
                    "Project name is required."
                )

                return

            if not description.strip():

                st.warning(
                    "Description is required."
                )

                return

            if not technology_stack.strip():

                st.warning(
                    "Technology stack is required."
                )

                return

            project_data = {

                "project_name":
                    project_name.strip(),

                "description":
                    description.strip(),

                "technology_stack":
                    technology_stack.strip(),

                "status":
                    status
            }

            try:

                response = update_project(
                    access_token,
                    int(project_id),
                    project_data
                )

                if response.status_code == 200:

                    st.success(
                        "Project updated successfully."
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
                        "Only Admin can update projects."
                    )

                elif response.status_code == 404:

                    st.error(
                        "Project not found."
                    )

                else:

                    try:

                        error_data = response.json()

                        st.error(
                            error_data.get(
                                "detail",
                                "Failed to update project."
                            )
                        )

                    except Exception:

                        st.error(
                            f"Backend error: "
                            f"{response.status_code}"
                        )

            except Exception as e:

                st.error(
                    f"Unable to connect to backend: {e}"
                )

    # ============================================================
    # DELETE PROJECT
    # ============================================================

    elif project_action == "Delete Project":

        if current_role != "admin":

            st.error(
                "Only Admin can delete projects."
            )

            return

        st.subheader(
            "Delete Project"
        )

        project_id = st.number_input(
            "Project ID",
            min_value=1,
            step=1,
            key="delete_project_id"
        )

        st.warning(
            "Deleting a project may permanently remove "
            "its associated data."
        )

        if st.button(
            "Delete Project",
            key="delete_project_button"
        ):

            try:

                response = delete_project(
                    access_token,
                    int(project_id)
                )

                if response.status_code in [
                    200,
                    204
                ]:

                    st.success(
                        "Project deleted successfully."
                    )

                    # --------------------------------------------
                    # CLEAR CURRENT PROJECT IF DELETED
                    # --------------------------------------------

                    if (
                        st.session_state.get(
                            "current_project_id"
                        )
                        == int(project_id)
                    ):

                        st.session_state.pop(
                            "current_project_id",
                            None
                        )

                        st.session_state.pop(
                            "current_project",
                            None
                        )

                        st.session_state[
                            "project_role"
                        ] = "Member"

                    # --------------------------------------------
                    # RESPONSE
                    # --------------------------------------------

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
                        "Only Admin can delete projects."
                    )

                elif response.status_code == 404:

                    st.error(
                        "Project not found."
                    )

                else:

                    try:

                        error_data = response.json()

                        st.error(
                            error_data.get(
                                "detail",
                                "Failed to delete project."
                            )
                        )

                    except Exception:

                        st.error(
                            f"Backend error: "
                            f"{response.status_code}"
                        )

            except Exception as e:

                st.error(
                    f"Unable to connect to backend: {e}"
                )