import streamlit as st

from api_client import (
    get_notifications,
    get_notification,
    mark_notification_read,
    mark_all_notifications_read,
    delete_notification
)


# ============================================================
# Notification Management Page
# ============================================================

def show_notifications():

    st.title("Notification Management")

    # ========================================================
    # Access Token
    # ========================================================

    access_token = st.session_state.get(
        "access_token"
    )

    if not access_token:

        st.error(
            "Authentication token not found."
        )

        return

    # ========================================================
    # Persistent Notification State
    # ========================================================
    #
    # Streamlit reruns the script after every button click.
    # Keep notifications in session_state so the list remains
    # available after Mark as Read / Mark All as Read.
    #
    # ========================================================

    if "notifications_data" not in st.session_state:

        st.session_state.notifications_data = None

    # ========================================================
    # Get Current User
    # ========================================================

    user_data = st.session_state.get(
        "user",
        {}
    )

    if not isinstance(
        user_data,
        dict
    ):

        user_data = {}

    # ========================================================
    # System Role
    # ========================================================

    current_role = str(
        st.session_state.get(
            "role",
            user_data.get(
                "role",
                ""
            )
        )
    ).lower().strip()

    # ========================================================
    # Project Role
    # ========================================================

    project_role = str(
        st.session_state.get(
            "project_role",
            user_data.get(
                "project_role",
                user_data.get(
                    "permission",
                    user_data.get(
                        "project_permission",
                        ""
                    )
                )
            )
        )
    ).lower().strip()

    # ========================================================
    # Determine Notification Permissions
    # ========================================================
    #
    # ADMIN
    #   View
    #   View By ID
    #   Mark Read
    #   Delete
    #
    # EMPLOYEE + CONTRIBUTOR
    #   View
    #   View By ID
    #   Mark Read
    #   Delete
    #
    # EMPLOYEE + MEMBER
    #   View
    #   View By ID
    #   Mark Read
    #   NO DELETE
    #
    # ========================================================

    is_admin = (
        current_role == "admin"
    )

    is_contributor = (
        current_role == "employee"
        and
        project_role == "contributor"
    )

    is_member = (
        current_role == "employee"
        and
        project_role == "member"
    )

    can_delete_notification = (
        is_admin
        or
        is_contributor
    )

    # ========================================================
    # Notification Actions
    # ========================================================

    if can_delete_notification:

        notification_actions = [
            "View Notifications",
            "View Notification by ID",
            "Mark as Read",
            "Delete Notification"
        ]

    else:

        notification_actions = [
            "View Notifications",
            "View Notification by ID",
            "Mark as Read"
        ]

    # ========================================================
    # Navigation
    # ========================================================

    action = st.selectbox(
        "Notification Action",
        notification_actions
    )

    # ========================================================
    # View Notifications
    # ========================================================

    if action == "View Notifications":

        st.subheader(
            "🔔 Notifications"
        )

        # ----------------------------------------------------
        # Load / Refresh Notifications
        # ----------------------------------------------------

        if st.button(
            "Load Notifications",
            key="load_notifications"
        ):

            try:

                response = get_notifications(
                    access_token
                )

                # ====================================================
                # SUCCESS
                # ====================================================

                if response.status_code == 200:

                    try:

                        payload = response.json()

                    except Exception:

                        st.error(
                            "Backend returned an invalid response."
                        )

                        return

                    # ------------------------------------------------
                    # Handle Different Response Formats
                    # ------------------------------------------------

                    if isinstance(
                        payload,
                        dict
                    ):

                        notifications = payload.get(
                            "data",
                            payload.get(
                                "notifications",
                                []
                            )
                        )

                    elif isinstance(
                        payload,
                        list
                    ):

                        notifications = payload

                    else:

                        notifications = []

                    # ------------------------------------------------
                    # Validate Notification List
                    # ------------------------------------------------

                    if not isinstance(
                        notifications,
                        list
                    ):

                        notifications = []

                    # ------------------------------------------------
                    # Save Notifications
                    # ------------------------------------------------

                    st.session_state.notifications_data = (
                        notifications
                    )

                # ====================================================
                # UNAUTHORIZED
                # ====================================================

                elif response.status_code == 401:

                    st.error(
                        "Authentication failed. "
                        "Please login again."
                    )

                    return

                # ====================================================
                # FORBIDDEN
                # ====================================================

                elif response.status_code == 403:

                    st.error(
                        "You do not have permission "
                        "to view notifications."
                    )

                    return

                # ====================================================
                # OTHER ERROR
                # ====================================================

                else:

                    try:

                        data = response.json()

                        st.error(
                            data.get(
                                "detail",
                                "Failed to load notifications."
                            )
                        )

                    except Exception:

                        st.error(
                            f"Error: {response.status_code}"
                        )

                    return

            except Exception as e:

                st.error(
                    f"Unable to connect to backend: {e}"
                )

                return

        # ====================================================
        # Read Notifications From Session State
        # ====================================================

        notifications = st.session_state.get(
            "notifications_data"
        )

        if notifications is None:

            st.info(
                "Click 'Load Notifications' "
                "to view your notifications."
            )

            return

        # ====================================================
        # Empty State
        # ====================================================

        if not notifications:

            st.info(
                "No notifications found."
            )

            return

        # ====================================================
        # Count Unread Notifications
        # ====================================================

        unread_count = sum(
            1
            for notification in notifications
            if (
                isinstance(
                    notification,
                    dict
                )
                and
                not bool(
                    notification.get(
                        "is_read",
                        False
                    )
                )
            )
        )

        # ====================================================
        # Notification Summary
        # ====================================================

        st.success(
            f"{len(notifications)} notification(s) loaded."
        )

        if unread_count > 0:

            st.warning(
                f"🔴 {unread_count} unread notification(s)"
            )

        else:

            st.success(
                "🟢 All notifications are read."
            )

        # ====================================================
        # MARK ALL AS READ
        # ====================================================

        if unread_count > 0:

            if st.button(
                "Mark All as Read",
                key="mark_all_notifications_read"
            ):

                try:

                    mark_all_response = (
                        mark_all_notifications_read(
                            access_token
                        )
                    )

                    # Accept both normal FastAPI 200
                    # and possible 204 responses.
                    if mark_all_response.status_code in [
                        200,
                        204
                    ]:

                        # Update local notification state.
                        for notification in notifications:

                            if isinstance(
                                notification,
                                dict
                            ):

                                notification["is_read"] = True

                        st.session_state.notifications_data = (
                            notifications
                        )

                        st.success(
                            "All notifications marked as read."
                        )

                        st.rerun()

                    elif mark_all_response.status_code == 401:

                        st.error(
                            "Authentication failed. "
                            "Please login again."
                        )

                    elif mark_all_response.status_code == 403:

                        st.error(
                            "You do not have permission "
                            "to update notifications."
                        )

                    else:

                        try:

                            data = (
                                mark_all_response.json()
                            )

                            st.error(
                                data.get(
                                    "detail",
                                    "Failed to mark all "
                                    "notifications as read."
                                )
                            )

                        except Exception:

                            st.error(
                                f"Error: "
                                f"{mark_all_response.status_code}"
                            )

                except Exception as e:

                    st.error(
                        "Unable to connect to backend: "
                        f"{e}"
                    )

        st.divider()

        # ====================================================
        # DISPLAY EACH NOTIFICATION
        # ====================================================

        for index, notification in enumerate(
            notifications
        ):

            if not isinstance(
                notification,
                dict
            ):

                continue

            notification_id = notification.get(
                "id"
            )

            title = notification.get(
                "title",
                "Notification"
            )

            message = notification.get(
                "message",
                ""
            )

            notification_type = notification.get(
                "notification_type",
                ""
            )

            is_read = bool(
                notification.get(
                    "is_read",
                    False
                )
            )

            created_at = notification.get(
                "created_at",
                ""
            )

            project_id = notification.get(
                "project_id"
            )

            # ====================================================
            # Notification Container
            # ====================================================

            with st.container(
                border=True
            ):

                # ------------------------------------------------
                # Header
                # ------------------------------------------------

                header_col, status_col = st.columns(
                    [4, 1]
                )

                with header_col:

                    st.markdown(
                        f"### 🔔 {title}"
                    )

                with status_col:

                    if is_read:

                        st.success(
                            "🟢 Read"
                        )

                    else:

                        st.error(
                            "🔴 Unread"
                        )

                # ------------------------------------------------
                # Message
                # ------------------------------------------------

                if message:

                    st.write(
                        message
                    )

                # ------------------------------------------------
                # Metadata
                # ------------------------------------------------

                metadata = []

                if notification_id is not None:

                    metadata.append(
                        f"Notification ID: {notification_id}"
                    )

                if project_id is not None:

                    metadata.append(
                        f"Project ID: {project_id}"
                    )

                if notification_type:

                    metadata.append(
                        f"Type: {notification_type}"
                    )

                if created_at:

                    metadata.append(
                        f"Created: {created_at}"
                    )

                if metadata:

                    st.caption(
                        " | ".join(metadata)
                    )

                # ====================================================
                # INDIVIDUAL MARK AS READ BUTTON
                # ====================================================

                if (
                    not is_read
                    and
                    notification_id is not None
                ):

                    if st.button(
                        "Mark as Read",
                        key=(
                            f"inline_mark_read_"
                            f"{notification_id}_"
                            f"{index}"
                        )
                    ):

                        try:

                            mark_response = (
                                mark_notification_read(
                                    access_token,
                                    int(notification_id)
                                )
                            )

                            # Accept 200 or 204.
                            if mark_response.status_code in [
                                200,
                                204
                            ]:

                                # Update only the clicked
                                # notification.
                                notification["is_read"] = True

                                st.session_state.notifications_data = (
                                    notifications
                                )

                                st.success(
                                    "Notification marked as read."
                                )

                                st.rerun()

                            elif mark_response.status_code == 401:

                                st.error(
                                    "Authentication failed. "
                                    "Please login again."
                                )

                            elif mark_response.status_code == 403:

                                st.error(
                                    "You do not have permission "
                                    "to update this notification."
                                )

                            else:

                                try:

                                    data = (
                                        mark_response.json()
                                    )

                                    st.error(
                                        data.get(
                                            "detail",
                                            "Failed to mark "
                                            "notification as read."
                                        )
                                    )

                                except Exception:

                                    st.error(
                                        f"Error: "
                                        f"{mark_response.status_code}"
                                    )

                        except Exception as e:

                            st.error(
                                "Unable to connect to backend: "
                                f"{e}"
                            )

                else:

                    st.caption(
                        "✓ This notification has already been read."
                    )

            st.write("")

    # ========================================================
    # View Notification By ID
    # ========================================================

    elif action == "View Notification by ID":

        st.subheader(
            "View Notification"
        )

        notification_id = st.number_input(
            "Notification ID",
            min_value=1,
            step=1,
            key="notification_view_id"
        )

        if st.button(
            "Get Notification",
            key="get_notification_by_id"
        ):

            try:

                response = get_notification(
                    access_token,
                    int(notification_id)
                )

                if response.status_code == 200:

                    st.success(
                        "Notification retrieved successfully."
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
                        "to view this notification."
                    )

                else:

                    try:

                        data = response.json()

                        st.error(
                            data.get(
                                "detail",
                                "Notification not found."
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

    # ========================================================
    # Mark Notification As Read
    # ========================================================

    elif action == "Mark as Read":

        st.subheader(
            "Mark Notification as Read"
        )

        notification_id = st.number_input(
            "Notification ID",
            min_value=1,
            step=1,
            key="notification_read_id"
        )

        if st.button(
            "Mark as Read",
            key="manual_mark_notification_read"
        ):

            try:

                response = mark_notification_read(
                    access_token,
                    int(notification_id)
                )

                if response.status_code in [
                    200,
                    204
                ]:

                    st.success(
                        "Notification marked as read."
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
                        "You do not have permission "
                        "to update this notification."
                    )

                else:

                    try:

                        data = response.json()

                        st.error(
                            data.get(
                                "detail",
                                "Failed to mark "
                                "notification as read."
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

    # ========================================================
    # Delete Notification
    # ========================================================

    elif action == "Delete Notification":

        # ====================================================
        # Frontend RBAC Protection
        # ====================================================
        #
        # Only:
        #
        # Admin
        # Employee + Contributor
        #
        # can reach this operation.
        #
        # Employee + Member should never see this option.
        #
        # ====================================================

        if not can_delete_notification:

            st.error(
                "Employee + Member cannot delete notifications."
            )

            return

        st.subheader(
            "Delete Notification"
        )

        notification_id = st.number_input(
            "Notification ID",
            min_value=1,
            step=1,
            key="notification_delete_id"
        )

        if st.button(
            "Delete Notification",
            key="delete_notification_button"
        ):

            try:

                response = delete_notification(
                    access_token,
                    int(notification_id)
                )

                if response.status_code in [
                    200,
                    204
                ]:

                    st.success(
                        "Notification deleted successfully."
                    )

                    # Remove deleted notification from
                    # local session state if it exists.
                    notifications = st.session_state.get(
                        "notifications_data"
                    )

                    if isinstance(
                        notifications,
                        list
                    ):

                        st.session_state.notifications_data = [
                            notification
                            for notification in notifications
                            if not (
                                isinstance(
                                    notification,
                                    dict
                                )
                                and
                                notification.get("id") == int(
                                    notification_id
                                )
                            )
                        ]

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
                        "Only Admin or Contributor "
                        "can delete notifications."
                    )

                else:

                    try:

                        data = response.json()

                        st.error(
                            data.get(
                                "detail",
                                "Failed to delete notification."
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