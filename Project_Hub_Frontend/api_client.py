import requests

from config import BACKEND_URL


# ============================================================
# COMMON HEADERS
# ============================================================

def get_auth_headers(
    access_token: str
):
    return {
        "Authorization": f"Bearer {access_token}"
    }


def get_headers(
    access_token: str
):
    return get_auth_headers(
        access_token
    )


# ============================================================
# AUTHENTICATION
# ============================================================

def login(
    username: str,
    password: str
):
    return requests.post(
        f"{BACKEND_URL}/login",
        json={
            "username": username,
            "password": password
        },
        timeout=15
    )


def register_employee(
    username: str,
    full_name: str,
    email: str,
    password: str
):
    payload = {
        "username": username,
        "full_name": full_name,
        "email": email,
        "password": password
    }

    print(
        "REGISTER URL:",
        f"{BACKEND_URL}/register"
    )

    print(
        "REGISTER PAYLOAD:",
        payload
    )

    response = requests.post(
        f"{BACKEND_URL}/register",
        json=payload,
        timeout=15
    )

    print(
        "REGISTER STATUS:",
        response.status_code
    )

    print(
        "REGISTER RESPONSE:",
        response.text
    )

    return response


def admin_create_employee(
    access_token: str,
    username: str,
    full_name: str,
    email: str,
    password: str
):
    return requests.post(
        f"{BACKEND_URL}/users/employees",
        json={
            "username": username,
            "full_name": full_name,
            "email": email,
            "password": password
        },
        headers=get_auth_headers(
            access_token
        ),
        timeout=15
    )


def forgot_password(
    email: str
):
    return requests.post(
        f"{BACKEND_URL}/forgot-password",
        json={
            "email": email
        },
        timeout=15
    )


def reset_password(
    token: str,
    new_password: str
):
    return requests.post(
        f"{BACKEND_URL}/reset-password",
        json={
            "token": token,
            "new_password": new_password
        },
        timeout=15
    )


def get_current_user(
    access_token: str
):
    return requests.get(
        f"{BACKEND_URL}/me",
        headers=get_auth_headers(
            access_token
        ),
        timeout=15
    )


def get_users(
    access_token: str
):
    return requests.get(
        f"{BACKEND_URL}/users",
        headers=get_auth_headers(
            access_token
        ),
        timeout=15
    )


# ============================================================
# DASHBOARD
# ============================================================

def get_dashboard(
    access_token: str
):
    return requests.get(
        f"{BACKEND_URL}/dashboard/summary",
        headers=get_auth_headers(
            access_token
        ),
        timeout=15
    )


# ============================================================
# PROJECTS
# ============================================================

def get_projects(
    access_token: str
):
    return requests.get(
        f"{BACKEND_URL}/projects",
        headers=get_auth_headers(
            access_token
        ),
        timeout=15
    )


def get_project(
    access_token: str,
    project_id: int
):
    return requests.get(
        f"{BACKEND_URL}/projects/{project_id}",
        headers=get_auth_headers(
            access_token
        ),
        timeout=15
    )


def create_project(
    access_token: str,
    project_data: dict
):
    return requests.post(
        f"{BACKEND_URL}/projects",
        json=project_data,
        headers=get_auth_headers(
            access_token
        ),
        timeout=15
    )


def update_project(
    access_token: str,
    project_id: int,
    project_data: dict
):
    return requests.put(
        f"{BACKEND_URL}/projects/{project_id}",
        json=project_data,
        headers=get_auth_headers(
            access_token
        ),
        timeout=15
    )


def delete_project(
    access_token: str,
    project_id: int
):
    return requests.delete(
        f"{BACKEND_URL}/projects/{project_id}",
        headers=get_auth_headers(
            access_token
        ),
        timeout=15
    )


# ============================================================
# PROJECT MEMBERS
# ============================================================

def assign_project_member(
    access_token: str,
    project_id: int,
    user_id: int,
    permission: str
):
    return requests.post(
        f"{BACKEND_URL}/project-members/assign",
        json={
            "project_id": project_id,
            "user_id": user_id,
            "permission": permission
        },
        headers=get_auth_headers(
            access_token
        ),
        timeout=15
    )


def get_project_members(
    access_token: str,
    project_id: int
):
    return requests.get(
        f"{BACKEND_URL}/project-members/project/{project_id}",
        headers=get_auth_headers(
            access_token
        ),
        timeout=15
    )


def update_project_member(
    access_token: str,
    member_id: int,
    permission: str
):
    return requests.put(
        f"{BACKEND_URL}/project-members/{member_id}",
        json={
            "permission": permission
        },
        headers=get_auth_headers(
            access_token
        ),
        timeout=15
    )


def delete_project_member(
    access_token: str,
    member_id: int
):
    return requests.delete(
        f"{BACKEND_URL}/project-members/{member_id}",
        headers=get_auth_headers(
            access_token
        ),
        timeout=15
    )


def remove_project_member(
    access_token: str,
    member_id: int
):
    return delete_project_member(
        access_token,
        member_id
    )


# ============================================================
# KNOWLEDGE
# ============================================================

def get_knowledge(
    access_token: str,
    project_id: int = None
):
    url = f"{BACKEND_URL}/knowledge"

    params = {}

    if project_id is not None:
        params["project_id"] = project_id

    return requests.get(
        url,
        params=params,
        headers=get_auth_headers(
            access_token
        ),
        timeout=15
    )


def get_knowledge_by_id(
    access_token: str,
    knowledge_id: int
):
    return requests.get(
        f"{BACKEND_URL}/knowledge/{knowledge_id}",
        headers=get_auth_headers(
            access_token
        ),
        timeout=15
    )


def create_knowledge(
    access_token: str,
    knowledge_data: dict
):
    return requests.post(
        f"{BACKEND_URL}/knowledge",
        json=knowledge_data,
        headers=get_auth_headers(
            access_token
        ),
        timeout=15
    )


def update_knowledge(
    access_token: str,
    knowledge_id: int,
    knowledge_data: dict
):
    return requests.put(
        f"{BACKEND_URL}/knowledge/{knowledge_id}",
        json=knowledge_data,
        headers=get_auth_headers(
            access_token
        ),
        timeout=15
    )


def delete_knowledge(
    access_token: str,
    knowledge_id: int
):
    return requests.delete(
        f"{BACKEND_URL}/knowledge/{knowledge_id}",
        headers=get_auth_headers(
            access_token
        ),
        timeout=15
    )


# ============================================================
# BUGS
# ============================================================

def get_bugs(
    access_token: str,
    project_id: int = None
):
    url = f"{BACKEND_URL}/bugs"

    params = {}

    if project_id is not None:
        params["project_id"] = project_id

    return requests.get(
        url,
        params=params,
        headers=get_auth_headers(
            access_token
        ),
        timeout=15
    )


def get_bug(
    access_token: str,
    bug_id: int
):
    return requests.get(
        f"{BACKEND_URL}/bugs/{bug_id}",
        headers=get_auth_headers(
            access_token
        ),
        timeout=15
    )


def create_bug(
    access_token: str,
    bug_data: dict
):
    return requests.post(
        f"{BACKEND_URL}/bugs",
        json=bug_data,
        headers=get_auth_headers(
            access_token
        ),
        timeout=15
    )


def update_bug(
    access_token: str,
    bug_id: int,
    bug_data: dict
):
    return requests.put(
        f"{BACKEND_URL}/bugs/{bug_id}",
        json=bug_data,
        headers=get_auth_headers(
            access_token
        ),
        timeout=15
    )


def delete_bug(
    access_token: str,
    bug_id: int
):
    return requests.delete(
        f"{BACKEND_URL}/bugs/{bug_id}",
        headers=get_auth_headers(
            access_token
        ),
        timeout=15
    )


def assign_bug(
    access_token: str,
    bug_id: int,
    assigned_to: int
):
    return requests.put(
        f"{BACKEND_URL}/bugs/{bug_id}/assign",
        json={
            "assigned_to": assigned_to
        },
        headers=get_auth_headers(
            access_token
        ),
        timeout=15
    )


def update_bug_status(
    access_token: str,
    bug_id: int,
    status: str
):
    return requests.put(
        f"{BACKEND_URL}/bugs/{bug_id}/status",
        json={
            "status": status
        },
        headers=get_auth_headers(
            access_token
        ),
        timeout=15
    )


# ============================================================
# TASKS
# ============================================================

def get_tasks(
    access_token: str,
    project_id: int = None
):
    url = f"{BACKEND_URL}/tasks"

    params = {}

    if project_id is not None:
        params["project_id"] = project_id

    return requests.get(
        url,
        params=params,
        headers=get_auth_headers(
            access_token
        ),
        timeout=15
    )


def get_task(
    access_token: str,
    task_id: int
):
    return requests.get(
        f"{BACKEND_URL}/tasks/{task_id}",
        headers=get_auth_headers(
            access_token
        ),
        timeout=15
    )


def create_task(
    access_token: str,
    task_data: dict
):
    return requests.post(
        f"{BACKEND_URL}/tasks",
        json=task_data,
        headers=get_auth_headers(
            access_token
        ),
        timeout=15
    )


def update_task(
    access_token: str,
    task_id: int,
    task_data: dict
):
    return requests.put(
        f"{BACKEND_URL}/tasks/{task_id}",
        json=task_data,
        headers=get_auth_headers(
            access_token
        ),
        timeout=15
    )


def delete_task(
    access_token: str,
    task_id: int
):
    return requests.delete(
        f"{BACKEND_URL}/tasks/{task_id}",
        headers=get_auth_headers(
            access_token
        ),
        timeout=15
    )


def assign_task(
    access_token: str,
    task_id: int,
    assigned_to: int
):
    return requests.put(
        f"{BACKEND_URL}/tasks/{task_id}/assign",
        json={
            "assigned_to": assigned_to
        },
        headers=get_auth_headers(
            access_token
        ),
        timeout=15
    )


def update_task_status(
    access_token: str,
    task_id: int,
    status: str
):
    return requests.put(
        f"{BACKEND_URL}/tasks/{task_id}/status",
        json={
            "status": status
        },
        headers=get_auth_headers(
            access_token
        ),
        timeout=15
    )


# ============================================================
# SEARCH
# ============================================================

def search_projects(
    access_token: str,
    query: str
):
    return requests.get(
        f"{BACKEND_URL}/search/",
        params={
            "q": query
        },
        headers=get_auth_headers(
            access_token
        ),
        timeout=15
    )


def search(
    access_token: str,
    query: str
):
    return search_projects(
        access_token,
        query
    )


def search_all(
    access_token: str,
    query: str
):
    return search_projects(
        access_token,
        query
    )


# ============================================================
# DOCUMENTS
# ============================================================

def get_documents(
    access_token: str,
    project_id: int = None
):
    url = f"{BACKEND_URL}/documents"

    params = {}

    if project_id is not None:
        params["project_id"] = project_id

    return requests.get(
        url,
        params=params,
        headers=get_auth_headers(
            access_token
        ),
        timeout=15
    )


def get_document(
    access_token: str,
    document_id: int
):
    return requests.get(
        f"{BACKEND_URL}/documents/{document_id}",
        headers=get_auth_headers(
            access_token
        ),
        timeout=15
    )


def upload_document(
    access_token: str,
    project_id: int,
    uploaded_file
):
    files = {
        "file": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            uploaded_file.type
        )
    }

    data = {
        "project_id": project_id
    }

    return requests.post(
        f"{BACKEND_URL}/documents/upload",
        data=data,
        files=files,
        headers=get_auth_headers(
            access_token
        ),
        timeout=30
    )


def delete_document(
    access_token: str,
    document_id: int
):
    return requests.delete(
        f"{BACKEND_URL}/documents/{document_id}",
        headers=get_auth_headers(
            access_token
        ),
        timeout=15
    )


# ============================================================
# ACTIVITY
# ============================================================

def get_activities(
    access_token: str
):
    return requests.get(
        f"{BACKEND_URL}/activities/",
        headers=get_auth_headers(
            access_token
        ),
        timeout=15
    )


def get_activity(
    access_token: str,
    activity_id: int
):
    return requests.get(
        f"{BACKEND_URL}/activities/{activity_id}",
        headers=get_auth_headers(
            access_token
        ),
        timeout=15
    )


def get_project_activities(
    access_token: str,
    project_id: int
):
    return requests.get(
        f"{BACKEND_URL}/activities/project/{project_id}",
        headers=get_auth_headers(
            access_token
        ),
        timeout=15
    )


# ============================================================
# NOTIFICATIONS
# ============================================================

def get_notifications(
    access_token: str
):
    return requests.get(
        f"{BACKEND_URL}/notifications",
        headers=get_auth_headers(
            access_token
        ),
        timeout=15
    )


def get_notification(
    access_token: str,
    notification_id: int
):
    return requests.get(
        f"{BACKEND_URL}/notifications/{notification_id}",
        headers=get_auth_headers(
            access_token
        ),
        timeout=15
    )


def mark_notification_read(
    access_token: str,
    notification_id: int
):
    return requests.put(
        f"{BACKEND_URL}/notifications/{notification_id}/read",
        headers=get_auth_headers(
            access_token
        ),
        timeout=15
    )


def mark_all_notifications_read(
    access_token: str
):
    return requests.put(
        f"{BACKEND_URL}/notifications/read-all",
        headers=get_auth_headers(
            access_token
        ),
        timeout=15
    )


def delete_notification(
    access_token: str,
    notification_id: int
):
    return requests.delete(
        f"{BACKEND_URL}/notifications/{notification_id}",
        headers=get_auth_headers(
            access_token
        ),
        timeout=15
    )


# ============================================================
# RCA REPORTS
# ============================================================

def get_rca_reports(
    access_token: str,
    project_id: int = None,
    bug_id: int = None
):
    # Project-specific RCA
    if project_id is not None:
        return requests.get(
            f"{BACKEND_URL}/rca/project/{project_id}",
            headers=get_auth_headers(
                access_token
            ),
            timeout=15
        )

    # Bug-specific RCA
    if bug_id is not None:
        return requests.get(
            f"{BACKEND_URL}/rca/bug/{bug_id}",
            headers=get_auth_headers(
                access_token
            ),
            timeout=15
        )

    # Global RCA - Admin only
    return requests.get(
        f"{BACKEND_URL}/rca/",
        headers=get_auth_headers(
            access_token
        ),
        timeout=15
    )


def get_rca_report(
    access_token: str,
    rca_id: int
):
    return requests.get(
        f"{BACKEND_URL}/rca/{rca_id}",
        headers=get_auth_headers(
            access_token
        ),
        timeout=15
    )


def create_rca(
    access_token: str,
    rca_data: dict
):
    return requests.post(
        f"{BACKEND_URL}/rca",
        json=rca_data,
        headers=get_auth_headers(
            access_token
        ),
        timeout=15
    )


def update_rca(
    access_token: str,
    rca_id: int,
    rca_data: dict
):
    return requests.put(
        f"{BACKEND_URL}/rca/{rca_id}",
        json=rca_data,
        headers=get_auth_headers(
            access_token
        ),
        timeout=15
    )


def delete_rca(
    access_token: str,
    rca_id: int
):
    return requests.delete(
        f"{BACKEND_URL}/rca/{rca_id}",
        headers=get_auth_headers(
            access_token
        ),
        timeout=15
    )


# ============================================================
# FRONTEND COMPATIBILITY ALIASES
# ============================================================

# ------------------------------------------------------------
# Project Member aliases
# ------------------------------------------------------------

remove_project_member = delete_project_member


# ------------------------------------------------------------
# Knowledge aliases
# ------------------------------------------------------------

remove_knowledge = delete_knowledge


# ------------------------------------------------------------
# Bug aliases
# ------------------------------------------------------------

remove_bug = delete_bug


# ------------------------------------------------------------
# Task aliases
# ------------------------------------------------------------

remove_task = delete_task


# ------------------------------------------------------------
# Document aliases
# ------------------------------------------------------------

remove_document = delete_document


# ------------------------------------------------------------
# Notification aliases
# ------------------------------------------------------------

get_notification_by_id = get_notification

read_notification = mark_notification_read

read_all_notifications = mark_all_notifications_read

remove_notification = delete_notification


# ------------------------------------------------------------
# RCA aliases
# ------------------------------------------------------------

create_rca_report = create_rca

update_rca_report = update_rca

delete_rca_report = delete_rca

remove_rca = delete_rca


# ============================================================
# AI AGENT
# ============================================================

def chat_with_ai(
    access_token: str,
    message: str,
    project_id: int
):
    return requests.post(
        f"{BACKEND_URL}/ai/chat",
        json={
            "message": message,
            "project_id": project_id
        },
        headers=get_auth_headers(
            access_token
        ),
        timeout=300
    )


# ============================================================
# PROJECT PERMISSION
# ============================================================

def get_my_project_permission(
    access_token: str,
    project_id: int,
    user_id: int
):
    response = get_project_members(
        access_token,
        project_id
    )

    print(
        "\n========== PROJECT PERMISSION DEBUG =========="
    )

    print(
        "PROJECT ID:",
        project_id
    )

    print(
        "CURRENT USER ID:",
        user_id
    )

    print(
        "STATUS CODE:",
        response.status_code
    )

    print(
        "RAW RESPONSE:",
        response.text
    )

    if response.status_code != 200:

        print(
            "ERROR: Project members API did not return 200"
        )

        print(
            "==============================================\n"
        )

        return None

    try:

        data = response.json()

        print(
            "JSON TYPE:",
            type(data).__name__
        )

        print(
            "JSON DATA:",
            data
        )

        # Backend returned direct list
        if isinstance(data, list):

            members = data

        # Backend returned wrapped response
        elif isinstance(data, dict):

            members = (
                data.get("members")
                or data.get("project_members")
                or data.get("data")
                or []
            )

        else:

            members = []

        print(
            "MEMBERS:",
            members
        )

        for member in members:

            if not isinstance(member, dict):
                continue

            member_user_id = member.get(
                "user_id"
            )

            print(
                "CHECKING MEMBER:",
                member_user_id,
                "AGAINST:",
                user_id
            )

            if member_user_id is None:
                continue

            try:

                is_same_user = (
                    int(member_user_id)
                    == int(user_id)
                )

            except (
                TypeError,
                ValueError
            ):

                continue

            if is_same_user:

                permission = member.get(
                    "permission",
                    "member"
                )

                print(
                    "MATCH FOUND -> PERMISSION:",
                    permission
                )

                print(
                    "==============================================\n"
                )

                return permission

        print(
            "NO MATCHING USER FOUND"
        )

        print(
            "==============================================\n"
        )

        return None

    except Exception as e:

        print(
            "PROJECT PERMISSION PARSE ERROR:",
            repr(e)
        )

        print(
            "==============================================\n"
        )

        return None