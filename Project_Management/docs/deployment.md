# Project Hub Deployment Guide

## 1. Purpose

This guide explains how a new developer can set up and run the Project Hub backend.

Technology:

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- JWT Authentication

---

## 2. Project Flow

New Developer
    ↓
Get Project Source Code
    ↓
Create Virtual Environment
    ↓
Install Dependencies
    ↓
Configure PostgreSQL
    ↓
Configure Database URL
    ↓
Start FastAPI
    ↓
Open Swagger
    ↓
Test APIs

---

## 3. Get the Project

Place the Project Hub source code on the development machine.

Example:

Project_Management/

Make sure the main project files and folders are available.

---

## 4. Create Virtual Environment

Open a terminal inside the project folder.

Windows:

python -m venv myenv

Activate:

myenv\Scripts\activate

Linux / macOS:

python3 -m venv myenv

Activate:

source myenv/bin/activate

---

## 5. Install Dependencies

After activating the virtual environment:

pip install -r requirements.txt

This installs the Python packages required by Project Hub.

---

## 6. Configure PostgreSQL

Project Hub uses PostgreSQL as the database.

Create the database:

project_management

Example PostgreSQL configuration:

Database:
project_management

Username:
postgres

Password:
<your-password>

Host:
localhost

Port:
5432

---

## 7. Configure Database Connection

The database connection is configured in:

database.py

Example:

DATABASE_URL = "postgresql://postgres:<password>@localhost:5432/project_management"

Do not expose real passwords in source control.

For production, sensitive values should be stored in environment variables.

---

## 8. Database Initialization

The application uses SQLAlchemy models.

The models define the main tables:

users
projects
project_members
knowledge
tasks
bugs
documents
activity_logs
notifications

The application initializes the database metadata when configured to do so.

---

## 9. Start the FastAPI Application

Activate the virtual environment first.

Then start the application using the project's configured startup command.

Typical FastAPI development command:

uvicorn main:app --reload

The application should start at:

http://127.0.0.1:8000

---

## 10. Open Swagger

Open:

http://127.0.0.1:8000/docs

Swagger provides an interactive interface to:

- View APIs
- Test APIs
- Send request data
- Authenticate
- View responses
- Check errors

---

## 11. Authentication Setup

First register a user:

POST /register

Then login:

POST /login

The login response provides:

access_token

Use this token for protected APIs:

Authorization: Bearer <access_token>

---

## 12. Recommended Testing Flow

After starting the server:

1. Open Swagger.
2. Register a user.
3. Login.
4. Copy the JWT access token.
5. Authenticate protected APIs.
6. Create a project.
7. Assign project members.
8. Create tasks and bugs.
9. Assign tasks and bugs.
10. Check notifications.
11. Check activity logs.
12. Test dashboard.
13. Test search.
14. Test RCA APIs.

---

## 13. Deployment Architecture

Development:

Developer Machine
      ↓
FastAPI
      ↓
SQLAlchemy
      ↓
PostgreSQL

Frontend Integration:

Streamlit
      ↓
FastAPI APIs
      ↓
Services
      ↓
Repositories
      ↓
PostgreSQL

---

## 14. Production Deployment Concept

For production, the application can be deployed on a server.

Basic flow:

Client / Streamlit
      ↓
Production Server
      ↓
FastAPI Application
      ↓
SQLAlchemy
      ↓
PostgreSQL

Production configuration should use:

- Production database
- Secure environment variables
- Strong JWT secret
- Appropriate application server configuration
- HTTPS
- Proper logging
- Restricted database access

---

## 15. Environment Variables

Sensitive configuration should not be hardcoded.

Recommended configuration:

DATABASE_URL=<database-url>

SECRET_KEY=<strong-secret-key>

Example:

DATABASE_URL=postgresql://postgres:<password>@localhost:5432/project_management

SECRET_KEY=<strong-random-secret>

Never commit real secrets to Git.

---

## 16. Common Problems

### Database Connection Error

Check:

- PostgreSQL is running.
- Database name is correct.
- Username is correct.
- Password is correct.
- Port is correct.
- DATABASE_URL is correct.

---

### Module Not Found

Make sure:

- Virtual environment is activated.
- Dependencies are installed.
- You are running the command from the project root.

Run:

pip install -r requirements.txt

---

### Port Already in Use

If port 8000 is already being used, stop the existing application or run FastAPI on another available port.

---

### Authentication Error

Check:

- Login credentials.
- JWT token.
- Authorization header.
- Token expiration.
- SECRET_KEY configuration.

---

## 17. Project Startup Checklist

Before running the application:

[ ] Project source code available

[ ] Virtual environment created

[ ] Virtual environment activated

[ ] Dependencies installed

[ ] PostgreSQL installed and running

[ ] project_management database created

[ ] Database configuration verified

[ ] Environment variables configured

[ ] FastAPI application started

[ ] Swagger opened

[ ] User registered

[ ] Login tested

[ ] Protected API tested

---

## 18. Streamlit Integration

Once the backend is running, Streamlit can consume the APIs.

Flow:

Streamlit UI
    ↓
HTTP Request
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
Response
    ↓
Streamlit UI

The Streamlit application should communicate with Project Hub through APIs rather than directly connecting to the PostgreSQL database.

---

## 19. Future AI Assistant

The AI Assistant will be added after the core Project Hub backend is completed.

Expected flow:

User
  ↓
AI Assistant
  ↓
Understand Query
  ↓
Project Data / Knowledge
  ↓
Retrieve Relevant Information
  ↓
Generate Response
  ↓
User

The existing Knowledge, Task, Bug, Project and other modules provide the data foundation for the future AI Assistant.

---

## 20. Deployment Summary

The complete deployment flow is:

Source Code
    ↓
Virtual Environment
    ↓
Dependencies
    ↓
PostgreSQL
    ↓
Environment Configuration
    ↓
FastAPI
    ↓
Swagger
    ↓
API Testing
    ↓
Frontend / Streamlit Integration
    ↓
Production Deployment
