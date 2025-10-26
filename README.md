# GetEmpStatus API

A Django REST Framework (DRF) project that provides an API endpoint to retrieve employee status based on their national number.
It validates input, checks user status, computes salary averages, bonuses, deductions, and determines overall employment status.

## 🚀 Features

- RESTful API built with Django REST Framework
- Validates national numbers and user status
- Computes bonuses, deductions, and final salary status
- Returns a color-coded status (Green, Orange, Red)
- Auto-generated Swagger and Redoc documentation

## 🧩 Project Structure
```
GetEmpStatus/
├── api/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── utils.py
│   └── ...
├── GetEmpStatus/
│   ├── settings.py
│   ├── urls.py
│   └── ...
└── manage.py
```

## 🧾 Requirements

- Python 3.12+
- pipenv
- Git

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/kareemk11/Empmanager.git
cd Empmanager
```

### 2️⃣ Install pipenv (if not already installed)
```bash
pip install pipenv
```

### 3️⃣ Install dependencies
```bash
pipenv install
```

This automatically creates a virtual environment and installs all required packages.

### 4️⃣ Activate the environment
```bash
pipenv shell
```

### 5️⃣ Apply Migrations
```bash
python manage.py migrate
```

### 6️⃣ Run the Server
```bash
python manage.py runserver
```

## 🧠 API Overview

### Endpoint
```
POST /api/GetEmpStatus/
```

### Request Body
```json
{
  "NationalNumber": "1234567890"
}
```

### Example Response
```json
{
  "user": {
    "national_number": "1234567890",
    "full_name": "John Doe",
    "is_active": true
  },
  "average_salary": 6500.0,
  "status": "Good Standing",
  "status_color": "green"
}
```

### Error Responses

| HTTP Code | Description |
|-----------|-------------|
| 400 | Invalid or missing national number |
| 404 | User not found |
| 403 | User is inactive |
| 500 | Internal server error |

## 🧾 Database Schema

### User

| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary key |
| national_number | CharField | Unique national ID |
| full_name | CharField | Employee full name |
| is_active | BooleanField | Whether user is active |

### Salary

| Field | Type | Description |
|-------|------|-------------|
| user | ForeignKey | Linked user |
| month | IntegerField | Month of salary |
| year | IntegerField | Year of salary |
| amount | DecimalField | Monthly salary amount |
| bonus | DecimalField | Optional bonus |
| deduction | DecimalField | Optional deduction |

## 📘 API Documentation

### Swagger UI

Once the server is running, visit:

👉 http://127.0.0.1:8000/swagger/

### Redoc UI

👉 http://127.0.0.1:8000/redoc/

## 🧰 Tech Stack

- **Backend:** Django 5+, Django REST Framework
- **Database:** SQLite (default, can switch to PostgreSQL)
- **Documentation:** drf-yasg / drf-spectacular
- **Environment:** pipenv

## 📄 License

This project is provided for educational and assessment purposes.
