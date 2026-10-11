import streamlit as st

from api_client import (
    get_project_activities,
    get_activity
)


# ==========================================================
# Activity Log Page
# ==========================================================

def show_activity():

    st.title("Activity Log")

    # ==========================================================
    # ACCESS TOKEN
    # ==========================================================

    access_token = st.session_state.get(
        "access_token"
    )

    if not access_token:

        st.error(
            "Authentication token not found."
        )

        return

    # ==========================================================
    # CURRENT PROJECT
    # ==========================================================

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

    # ==========================================================
    # PROJECT ROLE
    # ==========================================================

    project_role = str(
        st.session_state.get(
            "project_role",
            "member"
        )
    ).strip().lower()

    # ==========================================================
    # DISPLAY CURRENT PROJECT
    # ==========================================================

    st.info(
        f"Current Project ID: {current_project_id}"
    )

    # ==========================================================
    # ACTIVITY ACTIONS
    #
    # Admin:
    #   View Activity Logs
    #   View Activity by ID
    #
    # Contributor:
    #   View Activity Logs
    #   View Activity by ID
    #
    # Member:
    #   View Activity Logs
    #   View Activity by ID
    # ==========================================================

    activity_actions = [
        "View Activity Logs",
        "View Activity by ID"
    ]

    # ==========================================================
    # NAVIGATION
    # ==========================================================

    action = st.selectbox(
        "Activity Action",
        activity_actions
    )

    # ==========================================================
    # VIEW PROJECT ACTIVITY LOGS
    # ==========================================================

    if action == "View Activity Logs":

        st.subheader(
            "Activity Logs"
        )

        if st.button(
            "Load Activity Logs",
            key="load_activity_logs_button"
        ):

            try:

                # --------------------------------------------------
                # IMPORTANT:
                # Use project-specific endpoint.
                #
                # DO NOT use get_activities(access_token)
                # because that is the global Admin-only endpoint.
                # --------------------------------------------------

                response = get_project_activities(
                    access_token,
                    current_project_id
                )

                if response.status_code == 200:

                    data = response.json()

                    activities = data.get(
                        "data",
                        []
                    )

                    count = data.get(
                        "count",
                        len(activities)
                    )

                    st.success(
                        f"{count} activity records found."
                    )

                    # ==================================================
                    # PREPARE TABLE
                    # ==================================================

                    if activities:

                        table_data = []

                        for activity in activities:

                            table_data.append({

                                "ID": activity.get(
                                    "id"
                                ),

                                "Project ID": activity.get(
                                    "project_id"
                                ),

                                "User ID": activity.get(
                                    "user_id"
                                ),

                                "Action": activity.get(
                                    "action"
                                ),

                                "Entity Type": activity.get(
                                    "entity_type"
                                ),

                                "Entity ID": activity.get(
                                    "entity_id"
                                ),

                                "Description": activity.get(
                                    "description"
                                ),

                                "Created At": activity.get(
                                    "created_at"
                                )
                            })

                        # ==================================================
                        # DISPLAY TABLE
                        # ==================================================

                        st.dataframe(
                            table_data,
                            use_container_width=True,
                            hide_index=True
                        )

                    else:

                        st.info(
                            "No activity records found "
                            "for the current project."
                        )

                elif response.status_code == 401:

                    st.error(
                        "Authentication failed. "
                        "Please login again."
                    )

                elif response.status_code == 403:

                    st.error(
                        "You do not have permission "
                        "to view activity logs for this project."
                    )

                elif response.status_code == 404:

                    st.error(
                        "Current project was not found."
                    )

                else:

                    try:

                        error_data = response.json()

                        st.error(
                            error_data.get(
                                "detail",
                                "Failed to load activity logs."
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

    # ==========================================================
    # VIEW ACTIVITY BY ID
    # ==========================================================

    elif action == "View Activity by ID":

        st.subheader(
            "View Activity"
        )

        activity_id = st.number_input(
            "Activity ID",
            min_value=1,
            step=1,
            key="activity_view_id"
        )

        if st.button(
            "Get Activity",
            key="get_activity_button"
        ):

            try:

                response = get_activity(
                    access_token,
                    int(activity_id)
                )

                if response.status_code == 200:

                    activity = response.json()

                    # --------------------------------------------------
                    # Extra frontend safety:
                    #
                    # The activity returned by backend should belong
                    # to the current project.
                    # --------------------------------------------------

                    if isinstance(
                        activity,
                        dict
                    ):

                        activity_project_id = activity.get(
                            "project_id"
                        )

                        if (
                            activity_project_id is not None
                            and int(activity_project_id)
                            != current_project_id
                        ):

                            st.error(
                                "This activity does not belong "
                                "to the current project."
                            )

                            return

                        st.success(
                            "Activity retrieved successfully."
                        )

                        st.json(
                            activity
                        )

                    else:

                        st.success(
                            "Activity retrieved successfully."
                        )

                        st.write(
                            activity
                        )

                elif response.status_code == 401:

                    st.error(
                        "Authentication failed. "
                        "Please login again."
                    )

                elif response.status_code == 403:

                    st.error(
                        "You do not have permission "
                        "to view this activity."
                    )

                elif response.status_code == 404:

                    st.error(
                        "Activity not found."
                    )

                else:

                    try:

                        error_data = response.json()

                        st.error(
                            error_data.get(
                                "detail",
                                "Activity not found."
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