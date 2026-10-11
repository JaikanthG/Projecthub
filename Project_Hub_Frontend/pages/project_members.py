import streamlit as st

from api_client import (
    assign_project_member,
    get_project_members,
    update_project_member,
    remove_project_member
)


# ==========================================
# Project Member Management Page
# ==========================================

def show_project_members():

    st.title("Project Member Management")

    access_token = st.session_state.get(
        "access_token"
    )

    if not access_token:

        st.error(
            "Authentication token not found."
        )

        return

    # ==========================================
    # Get Current User Role
    # ==========================================

    current_role = str(
        st.session_state.get(
            "role",
            ""
        )
    ).lower()

    # ==========================================
    # Admin
    #   View
    #   Assign
    #   Update Permission
    #   Remove
    #
    # Employee
    #   View only
    # ==========================================

    if current_role == "admin":

        member_actions = [
            "View Project Members",
            "Assign Member",
            "Update Permission",
            "Remove Member"
        ]

    else:

        member_actions = [
            "View Project Members"
        ]

    # ==========================================
    # Navigation
    # ==========================================

    action = st.selectbox(
        "Member Action",
        member_actions
    )

    # ==========================================
    # View Members
    # ==========================================

    if action == "View Project Members":

        st.subheader("Project Members")

        project_id = st.number_input(
            "Project ID",
            min_value=1,
            step=1
        )

        if st.button("Load Members"):

            try:

                response = get_project_members(
                    access_token,
                    int(project_id)
                )

                if response.status_code == 200:

                    st.success(
                        "Project members loaded successfully."
                    )

                    st.json(
                        response.json()
                    )

                elif response.status_code == 403:

                    st.error(
                        "You do not have permission "
                        "to view project members."
                    )

                else:

                    try:

                        data = response.json()

                        st.error(
                            data.get(
                                "detail",
                                "Failed to load project members."
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
    # Assign Member
    # ==========================================

    elif action == "Assign Member":

        if current_role != "admin":

            st.error(
                "Only Admin can assign project members."
            )

            return

        st.subheader("Assign Project Member")

        project_id = st.number_input(
            "Project ID",
            min_value=1,
            step=1,
            key="assign_project_id"
        )

        user_id = st.number_input(
            "User ID",
            min_value=1,
            step=1,
            key="assign_user_id"
        )

        permission = st.selectbox(
            "Permission",
            [
                "member",
                "contributor"
            ]
        )

        if st.button("Assign Member"):

            try:

                response = assign_project_member(
                    access_token,
                    int(project_id),
                    int(user_id),
                    permission
                )

                if response.status_code in [200, 201]:

                    st.success(
                        "Employee assigned successfully."
                    )

                    st.json(
                        response.json()
                    )

                elif response.status_code == 403:

                    st.error(
                        "Only Admin can assign project members."
                    )

                else:

                    try:

                        data = response.json()

                        st.error(
                            data.get(
                                "detail",
                                "Failed to assign member."
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
    # Update Permission
    # ==========================================

    elif action == "Update Permission":

        if current_role != "admin":

            st.error(
                "Only Admin can update member permissions."
            )

            return

        st.subheader("Update Member Permission")

        member_id = st.number_input(
            "Member ID",
            min_value=1,
            step=1,
            key="update_member_id"
        )

        permission = st.selectbox(
            "New Permission",
            [
                "member",
                "contributor"
            ]
        )

        if st.button("Update Permission"):

            try:

                response = update_project_member(
                    access_token,
                    int(member_id),
                    permission
                )

                if response.status_code == 200:

                    st.success(
                        "Permission updated successfully."
                    )

                    st.json(
                        response.json()
                    )

                elif response.status_code == 403:

                    st.error(
                        "Only Admin can update member permissions."
                    )

                else:

                    try:

                        data = response.json()

                        st.error(
                            data.get(
                                "detail",
                                "Failed to update permission."
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
    # Remove Member
    # ==========================================

    elif action == "Remove Member":

        if current_role != "admin":

            st.error(
                "Only Admin can remove project members."
            )

            return

        st.subheader("Remove Project Member")

        member_id = st.number_input(
            "Member ID",
            min_value=1,
            step=1,
            key="remove_member_id"
        )

        if st.button("Remove Member"):

            try:

                response = remove_project_member(
                    access_token,
                    int(member_id)
                )

                if response.status_code in [200, 204]:

                    st.success(
                        "Project member removed successfully."
                    )

                    if response.text:

                        st.json(
                            response.json()
                        )

                elif response.status_code == 403:

                    st.error(
                        "Only Admin can remove project members."
                    )

                else:

                    try:

                        data = response.json()

                        st.error(
                            data.get(
                                "detail",
                                "Failed to remove member."
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