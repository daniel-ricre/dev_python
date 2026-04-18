# User Management REST API

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

A production-ready REST API for user management built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**. Deployed on **Render** with 24/7 uptime monitoring via **UptimeRobot**.

## 🚀 Live Demo

👉 **[Live API Documentation](https://dev-python-5phk.onrender.com/docs)**

> _Note: The first request may take a few seconds due to Render's free tier cold start._

## ✨ Features

- ✅ Full CRUD operations for user management
- ✅ PostgreSQL database with SQLAlchemy ORM
- ✅ Interactive Swagger UI for testing
- ✅ Modular code structure (routers, models, schemas, services)
- ✅ Input validation with Pydantic schemas
- ✅ Proper error handling with HTTP status codes
- ✅ Secure credential management with environment variables
- ✅ Deployed on Render with 24/7 uptime monitoring

## 🛠️ Tech Stack

| Category   | Technology       |
| ---------- | ---------------- |
| Framework  | FastAPI (Python) |
| ORM        | SQLAlchemy       |
| Database   | PostgreSQL       |
| Deployment | Render           |
| Monitoring | UptimeRobot      |
| Validation | Pydantic         |
| Server     | Uvicorn          |

## 📡 API Endpoints

| Method | Endpoint                        | Description             |
| ------ | ------------------------------- | ----------------------- |
| POST   | `/users/create`                 | Create a new user       |
| GET    | `/users/all`                    | Get all users           |
| GET    | `/users/by_id/{id}`             | Get user by ID          |
| GET    | `/users/by_username/{username}` | Get user by username    |
| GET    | `/users/by_email/{email}`       | Get user by email       |
| GET    | `/users/by_actives/{active}`    | Filter by active status |
| PUT    | `/users/update/{id}`            | Update user             |
| DELETE | `/users/delete/{id}`            | Delete user             |
| GET    | `/`                             | Health check            |

## 👨‍💻 About Me

I'm **Daniel Rivero Crespo**, a Computer Science Engineering student at the **University of Informatics Sciences (UCI)** in Cuba. I specialize in backend development with Python, FastAPI, and PostgreSQL.

- 💼 **Fiverr**: [danielrivero574](https://www.fiverr.com/danielrivero574)

---

⭐**Need a custom REST API?** Hire me on Fiverr!
