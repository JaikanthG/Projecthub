# Project Hub API Documentation

## Purpose

This file explains the Project Hub API flow and the purpose of each API module.

Base URL:
http://127.0.0.1:3000

Swagger:
http://127.0.0.1:3000/docs

---

## API Flow

Client
  ↓
Router
  ↓
Schema Validation
  ↓
Authentication
  ↓
Service
  ↓
Repository
  ↓
PostgreSQL
  ↓
Response

---

## 1. Authentication

Register:
POST /register

Login:
POST /login

Current User:
GET /me

Get Users:
GET /users

Login returns a JWT token.

Protected APIs use:

Authorization: Bearer <JWT_TOKEN>

---

## 2. Project Management

Purpose:
Create and manage projects.

Main operations:

POST   /projects/
GET    /projects/
GET    /projects/{project_id}
PUT    /projects/{project_id}
DELETE /projects/{project_id}

Flow:

Project Request
  ↓
Project Router
  ↓
Project Service
  ↓
Project Repository
  ↓
Database

---

## 3. Project Member Management

Base path:

/project-members

Assign Member:
POST /project-members/assign

Request:

{
    "project_id": 1,
    "user_id": 5,
    "permission": "contributor"
}

Flow:

Admin
  ↓
Check Project
  ↓
Check User
  ↓
Check Duplicate
  ↓
Validate Permission
  ↓
Assign Member
  ↓
Activity / Notification

Get Members:
GET /project-members/project/{project_id}

Update Permission:
PUT /project-members/{member_id}

Remove Member:
DELETE /project-members/{member_id}

---

## 4. Knowledge Management

Purpose:
Store and manage project knowledge.

Operations:

Create Knowledge
Get Knowledge
Get Knowledge By ID
Update Knowledge
Delete Knowledge

Knowledge contains:

Title
Content
Tags
Project
Version
Status
Created By

Future:

Knowledge
  ↓
RAG
  ↓
AI Assistant

---

## 5. Task Management

Purpose:
Manage project work.

Operations:

Create Task
Get All Tasks
Get Task By ID
Update Task
Delete Task
Assign Task
Update Task Status

Assign Task:

POST /tasks/{task_id}/assign

Request:

{
    "assigned_to": 5
}

Flow:

Admin
  ↓
Validate Task
  ↓
Validate User
  ↓
Assign Task
  ↓
Activity Log
  ↓
Notification

Update Status:

PUT /tasks/{task_id}/status

Request:

{
    "status": "in_progress"
}

---

## 6. Bug Management

Purpose:
Track software defects.

Operations:

Create Bug
Get Bugs
Get Bug By ID
Update Bug
Delete Bug
Assign Bug
Update Bug Status

Assign Bug:

POST /bugs/{bug_id}/assign

Request:

{
    "assigned_to": 5
}

Flow:

Admin
  ↓
Validate Bug
  ↓
Validate User
  ↓
Assign Bug
  ↓
Activity Log
  ↓
Notification

---

## 7. Document Management

Purpose:
Manage project documents.

Operations:

Upload Document
Get Documents
Get Document
Delete Document

Database stores:

file_name
file_path
file_type
uploaded_by
project_id

Actual files are stored in the configured upload directory.

---

## 8. Activity Log

Purpose:
Track who performed what operation.

Example:

Admin
  ↓
Assign Task
  ↓
Activity Log

Tracks:

User
Action
Entity Type
Entity ID
Description
Time
Project

Activity Log:
"What happened and who performed it?"

---

## 9. Notification

Purpose:
Inform users about important operations.

Operations:

GET    /notifications/
GET    /notifications/unread
GET    /notifications/{notification_id}
PUT    /notifications/{notification_id}/read
PUT    /notifications/read-all
DELETE /notifications/{notification_id}

Example:

Admin assigns Task
  ↓
Task Updated
  ↓
Notification Created
  ↓
Assigned Employee
  ↓
GET /notifications/unread

Activity Log:
"What happened?"

Notification:
"Who needs to know?"

---

## 10. Dashboard

Purpose:
Give a quick overall project view.

Dashboard can summarize:

Projects
Tasks
Bugs
Members
Activities

Flow:

Project Data
  ↓
Dashboard
  ↓
Quick Overview

---

## 11. Search

Purpose:
Find project information quickly.

Flow:

Search Query
  ↓
Search Module
  ↓
Relevant Results

---

## 12. RCA Reports

RCA = Root Cause Analysis

Purpose:
Find why a problem happened and prevent recurrence.

Flow:

Problem
  ↓
Investigation
  ↓
Root Cause
  ↓
Corrective Action
  ↓
Preventive Action

Bug Management:
"What problem occurred?"

RCA:
"Why did it occur and how do we prevent it?"

---

## Layer Responsibilities

Router:
Handles HTTP requests and routes them to services.

Service:
Handles business logic, validation, permissions and operation rules.

Repository:
Handles database operations.

Schema:
Validates request data.

Auth:
Handles JWT authentication and current user.

Database:
Manages PostgreSQL connections and sessions.

---

## Swagger

Open:

http://127.0.0.1:8000/docs

Swagger allows developers to:

- View APIs
- View request schemas
- Authenticate
- Test APIs
- View responses
- Test errors

---

## Streamlit Integration

Future frontend flow:

Streamlit
  ↓
HTTP API Request
  ↓
FastAPI
  ↓
Router
  ↓
Service
  ↓
Repository
  ↓
PostgreSQL
  ↓
API Response
  ↓
Streamlit UI

The Streamlit frontend does not directly access PostgreSQL.

---

## Future AI Assistant

AI Assistant will be added later.

Expected flow:

User
  ↓
AI Assistant
  ↓
Understand Query
  ↓
Search Project Data / Knowledge
  ↓
Retrieve Relevant Information
  ↓
Generate Response
  ↓
User
