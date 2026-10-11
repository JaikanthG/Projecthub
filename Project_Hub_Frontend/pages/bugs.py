import streamlit as st

from api_client import (
    create_bug,
    get_bugs,
    get_bug,
    update_bug,
    delete_bug,
    assign_bug,
    update_bug_status
)


def show_bugs():

    st.title("Bug Management")

    # ==========================================
    # Authentication
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
    # Current Project
    # ==========================================

    current_project_id = st.session_state.get(
        "current_project_id"
    )

    if current_project_id is None:

        st.warning(
            "Please select a current project first."
        )

        return

    current_project_id = int(
        current_project_id
    )

    st.info(
        f"Current Project ID: {current_project_id}"
    )

    # ==========================================
    # Bug Action
    # ==========================================

    action = st.selectbox(
        "Bug Action",
        [
            "View Bugs",
            "View Bug by ID",
            "Create Bug",
            "Update Bug",
            "Delete Bug",
            "Assign Bug",
            "Update Bug Status"
        ]
    )

    # ==========================================
    # View Bugs
    # ==========================================

    if action == "View Bugs":

        st.subheader(
            "Bug Repository"
        )

        if st.button(
            "Load Bugs"
        ):

            response = get_bugs(
                access_token,
                current_project_id
            )

            if response.status_code == 200:

                st.success(
                    "Bugs loaded successfully."
                )

                st.json(
                    response.json()
                )

            else:

                try:

                    data = response.json()

                    st.error(
                        data.get(
                            "detail",
                            "Failed to load bugs."
                        )
                    )

                except Exception:

                    st.error(
                        f"Error: {response.status_code}"
                    )

    # ==========================================
    # View Bug By ID
    # ==========================================

    elif action == "View Bug by ID":

        st.subheader(
            "View Bug"
        )

        bug_id = st.number_input(
            "Bug ID",
            min_value=1,
            step=1,
            key="bug_view_id"
        )

        if st.button(
            "Get Bug"
        ):

            response = get_bug(
                access_token,
                int(bug_id)
            )

            if response.status_code == 200:

                st.success(
                    "Bug retrieved successfully."
                )

                st.json(
                    response.json()
                )

            else:

                try:

                    data = response.json()

                    st.error(
                        data.get(
                            "detail",
                            "Bug not found."
                        )
                    )

                except Exception:

                    st.error(
                        f"Error: {response.status_code}"
                    )

    # ==========================================
    # Create Bug
    # ==========================================

    elif action == "Create Bug":

        st.subheader(
            "Create Bug"
        )

        st.text_input(
            "Project ID",
            value=str(current_project_id),
            disabled=True
        )

        title = st.text_input(
            "Bug Title"
        )

        description = st.text_area(
            "Description"
        )

        priority = st.selectbox(
            "Priority",
            [
                "low",
                "medium",
                "high"
            ]
        )

        severity = st.selectbox(
            "Severity",
            [
                "minor",
                "major",
                "critical"
            ]
        )

        if st.button(
            "Create Bug"
        ):

            if not title.strip():

                st.error(
                    "Bug title is required."
                )

                return

            if not description.strip():

                st.error(
                    "Bug description is required."
                )

                return

            bug_data = {
                "project_id": current_project_id,
                "title": title.strip(),
                "description": description.strip(),
                "priority": priority,
                "severity": severity
            }

            response = create_bug(
                access_token,
                bug_data
            )

            if response.status_code in [200, 201]:

                st.success(
                    "Bug created successfully."
                )

                st.json(
                    response.json()
                )

            else:

                try:

                    data = response.json()

                    st.error(
                        data.get(
                            "detail",
                            "Failed to create bug."
                        )
                    )

                except Exception:

                    st.error(
                        f"Error: {response.status_code}"
                    )

    # ==========================================
    # Update Bug
    # ==========================================

    elif action == "Update Bug":

        st.subheader(
            "Update Bug"
        )

        bug_id = st.number_input(
            "Bug ID",
            min_value=1,
            step=1,
            key="bug_update_id"
        )

        title = st.text_input(
            "Bug Title",
            key="bug_update_title"
        )

        description = st.text_area(
            "Description",
            key="bug_update_description"
        )

        priority = st.selectbox(
            "Priority",
            [
                "low",
                "medium",
                "high"
            ],
            key="bug_update_priority"
        )

        severity = st.selectbox(
            "Severity",
            [
                "minor",
                "major",
                "critical"
            ],
            key="bug_update_severity"
        )

        status = st.selectbox(
            "Status",
            [
                "open",
                "in_progress",
                "resolved",
                "closed"
            ],
            key="bug_update_status"
        )

        if st.button(
            "Update Bug"
        ):

            bug_data = {
                "title": title.strip(),
                "description": description.strip(),
                "priority": priority,
                "severity": severity,
                "status": status
            }

            response = update_bug(
                access_token,
                int(bug_id),
                bug_data
            )

            if response.status_code == 200:

                st.success(
                    "Bug updated successfully."
                )

                st.json(
                    response.json()
                )

            else:

                try:

                    data = response.json()

                    st.error(
                        data.get(
                            "detail",
                            "Failed to update bug."
                        )
                    )

                except Exception:

                    st.error(
                        f"Error: {response.status_code}"
                    )

    # ==========================================
    # Delete Bug
    # ==========================================

    elif action == "Delete Bug":

        st.subheader(
            "Delete Bug"
        )

        bug_id = st.number_input(
            "Bug ID",
            min_value=1,
            step=1,
            key="bug_delete_id"
        )

        if st.button(
            "Delete Bug"
        ):

            response = delete_bug(
                access_token,
                int(bug_id)
            )

            if response.status_code in [200, 204]:

                st.success(
                    "Bug deleted successfully."
                )

                if response.text:

                    try:

                        st.json(
                            response.json()
                        )

                    except Exception:

                        pass

            else:

                try:

                    data = response.json()

                    st.error(
                        data.get(
                            "detail",
                            "Failed to delete bug."
                        )
                    )

                except Exception:

                    st.error(
                        f"Error: {response.status_code}"
                    )

    # ==========================================
    # Assign Bug
    # ==========================================

    elif action == "Assign Bug":

        st.subheader(
            "Assign Bug"
        )

        bug_id = st.number_input(
            "Bug ID",
            min_value=1,
            step=1,
            key="bug_assign_id"
        )

        assigned_to = st.number_input(
            "Employee User ID",
            min_value=1,
            step=1,
            key="bug_assigned_to"
        )

        if st.button(
            "Assign Bug"
        ):

            response = assign_bug(
                access_token,
                int(bug_id),
                int(assigned_to)
            )

            if response.status_code == 200:

                st.success(
                    "Bug assigned successfully."
                )

                st.json(
                    response.json()
                )

            else:

                try:

                    data = response.json()

                    st.error(
                        data.get(
                            "detail",
                            "Failed to assign bug."
                        )
                    )

                except Exception:

                    st.error(
                        f"Error: {response.status_code}"
                    )

    # ==========================================
    # Update Bug Status
    # ==========================================

    elif action == "Update Bug Status":

        st.subheader(
            "Update Bug Status"
        )

        bug_id = st.number_input(
            "Bug ID",
            min_value=1,
            step=1,
            key="bug_status_id"
        )

        status = st.selectbox(
            "New Status",
            [
                "open",
                "in_progress",
                "resolved",
                "closed"
            ]
        )

        if st.button(
            "Update Status"
        ):

            response = update_bug_status(
                access_token,
                int(bug_id),
                status
            )

            if response.status_code == 200:

                st.success(
                    "Bug status updated successfully."
                )

                st.json(
                    response.json()
                )

            else:

                try:

                    data = response.json()

                    st.error(
                        data.get(
                            "detail",
                            "Failed to update bug status."
                        )
                    )

                except Exception:

                    st.error(
                        f"Error: {response.status_code}"
                    )