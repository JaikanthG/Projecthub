import streamlit as st

from api_client import (
    get_rca_reports,
    get_rca_report,
    create_rca_report,
    update_rca_report,
    delete_rca_report
)


# ==========================================
# RCA Reports Page
# ==========================================

def show_rca_reports():

    st.title("RCA Reports")

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
    # CURRENT USER
    # ==========================================

    user_data = st.session_state.get(
        "user",
        {}
    )

    if not isinstance(
        user_data,
        dict
    ):

        user_data = {}

    # ==========================================
    # GLOBAL / SYSTEM ROLE
    # ==========================================

    current_role = str(
        st.session_state.get(
            "role",
            user_data.get(
                "role",
                ""
            )
        )
    ).lower().strip()

    # ==========================================
    # PROJECT ROLE
    # ==========================================

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
    # PERMISSION RULES
    #
    # ADMIN
    #   View
    #   Create
    #   Update
    #   Delete
    #
    # EMPLOYEE + CONTRIBUTOR
    #   View
    #   Create
    #   Update
    #
    # EMPLOYEE + MEMBER
    #   View
    # ==========================================

    is_admin = (
        current_role == "admin"
    )

    is_contributor = (
        current_role == "employee"
        and
        project_role == "contributor"
    )

    can_create_rca = (
        is_admin
        or
        is_contributor
    )

    can_update_rca = (
        is_admin
        or
        is_contributor
    )

    can_delete_rca = (
        is_admin
    )

    # ==========================================
    # CURRENT PROJECT DISPLAY
    # ==========================================

    st.info(
        f"Current Project ID: {current_project_id}"
    )

    # ==========================================
    # RCA ACTIONS
    # ==========================================

    if is_admin:

        rca_actions = [
            "View RCA Reports",
            "View RCA Report by ID",
            "Create RCA Report",
            "Update RCA Report",
            "Delete RCA Report"
        ]

    elif is_contributor:

        rca_actions = [
            "View RCA Reports",
            "View RCA Report by ID",
            "Create RCA Report",
            "Update RCA Report"
        ]

    else:

        rca_actions = [
            "View RCA Reports",
            "View RCA Report by ID"
        ]

    # ==========================================
    # NAVIGATION
    # ==========================================

    action = st.selectbox(
        "RCA Action",
        rca_actions
    )

    # ==========================================
    # VIEW RCA REPORTS
    # ==========================================

    if action == "View RCA Reports":

        st.subheader(
            "RCA Reports"
        )

        if st.button(
            "Load RCA Reports",
            key="load_rca_reports_button"
        ):

            try:

                # ------------------------------------------
                # IMPORTANT:
                # Always use the current project endpoint.
                #
                # Do NOT call:
                # get_rca_reports(access_token)
                #
                # because that calls global /rca/
                # ------------------------------------------

                response = get_rca_reports(
                    access_token,
                    project_id=current_project_id
                )

                if response.status_code == 200:

                    reports = response.json()

                    if reports:

                        st.success(
                            f"{len(reports)} "
                            "RCA report(s) found."
                        )

                        st.dataframe(
                            reports,
                            use_container_width=True,
                            hide_index=True
                        )

                    else:

                        st.info(
                            "No RCA reports found "
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
                        "to view RCA reports for this project."
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
                                "Failed to load RCA reports."
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
    # VIEW RCA REPORT BY ID
    # ==========================================

    elif action == "View RCA Report by ID":

        st.subheader(
            "View RCA Report"
        )

        rca_id = st.number_input(
            "RCA Report ID",
            min_value=1,
            step=1,
            key="rca_view_id"
        )

        if st.button(
            "Get RCA Report",
            key="get_rca_report_button"
        ):

            try:

                response = get_rca_report(
                    access_token,
                    int(rca_id)
                )

                if response.status_code == 200:

                    report = response.json()

                    # ------------------------------------------
                    # Frontend project safety check
                    # ------------------------------------------

                    if isinstance(
                        report,
                        dict
                    ):

                        report_project_id = report.get(
                            "project_id"
                        )

                        if (
                            report_project_id is not None
                            and
                            int(report_project_id)
                            != current_project_id
                        ):

                            st.error(
                                "This RCA report does not belong "
                                "to the current project."
                            )

                            return

                    st.success(
                        "RCA report retrieved successfully."
                    )

                    st.json(
                        report
                    )

                elif response.status_code == 401:

                    st.error(
                        "Authentication failed. "
                        "Please login again."
                    )

                elif response.status_code == 403:

                    st.error(
                        "You do not have permission "
                        "to view this RCA report."
                    )

                elif response.status_code == 404:

                    st.error(
                        "RCA report not found."
                    )

                else:

                    try:

                        error_data = response.json()

                        st.error(
                            error_data.get(
                                "detail",
                                "RCA report not found."
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
    # CREATE RCA REPORT
    # ==========================================

    elif action == "Create RCA Report":

        if not can_create_rca:

            st.error(
                "Only Admin or Contributor "
                "can create RCA reports."
            )

            return

        st.subheader(
            "Create RCA Report"
        )

        # ------------------------------------------
        # Current Project
        # ------------------------------------------

        st.text_input(
            "Current Project ID",
            value=str(
                current_project_id
            ),
            disabled=True
        )

        bug_id = st.number_input(
            "Bug ID",
            min_value=1,
            step=1,
            key="rca_create_bug_id"
        )

        root_cause = st.text_area(
            "Root Cause",
            key="rca_create_root_cause"
        )

        impact = st.text_area(
            "Impact",
            key="rca_create_impact"
        )

        corrective_action = st.text_area(
            "Corrective Action",
            key="rca_create_corrective_action"
        )

        preventive_action = st.text_area(
            "Preventive Action",
            key="rca_create_preventive_action"
        )

        if st.button(
            "Create RCA Report",
            key="create_rca_report_button"
        ):

            rca_data = {
                "bug_id": int(bug_id),
                "root_cause": root_cause,
                "impact": impact,
                "corrective_action": corrective_action,
                "preventive_action": preventive_action
            }

            try:

                response = create_rca_report(
                    access_token,
                    rca_data
                )

                if response.status_code in [
                    200,
                    201
                ]:

                    st.success(
                        "RCA report created successfully."
                    )

                    st.json(
                        response.json()
                    )

                elif response.status_code == 403:

                    st.error(
                        "Only Admin or Contributor "
                        "can create RCA reports "
                        "for this project."
                    )

                elif response.status_code == 404:

                    st.error(
                        "Bug not found."
                    )

                else:

                    try:

                        error_data = response.json()

                        st.error(
                            error_data.get(
                                "detail",
                                "Failed to create RCA report."
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
    # UPDATE RCA REPORT
    # ==========================================

    elif action == "Update RCA Report":

        if not can_update_rca:

            st.error(
                "Only Admin or Contributor "
                "can update RCA reports."
            )

            return

        st.subheader(
            "Update RCA Report"
        )

        rca_id = st.number_input(
            "RCA Report ID",
            min_value=1,
            step=1,
            key="rca_update_id"
        )

        root_cause = st.text_area(
            "Root Cause",
            key="update_root_cause"
        )

        impact = st.text_area(
            "Impact",
            key="update_impact"
        )

        corrective_action = st.text_area(
            "Corrective Action",
            key="update_corrective_action"
        )

        preventive_action = st.text_area(
            "Preventive Action",
            key="update_preventive_action"
        )

        if st.button(
            "Update RCA Report",
            key="update_rca_report_button"
        ):

            rca_data = {
                "root_cause": root_cause,
                "impact": impact,
                "corrective_action": corrective_action,
                "preventive_action": preventive_action
            }

            try:

                response = update_rca_report(
                    access_token,
                    int(rca_id),
                    rca_data
                )

                if response.status_code == 200:

                    st.success(
                        "RCA report updated successfully."
                    )

                    st.json(
                        response.json()
                    )

                elif response.status_code == 403:

                    st.error(
                        "Only Admin or Contributor "
                        "can update RCA reports."
                    )

                elif response.status_code == 404:

                    st.error(
                        "RCA report not found."
                    )

                else:

                    try:

                        error_data = response.json()

                        st.error(
                            error_data.get(
                                "detail",
                                "Failed to update RCA report."
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
    # DELETE RCA REPORT
    # ==========================================

    elif action == "Delete RCA Report":

        if not can_delete_rca:

            st.error(
                "Only Admin can delete RCA reports."
            )

            return

        st.subheader(
            "Delete RCA Report"
        )

        rca_id = st.number_input(
            "RCA Report ID",
            min_value=1,
            step=1,
            key="rca_delete_id"
        )

        if st.button(
            "Delete RCA Report",
            key="delete_rca_report_button"
        ):

            try:

                response = delete_rca_report(
                    access_token,
                    int(rca_id)
                )

                if response.status_code in [
                    200,
                    204
                ]:

                    st.success(
                        "RCA report deleted successfully."
                    )

                    if response.text:

                        try:

                            st.json(
                                response.json()
                            )

                        except Exception:

                            pass

                elif response.status_code == 403:

                    st.error(
                        "Only Admin can delete RCA reports."
                    )

                elif response.status_code == 404:

                    st.error(
                        "RCA report not found."
                    )

                else:

                    try:

                        error_data = response.json()

                        st.error(
                            error_data.get(
                                "detail",
                                "Failed to delete RCA report."
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