# 📘 Moxie Medspa API
A Django REST Framework-based API for managing medspas, their services, and customer appointments.

## 🚀 Quick Start with Docker

### 1️⃣ Clone the Repository

```
git clone git@github.com:leonardorhojas/MoxiProject.git
cd MoxiProject
```

### 2️⃣ Start the Application

Simply run:

```
docker-compose up --build
```

This will:

- Start PostgreSQL database
- Apply database migrations automatically
- Start the Django application at 📌 http://localhost:8000

🎉 Your API is now running! 🎉

# 🐳 Docker Commands

If needed, you can run the following:

## Check Running Containers

```
docker ps
```

## Apply Migrations (if needed)

```
docker-compose exec moxie_django python manage.py migrate
```

## Create a Superuser

```
docker-compose exec moxie_django python manage.py createsuperuser
```

# 🛠 API Documentation

* Swagger UI: 📌 http://localhost:8000/swagger/
* ReDoc UI: 📌 http://localhost:8000/redoc/
* OpenAPI JSON: 📌 http://localhost:8000/swagger.json


## 📡 API Endpoints

### Medspa Endpoints

Method | Endpoint | description 
--- |----------|-------------
GET | /api/medspa/	      | List all medspas
POST | /api/medspa/	      | Create a new medspa
GET | /api/medspa/{id}/		      | Get details of a medspa
GET | /api/medspa/{id}/services/      | List services of a medspa

-------

### Service Endpoints

Method | Endpoint           | description 
--- |--------------------|-------------
GET | /api/service/      | List all services
POST | /api/service/      | Create a new service
GET | /api/service/{id}/ | Get details of a service

-------

## Appointment Endpoints

Method | Endpoint           | description 
--- |--------------------|-------------
GET | /api/appointment/      | List all appointments
POST | /api/appointment/    | Create an appointment
GET | /api/appointment/{id}/	 | Get details of an appointment
PATCH | /api/appointment/{id}/ | Update appointment status 
GET | /api/appointment/filter_by_status/ | Filter appointments by status
GET | /api/appointment/filter_by_date/ | Filter appointments by start date

-------

# 🧪 Running Tests

Run tests inside the Docker container:

```
docker-compose exec moxie_django python manage.py test
```


# 📩 Contact
For support, contact 📧 leonardorhojas@gmail.com










