import streamlit as st

from api_client import (
    create_task,
    get_tasks,
    get_task,
    update_task,
    delete_task,
    assign_task,
    update_task_status
)


# ==========================================
# Task Management Page
# ==========================================

def show_tasks():

    st.title("Task Management")

    # ==========================================
    # Access Token
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
            "Please select and set a current project "
            "from the Projects page."
        )

        return

    try:

        current_project_id = int(
            current_project_id
        )

    except (TypeError, ValueError):

        st.error(
            "Invalid current project ID."
        )

        return

    # ==========================================
    # Current User
    # ==========================================

    current_user = st.session_state.get(
        "user",
        {}
    )

    if not isinstance(current_user, dict):

        current_user = {}

    # ==========================================
    # System Role
    # ==========================================

    current_role = (
        current_user.get("role")
        or st.session_state.get(
            "display_role",
            ""
        )
    )

    current_role = str(
        current_role
    ).lower().strip()

    # ==========================================
    # Project Role
    # ==========================================

    project_role = (
        st.session_state.get(
            "project_role"
        )
        or current_user.get("project_role")
        or current_user.get("permission")
        or current_user.get("project_permission")
        or st.session_state.get(
            "display_project_role",
            ""
        )
    )

    project_role = str(
        project_role
    ).lower().strip()

    # ==========================================
    # Normalize Project Role
    # ==========================================

    if project_role in [
        "contributor",
        "project contributor"
    ]:

        project_role = "contributor"

    elif project_role in [
        "member",
        "project member"
    ]:

        project_role = "member"

    # ==========================================
    # CURRENT PROJECT DISPLAY
    # ==========================================

    st.info(
        f"Current Project: Project {current_project_id}"
        f" | Project Role: {project_role.title()}"
    )

    # ==========================================
    # ROLE BASED TASK ACTIONS
    #
    # ADMIN
    # ------------------------------------------
    # View Tasks              ✅
    # View Task by ID         ✅
    # Create Task             ✅
    # Update Task             ✅
    # Delete Task             ✅
    # Assign Task             ✅
    # Update Task Status      ✅
    #
    # EMPLOYEE + CONTRIBUTOR
    # ------------------------------------------
    # View Tasks              ✅
    # View Task by ID         ✅
    # Create Task             ✅
    # Update Task             ✅
    # Delete Task             ❌
    # Assign Task             ❌
    # Update Task Status      ✅
    #
    # EMPLOYEE + MEMBER
    # ------------------------------------------
    # View Tasks              ✅
    # View Task by ID         ✅
    # Create Task             ❌
    # Update Task             ❌
    # Delete Task             ❌
    # Assign Task             ❌
    # Update Task Status      ❌
    # ==========================================

    if current_role == "admin":

        task_actions = [
            "View Tasks",
            "View Task by ID",
            "Create Task",
            "Update Task",
            "Delete Task",
            "Assign Task",
            "Update Task Status"
        ]

    elif (
        current_role == "employee"
        and project_role == "contributor"
    ):

        task_actions = [
            "View Tasks",
            "View Task by ID",
            "Create Task",
            "Update Task",
            "Update Task Status"
        ]

    else:

        task_actions = [
            "View Tasks",
            "View Task by ID"
        ]

    # ==========================================
    # Navigation
    # ==========================================

    action = st.selectbox(
        "Task Action",
        task_actions
    )

    # ==========================================
    # View Tasks
    # ==========================================

    if action == "View Tasks":

        st.subheader(
            f"Tasks - Project {current_project_id}"
        )

        if st.button(
            "Load Tasks",
            key="load_current_project_tasks"
        ):

            try:

                # IMPORTANT:
                # Always send the current project ID.
                #
                # Before:
                # get_tasks(access_token)
                #
                # That caused:
                # 422 Field required: project_id
                #
                # Now:
                # get_tasks(access_token, current_project_id)

                response = get_tasks(
                    access_token,
                    current_project_id
                )

                if response.status_code == 200:

                    st.success(
                        f"Project {current_project_id} "
                        "tasks loaded successfully."
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
                        "You do not have permission "
                        "to view tasks for this project."
                    )

                else:

                    try:

                        data = response.json()

                        st.error(
                            data.get(
                                "detail",
                                "Failed to load tasks."
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
    # View Task By ID
    # ==========================================

    elif action == "View Task by ID":

        st.subheader(
            f"View Task - Project {current_project_id}"
        )

        task_id = st.number_input(
            "Task ID",
            min_value=1,
            step=1,
            key="view_task_id"
        )

        if st.button(
            "Get Task",
            key="get_task_by_id"
        ):

            try:

                response = get_task(
                    access_token,
                    int(task_id)
                )

                if response.status_code == 200:

                    task_data = response.json()

                    # ------------------------------------------
                    # Project safety check
                    # ------------------------------------------

                    actual_task = task_data

                    if isinstance(task_data, dict):

                        if isinstance(
                            task_data.get("data"),
                            dict
                        ):

                            actual_task = task_data.get(
                                "data"
                            )

                    task_project_id = None

                    if isinstance(
                        actual_task,
                        dict
                    ):

                        task_project_id = (
                            actual_task.get(
                                "project_id"
                            )
                        )

                    if (
                        task_project_id is not None
                        and int(task_project_id)
                        != int(current_project_id)
                    ):

                        st.error(
                            "This task does not belong "
                            "to the current project."
                        )

                        return

                    st.success(
                        "Task retrieved successfully."
                    )

                    st.json(
                        task_data
                    )

                elif response.status_code == 401:

                    st.error(
                        "Authentication failed. "
                        "Please login again."
                    )

                elif response.status_code == 403:

                    st.error(
                        "You do not have permission "
                        "to view this task."
                    )

                else:

                    try:

                        data = response.json()

                        st.error(
                            data.get(
                                "detail",
                                "Task not found."
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
    # Create Task
    # ==========================================

    elif action == "Create Task":

        # ------------------------------------------
        # Permission Check
        # ------------------------------------------

        if not (
            current_role == "admin"
            or (
                current_role == "employee"
                and project_role == "contributor"
            )
        ):

            st.error(
                "Only Admin or Contributor can create tasks."
            )

            return

        st.subheader(
            f"Create Task - Project {current_project_id}"
        )

        # ------------------------------------------
        # CURRENT PROJECT
        # ------------------------------------------

        st.text_input(
            "Project ID",
            value=str(current_project_id),
            disabled=True,
            key="task_create_current_project"
        )

        title = st.text_input(
            "Title",
            key="task_create_title"
        )

        description = st.text_area(
            "Description",
            key="task_create_description"
        )

        priority = st.selectbox(
            "Priority",
            [
                "low",
                "medium",
                "high"
            ],
            key="task_create_priority"
        )

        due_date = st.text_input(
            "Due Date",
            placeholder="2026-08-20T18:00:00",
            key="task_create_due_date"
        )

        if st.button(
            "Create Task",
            key="create_task_button"
        ):

            if not title.strip():

                st.warning(
                    "Task title is required."
                )

                return

            task_data = {
                "project_id": int(
                    current_project_id
                ),
                "title": title.strip(),
                "description": description.strip(),
                "priority": priority,
                "due_date": due_date.strip()
            }

            try:

                response = create_task(
                    access_token,
                    task_data
                )

                if response.status_code in [
                    200,
                    201
                ]:

                    st.success(
                        "Task created successfully."
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
                        "You do not have permission "
                        "to create tasks in this project."
                    )

                else:

                    try:

                        data = response.json()

                        st.error(
                            data.get(
                                "detail",
                                "Failed to create task."
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
    # Update Task
    # ==========================================

    elif action == "Update Task":

        # ------------------------------------------
        # Permission Check
        # ------------------------------------------

        if not (
            current_role == "admin"
            or (
                current_role == "employee"
                and project_role == "contributor"
            )
        ):

            st.error(
                "Only Admin or Contributor can update tasks."
            )

            return

        st.subheader(
            f"Update Task - Project {current_project_id}"
        )

        task_id = st.number_input(
            "Task ID",
            min_value=1,
            step=1,
            key="task_update_id"
        )

        title = st.text_input(
            "Title",
            key="task_update_title"
        )

        description = st.text_area(
            "Description",
            key="task_update_description"
        )

        priority = st.selectbox(
            "Priority",
            [
                "low",
                "medium",
                "high"
            ],
            key="task_update_priority"
        )

        status = st.selectbox(
            "Status",
            [
                "todo",
                "in_progress",
                "completed"
            ],
            key="task_update_status"
        )

        due_date = st.text_input(
            "Due Date",
            placeholder="2026-08-20T18:00:00",
            key="task_update_due_date"
        )

        if st.button(
            "Update Task",
            key="update_task_button"
        ):

            task_data = {
                "title": title.strip(),
                "description": description.strip(),
                "priority": priority,
                "status": status,
                "due_date": due_date.strip()
            }

            try:

                response = update_task(
                    access_token,
                    int(task_id),
                    task_data
                )

                if response.status_code == 200:

                    st.success(
                        "Task updated successfully."
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
                        "You do not have permission "
                        "to update this task."
                    )

                else:

                    try:

                        data = response.json()

                        st.error(
                            data.get(
                                "detail",
                                "Failed to update task."
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
    # Delete Task
    # ==========================================

    elif action == "Delete Task":

        # ------------------------------------------
        # Admin Only
        # ------------------------------------------

        if current_role != "admin":

            st.error(
                "Only Admin can delete tasks."
            )

            return

        st.subheader(
            f"Delete Task - Project {current_project_id}"
        )

        task_id = st.number_input(
            "Task ID",
            min_value=1,
            step=1,
            key="task_delete_id"
        )

        if st.button(
            "Delete Task",
            key="delete_task_button"
        ):

            try:

                response = delete_task(
                    access_token,
                    int(task_id)
                )

                if response.status_code in [
                    200,
                    204
                ]:

                    st.success(
                        "Task deleted successfully."
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
                        "Only Admin can delete tasks."
                    )

                else:

                    try:

                        data = response.json()

                        st.error(
                            data.get(
                                "detail",
                                "Failed to delete task."
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
    # Assign Task
    # ==========================================

    elif action == "Assign Task":

        # ------------------------------------------
        # Admin Only
        # ------------------------------------------

        if current_role != "admin":

            st.error(
                "Only Admin can assign tasks."
            )

            return

        st.subheader(
            f"Assign Task - Project {current_project_id}"
        )

        task_id = st.number_input(
            "Task ID",
            min_value=1,
            step=1,
            key="task_assign_id"
        )

        assigned_to = st.number_input(
            "Employee User ID",
            min_value=1,
            step=1,
            key="task_assigned_to"
        )

        if st.button(
            "Assign Task",
            key="assign_task_button"
        ):

            try:

                response = assign_task(
                    access_token,
                    int(task_id),
                    int(assigned_to)
                )

                if response.status_code == 200:

                    st.success(
                        "Task assigned successfully."
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
                        "Only Admin can assign tasks."
                    )

                else:

                    try:

                        data = response.json()

                        st.error(
                            data.get(
                                "detail",
                                "Failed to assign task."
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
    # Update Task Status
    # ==========================================

    elif action == "Update Task Status":

        # ------------------------------------------
        # Admin OR Contributor
        # ------------------------------------------

        if not (
            current_role == "admin"
            or (
                current_role == "employee"
                and project_role == "contributor"
            )
        ):

            st.error(
                "Only Admin or Contributor can update task status."
            )

            return

        st.subheader(
            f"Update Task Status - Project {current_project_id}"
        )

        task_id = st.number_input(
            "Task ID",
            min_value=1,
            step=1,
            key="task_status_id"
        )

        status = st.selectbox(
            "New Status",
            [
                "todo",
                "in_progress",
                "completed"
            ],
            key="task_status_value"
        )

        if st.button(
            "Update Status",
            key="update_task_status_button"
        ):

            try:

                response = update_task_status(
                    access_token,
                    int(task_id),
                    status
                )

                if response.status_code == 200:

                    st.success(
                        "Task status updated successfully."
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
                        "You do not have permission "
                        "to update task status."
                    )

                else:

                    try:

                        data = response.json()

                        st.error(
                            data.get(
                                "detail",
                                "Failed to update task status."
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