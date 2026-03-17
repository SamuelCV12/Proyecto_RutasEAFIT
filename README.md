# RutasEAFIT - Route Finder 🚌

RutasEAFIT is a web application designed to help the EAFIT University community and the citizens of Medellín find the most optimal public transport routes. The system features trip filtering (fastest, direct, or cheapest) and an interactive map with step-by-step navigation.

## 🛠️ Tech Stack
* **Backend:** Python 3.10, Django 4.2
* **Database:** PostgreSQL 15
* **Frontend:** HTML5, CSS3, Bootstrap 5, Leaflet.js (Interactive Maps)
* **Infrastructure:** Docker & Docker Compose

## 📋 Prerequisites

Ensure you have the following tools installed on your local machine before executing the program:
* [Git](https://git-scm.com/)
* [Docker](https://www.docker.com/get-started)
* [Docker Compose](https://docs.docker.com/compose/install/)

## 🚀 How to Run the Program

This project is fully containerized. You do not need to manually install Python or PostgreSQL on your host machine. The Docker build process will automatically install all the necessary libraries listed in the `requirements.txt` file.

**1. Clone the repository:**
\`\`\`bash
git clone https://github.com/SamuelCV12/Proyecto_RutasEAFIT.git
cd Proyecto_RutasEAFIT
\`\`\`

**2. Build and start the containers:**
This command will fetch the required images, build the Python environment (installing `requirements.txt`), and start the web and database services in detached mode (`-d` parameter):
\`\`\`bash
docker-compose up -d --build
\`\`\`

**3. Apply database migrations:**
Set up the PostgreSQL database schema to match the Django models:
\`\`\`bash
docker-compose exec web python manage.py migrate
\`\`\`

**4. Create a superuser (Optional, for admin panel access):**
\`\`\`bash
docker-compose exec web python manage.py createsuperuser
\`\`\`

**5. Access the application:**
* Main Application: Open your browser and navigate to `http://localhost:8000/inicio/`
* Admin Dashboard: Open your browser and navigate to `http://localhost:8000/admin/`

## 🛑 Stopping the Application
To gracefully stop the running containers without losing your persistent database data, run:
\`\`\`bash
docker-compose down
\`\`\`

## 👥 Development Team
* **Ana Angarita** - *Programmer*
* **Oriana Vayoles** - *Scrum Master / Analyst*
* **Samuel Correa** - *Tester*
* **Maria Laura Tafur** - *Architect*
