<div align="center">
  <h1>🚌 RutasEAFIT - Route Finder</h1>
  <p><em>Finding the most optimal public transport routes for the EAFIT community and Medellín citizens.</em></p>
  
  ![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=for-the-badge&logo=python&logoColor=white)
  ![Django](https://img.shields.io/badge/Django-4.2-092E20?style=for-the-badge&logo=django&logoColor=white)
  ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-316192?style=for-the-badge&logo=postgresql&logoColor=white)
  ![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)
</div>

---

## 📖 About the Project

**RutasEAFIT** is a web application designed to simplify urban mobility. By leveraging a containerized architecture and an interactive frontend, it helps users navigate Medellín's complex transit system with ease.

### ✨ Key Features
* **Smart Trip Filtering:** Sort available routes by *fastest*, *direct*, or *cheapest* options.
* **Interactive Mapping:** Visualize your entire journey with step-by-step navigation powered by Leaflet.js.
* **Containerized Environment:** Zero-headache local setup using Docker and Docker Compose.

---

## 🛠️ Tech Stack

* **Backend:** Python 3.10, Django 4.2
* **Database:** PostgreSQL 15
* **Frontend:** HTML5, CSS3, Bootstrap 5, Leaflet.js
* **Infrastructure:** Docker & Docker Compose

---

## 🚀 Getting Started

This project is fully containerized. You do not need to manually install Python or PostgreSQL on your host machine. The Docker build process will automatically handle the environment setup and install all dependencies from `requirements.txt`.

### Prerequisites

Ensure you have the following tools installed on your local machine before executing the program:
* [Git](https://git-scm.com/)
* [Docker](https://www.docker.com/get-started)
* [Docker Compose](https://docs.docker.com/compose/install/)

### Installation & Execution

**1. Clone the repository:**
```bash
git clone [https://github.com/SamuelCV12/Proyecto_RutasEAFIT.git](https://github.com/SamuelCV12/Proyecto_RutasEAFIT.git)
cd Proyecto_RutasEAFIT
```

**2. Configure Environment Variables:**
Before starting the containers, you must set up your local environment variables (such as the Maps API Key). Copy the provided example file:
```bash
cp .env.example .env
```

Make sure to open the new .env file and insert your specific MAPS_API_KEY before proceeding.
**3. Build and start the containers: This command will fetch the required images, build the Python environment (installing requirements.txt), and start the web and database services in detached mode (-d parameter):**
```bash
docker-compose up -d --build
```

**4. Apply database migrations: Set up the PostgreSQL database schema to match the Django models:**
```bash
docker-compose exec web python manage.py migrate
```

**5. Load Initial Data (Seeding):**
Populate the database with the verified pre-configured routes and locations (Parque San Antonio, EAFIT, Laureles, etc.):
```bash
docker-compose exec web python manage.py loaddata data_inicial.json
```

**6. Create a superuser (Optional, for admin panel access):**
```bash
docker-compose exec web python manage.py createsuperuser
```

---

## 💻 Usage

Once the containers are up and running, you can access the application through your web browser:

* **Main Application:** Navigate to [http://localhost:8000/inicio/](http://localhost:8000/inicio/)
* **Admin Dashboard:** Navigate to [http://localhost:8000/admin/](http://localhost:8000/admin/)

### Stopping the Application
To gracefully stop the running containers without losing your persistent database data, run:
```bash
docker-compose down
```

---

## 👥 Development Team

* **Ana Angarita** - *Programmer*
* **Oriana Vayoles** - *Scrum Master / Analyst*
* **Samuel Correa** - *Tester*
* **Maria Laura Tafur** - *Architect*
