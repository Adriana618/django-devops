# Secure Document Analyzer

Secure Document Analyzer is a document analysis system designed for secure and asynchronous processing. It utilizes **Django REST Framework** for the backend, **PostgreSQL** as the database, **Redis** and **Celery** for asynchronous tasks, **AWS S3** for secure storage, and **AWS Textract** for text extraction. The frontend is built with **React + TypeScript**.

---

## 📌 Table of Contents

1. [Project Overview](#project-overview)
2. [Requirements & Implemented Features](#requirements--implemented-features)
3. [Project Structure](#project-structure)
4. [Environment Variables](#environment-variables)
5. [Setup & Execution](#setup--execution)
6. [API Endpoints](#api-endpoints)
7. [How Requirements Were Met](#how-requirements-were-met)
8. [Running Tests](#running-tests)
9. [Final Notes](#final-notes)

---

## 🔍 Project Overview

This system allows users to:

✅ **Register** and **authenticate** using JWT.  
✅ **Upload** PDF (or image) documents to **AWS S3** with encryption at rest.  
✅ **Process** the document content using **AWS Textract** asynchronously (**Celery**).  
✅ **View** processing status and extracted text in a **React + TypeScript** interface.  

It focuses on **security** (S3 encryption, validation, logging), **asynchronous processing** (Celery), and **deployment ease** (Docker Compose).

---

## 🎯 Requirements & Implemented Features

### ✅ **Core Requirements**

1. **JWT Authentication**  
2. **Secure document upload** with encryption at rest (S3)  
3. **Asynchronous processing** with Celery  
4. **AWS Textract integration**  
5. **Security measures** (input validation, logs, API key management)  
6. **Frontend** for file upload and result visualization  

### 🚀 **Implemented Extras**

1. **Test Coverage** (pytest + pytest-cov)  
2. **OWASP Security** (secure headers, DRF throttling, etc.)  
3. **Audit Logging** using logs and/or django-auditlog  
4. **CI/CD with GitHub Actions** (lint + tests)  
5. **Full containerization with Docker Compose**  

---

## 📁 Project Structure

```bash
my-project/  
├── docker-compose.yml  
├── Makefile (optional)  
├── secure_doc_analyzer/            # Backend (Django)  
│   ├── Dockerfile  
│   ├── manage.py  
│   ├── requirements.txt  
│   ├── secure_doc_analyzer/  
│   │   ├── settings/  
│   │   │   ├── base.py  
│   │   │   ├── dev.py  
│   │   │   ├── prod.py  
│   │   │   └── ...  
│   │   ├── urls.py  
│   │   └── wsgi.py  
│   ├── documents/  
│   ├── accounts/  
│   ├── ...  
│   └── .env                        # env.example
└── secure-doc-frontend/            # Frontend (React + TypeScript)  
    ├── Dockerfile  
    ├── .env.local                  # env.local.example
    ├── package.json  
    ├── tsconfig.json  
    ├── public/  
    └── src/  
        ├── api/  
        ├── components/  
        └── pages/  
        └── ...

---
```

## 🌍 Environment Variables

A `.env.example` file is provided as a reference:

```bash
.env.example

###################

Database Config

###################
DATABASE_NAME=secure_analyzer
DATABASE_USER=myuser
DATABASE_PASSWORD=mypassword
DATABASE_HOST=postgres
DATABASE_PORT=5432

##########################

AWS / S3 Configuration

##########################
AWS_ACCESS_KEY_ID=xxx
AWS_SECRET_ACCESS_KEY=yyy
AWS_S3_BUCKET=my-secure-bucket
AWS_REGION=us-east-1

####################

Celery / Redis

####################
CELERY_BROKER_URL=redis://redis:6379/0

##################

Django Settings

##################
SECRET_KEY=myrandomsecretkey
DJANGO_SETTINGS_MODULE=secure_doc_analyzer.settings.dev
DEBUG=True
```

A `.env.local.example` file is provided as a reference:

```bash
.env.local.example

###################

React API_URL

###################
REACT_APP_API_BASE_URL=http://localhost:8000
```

Copy this file as `.env` (remove `.example`) and adjust the values to match your environment.  

---

## 🏗️ Setup & Execution

### 🔧 **Start with Docker Compose**

1. Copy `.env.example` to `.env` and edit it with your values.
2. Copy `.env.local.example` to `.env.local` and edit it with your values.
3. From the project root, run:
```bash
docker-compose build
docker-compose up -d
```

4. Verify the running containers:
```bash
docker-compose ps
```

5. Apply migrations and create a superuser:
```bash
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
```

6. **Frontend**:  
   - If running in dev mode, access `http://localhost:3000`.  
   - If running with Nginx in production, use `http://localhost:80`.

---

## 📡 API Endpoints

| **Endpoint**               | **Method**  | **Description**                              | **Protected** |
|----------------------------|------------|----------------------------------------------|---------------|
| `/api/accounts/signup/`    | `POST`     | Create a new user (username, password, email) | No (public)  |
| `/api/token/`              | `POST`     | Obtain JWT (access, refresh)                  | No (public)  |
| `/api/documents/upload/`   | `POST`     | Upload a document (`file` in multipart form) | Yes (JWT)    |
| `/api/documents/`          | `GET`      | List user-uploaded documents                 | Yes (JWT)    |

- **Authentication**:  
  - Requires **Bearer Token** in the header:  
    ```
    Authorization: Bearer <ACCESS_TOKEN>
    ```
- **Document Upload**:  
  - Only `.pdf`, `.jpg`, `.png`, etc. are allowed (configurable).  
  - The file must be sent as **multipart/form-data** with `file`.

---

## 🔒 How Requirements Were Met

### **1. Security**
✅ **Encryption at rest**: Documents are stored in S3 with `ServerSideEncryption=AES256`.  
✅ **API key management**: Sensitive variables (AWS keys, SECRET_KEY) are stored in `.env`, not in the repository.  
✅ **Audit logging**: Key actions (document uploads, etc.) are logged.  
✅ **Input validation**: File size and extensions are restricted, DRF serializers are used.  
✅ **OWASP Security**: Secure headers (`SECURE_SSL_REDIRECT`, `X_FRAME_OPTIONS`, etc. in `prod.py`), DRF throttling, etc.

### **2. Document Processing**
✅ **AWS Textract**: Extracts text asynchronously using Celery.  
✅ **Extracted text is stored in the database** in `extracted_text`.

### **3. Asynchronous Processing with Celery**
✅ **Celery Worker**: Downloads the file from S3, processes it, and updates the document status to `DONE` or `ERROR`.  
✅ **Redis** is used as the broker (SQS, RabbitMQ, etc. can be configured).

### **4. Frontend**
✅ **React + TypeScript**: File upload component, document status page, displays extracted text when `DONE`.  
✅ **Material UI** for a clean and modern design.

### **5. Additional Implementations**
✅ **Test Coverage**: `pytest --cov` covers models, views, and tasks.  
✅ **OWASP Security**: Secure Django settings for production.  
✅ **Audit Logging**: Using logs and/or [django-auditlog](https://github.com/jazzband/django-auditlog).  
✅ **CI/CD**: GitHub Actions workflow runs linting, tests, and coverage on each push.

---

## 🧪 Running Tests

Run **backend tests** with Pytest:
```bash
cd secure_doc_analyzer
pytest –cov=. –cov-report=term-missing
```

---

## 📌 Final Notes

- **For production**, enable `DEBUG=False`, enforce HTTPS, and use a managed database (e.g., AWS RDS for PostgreSQL).  
- **For domain setup**, consider using Nginx as a reverse proxy or AWS CloudFront for static hosting.  
- **Support**: For issues, check repository issues or contact the team.
