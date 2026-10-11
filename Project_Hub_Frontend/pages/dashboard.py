import streamlit as st

from api_client import (
    get_projects,
    get_project,
    get_tasks,
    get_bugs,
    get_knowledge,
    get_project_members,
    get_documents,
)


# ============================================================
# RESPONSE COUNT HELPER
# ============================================================

def _get_count_from_response(response, possible_keys):
    """
    Extract a count safely from an API response.

    Supported formats:

    List:
        [{...}, {...}]

    Dictionary containing a list:
        {"tasks": [...]}

    Dictionary containing count:
        {"count": 5}

    Dictionary containing total:
        {"total": 5}
    """

    if response is None:
        return 0

    if response.status_code != 200:
        return 0

    try:
        data = response.json()
    except Exception:
        return 0

    # --------------------------------------------------------
    # Direct list response
    # --------------------------------------------------------

    if isinstance(data, list):
        return len(data)

    # --------------------------------------------------------
    # Dictionary response
    # --------------------------------------------------------

    if isinstance(data, dict):

        if "count" in data:
            try:
                return int(data["count"])
            except Exception:
                pass

        if "total" in data:
            try:
                return int(data["total"])
            except Exception:
                pass

        for key in possible_keys:

            value = data.get(key)

            if isinstance(value, list):
                return len(value)

    return 0


# ============================================================
# GET PROJECT NAME
# ============================================================

def _get_project_name(
    access_token,
    project_id,
):
    try:

        response = get_project(
            access_token,
            project_id,
        )

        if response.status_code != 200:
            return f"Project {project_id}"

        data = response.json()

        if isinstance(data, dict):

            return (
                data.get("name")
                or data.get("project_name")
                or f"Project {project_id}"
            )

    except Exception:
        pass

    return f"Project {project_id}"


# ============================================================
# LOAD SINGLE PROJECT COUNTS
# ============================================================

def _load_project_counts(
    access_token,
    project_id,
):
    """
    Load statistics for one project.

    This function is used for:
        - Non-admin current-project dashboard
        - Admin all-project aggregation
    """

    counts = {
        "tasks": 0,
        "bugs": 0,
        "knowledge": 0,
        "members": 0,
        "documents": 0,
    }

    # ========================================================
    # TASKS
    # ========================================================

    try:

        response = get_tasks(
            access_token,
            project_id,
        )

        counts["tasks"] = _get_count_from_response(
            response,
            [
                "tasks",
                "items",
                "data",
            ],
        )

    except Exception:
        counts["tasks"] = 0


    # ========================================================
    # BUGS
    # ========================================================

    try:

        response = get_bugs(
            access_token,
            project_id,
        )

        counts["bugs"] = _get_count_from_response(
            response,
            [
                "bugs",
                "items",
                "data",
            ],
        )

    except Exception:
        counts["bugs"] = 0


    # ========================================================
    # KNOWLEDGE
    # ========================================================

    try:

        response = get_knowledge(
            access_token,
            project_id,
        )

        counts["knowledge"] = _get_count_from_response(
            response,
            [
                "knowledge",
                "items",
                "data",
            ],
        )

    except Exception:
        counts["knowledge"] = 0


    # ========================================================
    # PROJECT MEMBERS
    # ========================================================

    try:

        response = get_project_members(
            access_token,
            project_id,
        )

        counts["members"] = _get_count_from_response(
            response,
            [
                "members",
                "project_members",
                "items",
                "data",
            ],
        )

    except Exception:
        counts["members"] = 0


    # ========================================================
    # DOCUMENTS
    # ========================================================

    try:

        response = get_documents(
            access_token,
            project_id,
        )

        counts["documents"] = _get_count_from_response(
            response,
            [
                "documents",
                "items",
                "data",
            ],
        )

    except Exception:
        counts["documents"] = 0


    return counts


# ============================================================
# LOAD ALL PROJECT COUNTS
# ============================================================

def _load_all_project_counts(
    access_token,
    projects,
):
    """
    Aggregate statistics across all projects.

    Used only for Admin dashboard.
    """

    total_counts = {
        "tasks": 0,
        "bugs": 0,
        "knowledge": 0,
        "members": 0,
        "documents": 0,
    }

    for project in projects:

        if not isinstance(project, dict):
            continue

        project_id = project.get("id")

        if project_id is None:
            continue

        try:
            project_id = int(project_id)
        except (TypeError, ValueError):
            continue

        project_counts = _load_project_counts(
            access_token,
            project_id,
        )

        total_counts["tasks"] += project_counts["tasks"]
        total_counts["bugs"] += project_counts["bugs"]
        total_counts["knowledge"] += project_counts["knowledge"]
        total_counts["members"] += project_counts["members"]
        total_counts["documents"] += project_counts["documents"]

    return total_counts


# ============================================================
# LOAD ALL PROJECTS
# ============================================================

def _load_projects(
    access_token,
):
    """
    Load all projects for Admin dashboard.
    """

    try:

        response = get_projects(
            access_token
        )

        if response.status_code != 200:
            return []

        data = response.json()

        # ----------------------------------------------------
        # Backend format:
        # {"count": 8, "projects": [...]}
        # ----------------------------------------------------

        if isinstance(data, dict):

            projects = data.get(
                "projects",
                []
            )

            if isinstance(projects, list):
                return projects

            return []

        # ----------------------------------------------------
        # Backend direct list format
        # ----------------------------------------------------

        if isinstance(data, list):
            return data

    except Exception:
        pass

    return []


# ============================================================
# GET CURRENT USER ROLE
# ============================================================

def _get_current_role():
    """
    Resolve global application role.

    Admin is determined from the global user role,
    not from the project role.
    """

    current_user = st.session_state.get(
        "user",
        {}
    )

    if isinstance(current_user, dict):

        role = current_user.get(
            "role"
        )

        if role:
            return str(
                role
            ).strip().lower()

    return str(
        st.session_state.get(
            "role",
            ""
        )
    ).strip().lower()


# ============================================================
# DASHBOARD
# ============================================================

def show_dashboard():

    # ========================================================
    # AUTHENTICATION
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
    # GLOBAL ROLE
    # ========================================================

    current_role = _get_current_role()

    is_admin = (
        current_role == "admin"
    )


    # ========================================================
    # DASHBOARD MODE
    # ========================================================

    if is_admin:

        # ====================================================
        # ADMIN DASHBOARD
        #
        # Admin does NOT need a current project.
        # Dashboard shows statistics across ALL projects.
        # ====================================================

        projects = _load_projects(
            access_token
        )

        total_project_count = len(
            projects
        )

        counts = _load_all_project_counts(
            access_token,
            projects,
        )

        total_tasks = counts["tasks"]
        total_bugs = counts["bugs"]
        total_knowledge = counts["knowledge"]
        total_members = counts["members"]
        total_documents = counts["documents"]

        dashboard_title = "📊 Admin Dashboard"
        dashboard_subtitle = (
            "Workspace Overview: "
            "<b>All Projects</b>"
        )

        summary_title = "📌 All Projects"

        summary_subtitle = (
            "Overall workspace statistics"
        )

        overview_title = (
            "📈 Workspace Overview"
        )

        overview_subtitle = (
            "Statistics shown above include "
            "all projects in the workspace."
        )

        footer_text = (
            "Dashboard statistics are scoped to "
            "<b>All Projects</b>. "
            "No current project selection is required for Admin."
        )


    else:

        # ====================================================
        # NON-ADMIN DASHBOARD
        #
        # Employee / Contributor / Member must select
        # a current project.
        # ====================================================

        current_project_id = st.session_state.get(
            "current_project_id"
        )

        if current_project_id is None:

            st.warning(
                "Please select a current project first."
            )

            st.info(
                "Go to Projects → select a project → "
                "Set Current Project."
            )

            return


        # ====================================================
        # VALIDATE PROJECT ID
        # ====================================================

        try:

            current_project_id = int(
                current_project_id
            )

        except (TypeError, ValueError):

            st.error(
                "Invalid current project ID."
            )

            return


        # ====================================================
        # PROJECT INFORMATION
        # ====================================================

        project_name = _get_project_name(
            access_token,
            current_project_id,
        )


        # ====================================================
        # PROJECT COUNTS
        # ====================================================

        counts = _load_project_counts(
            access_token,
            current_project_id,
        )

        total_tasks = counts["tasks"]
        total_bugs = counts["bugs"]
        total_knowledge = counts["knowledge"]
        total_members = counts["members"]
        total_documents = counts["documents"]


        # ====================================================
        # NON-ADMIN DISPLAY INFORMATION
        # ====================================================

        dashboard_title = (
            "📊 Project Dashboard"
        )

        dashboard_subtitle = (
            f"Current Project: "
            f"<b>{project_name}</b>"
            f"&nbsp; | &nbsp;"
            f"Project ID: "
            f"<b>{current_project_id}</b>"
        )

        summary_title = (
            f"📌 {project_name}"
        )

        summary_subtitle = (
            "Project-specific statistics"
        )

        overview_title = (
            "📈 Project Overview"
        )

        overview_subtitle = (
            "Statistics shown above belong only "
            "to the currently selected project."
        )

        footer_text = (
            f"Dashboard statistics are scoped to "
            f"<b>{project_name}</b> "
            f"(Project ID: {current_project_id}). "
            f"No statistics from other projects are included."
        )


    # ========================================================
    # PAGE HEADER
    # ========================================================

    st.markdown(
        f"""
<div class="page-title">
{dashboard_title}
</div>

<div class="page-subtitle">
{dashboard_subtitle}
</div>
""",
        unsafe_allow_html=True,
    )


    # ========================================================
    # SUMMARY
    # ========================================================

    st.markdown(
        f"""
<div class="section-card">

<div class="section-title">
{summary_title}
</div>

<div class="section-subtitle">
{summary_subtitle}
</div>

</div>
""",
        unsafe_allow_html=True,
    )


    # ========================================================
    # KPI ROW 1
    # ========================================================

    col1, col2, col3 = st.columns(3)


    # --------------------------------------------------------
    # TASKS
    # --------------------------------------------------------

    with col1:

        task_description = (
            "Tasks across all projects"
            if is_admin
            else f"Tasks in {project_name}"
        )

        st.markdown(
            f"""
<div class="kpi-card">

<div class="kpi-icon">
✅
</div>

<div class="kpi-label">
TOTAL TASKS
</div>

<div class="kpi-value">
{total_tasks}
</div>

<div class="kpi-description">
{task_description}
</div>

</div>
""",
            unsafe_allow_html=True,
        )


    # --------------------------------------------------------
    # BUGS
    # --------------------------------------------------------

    with col2:

        bug_description = (
            "Bugs across all projects"
            if is_admin
            else f"Bugs in {project_name}"
        )

        st.markdown(
            f"""
<div class="kpi-card">

<div class="kpi-icon">
🐞
</div>

<div class="kpi-label">
TOTAL BUGS
</div>

<div class="kpi-value">
{total_bugs}
</div>

<div class="kpi-description">
{bug_description}
</div>

</div>
""",
            unsafe_allow_html=True,
        )


    # --------------------------------------------------------
    # KNOWLEDGE
    # --------------------------------------------------------

    with col3:

        knowledge_description = (
            "Knowledge resources across all projects"
            if is_admin
            else f"Knowledge resources in {project_name}"
        )

        st.markdown(
            f"""
<div class="kpi-card">

<div class="kpi-icon">
📚
</div>

<div class="kpi-label">
TOTAL KNOWLEDGE
</div>

<div class="kpi-value">
{total_knowledge}
</div>

<div class="kpi-description">
{knowledge_description}
</div>

</div>
""",
            unsafe_allow_html=True,
        )


    # ========================================================
    # SPACING
    # ========================================================

    st.markdown(
        "<br>",
        unsafe_allow_html=True,
    )


    # ========================================================
    # KPI ROW 2
    # ========================================================

    col4, col5, col6 = st.columns(3)


    # --------------------------------------------------------
    # MEMBERS
    # --------------------------------------------------------

    with col4:

        member_description = (
            "Members across all projects"
            if is_admin
            else f"Members assigned to {project_name}"
        )

        st.markdown(
            f"""
<div class="kpi-card">

<div class="kpi-icon">
👥
</div>

<div class="kpi-label">
TOTAL MEMBERS
</div>

<div class="kpi-value">
{total_members}
</div>

<div class="kpi-description">
{member_description}
</div>

</div>
""",
            unsafe_allow_html=True,
        )


    # --------------------------------------------------------
    # DOCUMENTS
    # --------------------------------------------------------

    with col5:

        document_description = (
            "Documents across all projects"
            if is_admin
            else f"Documents uploaded to {project_name}"
        )

        st.markdown(
            f"""
<div class="kpi-card">

<div class="kpi-icon">
📄
</div>

<div class="kpi-label">
TOTAL DOCUMENTS
</div>

<div class="kpi-value">
{total_documents}
</div>

<div class="kpi-description">
{document_description}
</div>

</div>
""",
            unsafe_allow_html=True,
        )


    # --------------------------------------------------------
    # PROJECT COUNT / CURRENT PROJECT
    # --------------------------------------------------------

    with col6:

        if is_admin:

            st.markdown(
                f"""
<div class="kpi-card">

<div class="kpi-icon">
📁
</div>

<div class="kpi-label">
TOTAL PROJECTS
</div>

<div class="kpi-value">
{total_project_count}
</div>

<div class="kpi-description">
Projects in workspace
</div>

</div>
""",
                unsafe_allow_html=True,
            )

        else:

            st.markdown(
                f"""
<div class="kpi-card">

<div class="kpi-icon">
📁
</div>

<div class="kpi-label">
CURRENT PROJECT
</div>

<div class="kpi-value">
#{current_project_id}
</div>

<div class="kpi-description">
{project_name}
</div>

</div>
""",
                unsafe_allow_html=True,
            )


    # ========================================================
    # OVERVIEW
    # ========================================================

    st.markdown(
        "<br>",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
<div class="section-card">

<div class="section-title">
{overview_title}
</div>

<div class="section-subtitle">
{overview_subtitle}
</div>

</div>
""",
        unsafe_allow_html=True,
    )


    # ========================================================
    # QUICK SUMMARY
    # ========================================================

    st.markdown(
        "<br>",
        unsafe_allow_html=True,
    )

    summary_col1, summary_col2 = st.columns(2)


    with summary_col1:

        st.metric(
            "Knowledge Resources",
            total_knowledge,
        )

        st.metric(
            "Bugs",
            total_bugs,
        )


    with summary_col2:

        st.metric(
            "Tasks",
            total_tasks,
        )

        st.metric(
            "Members",
            total_members,
        )


    # ========================================================
    # FOOTER
    # ========================================================

    st.markdown(
        f"""
<div class="app-footer">
{footer_text}
</div>
""",
        unsafe_allow_html=True,
    )