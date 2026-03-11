<<<<<<< HEAD
# 🚌 RutaMedellín 

## Historia de Usuario Implementada: HU-07

**"Como usuario sin experiencia en transporte público, quiero que la información se presente de forma clara y sencilla, para poder reducir el estrés y la confusión al viajar."**
---

## ¿Qué hace esta historia de usuario?
La HU-07 se enfoca en la **experiencia del usuario primerizo**. Implementa tres escenarios clave:

**Escenario 1 — Presentación clara de la ruta:**
Cuando el usuario selecciona una ruta, el sistema la muestra en formato paso a paso, lineal y sin ambigüedad. Cada paso es numerado y fácil de seguir.

**Escenario 2 — Instrucciones sin conocimiento previo:**
Las instrucciones no asumen que el usuario conoce la ciudad. Cada paso indica exactamente qué hacer: por dónde salir de la universidad, cómo identificar la parada, cómo abordar el bus y dónde bajarse.

**Escenario 3 — Guía integrada para usuarios nuevos (MVP):**
En la página de búsqueda se muestra un mensaje de ayuda estático que explica cómo usar el sistema, junto con texto placeholder en el campo de búsqueda y ejemplos de destinos para orientar al usuario desde el primer momento.

---

## Criterios de Aceptación Cubiertos

| Escenario | Criterio                                                  | Estado  |
|-----------|-----------------------------------------------------------|---------|
| 1         | Ruta presentada en formato lineal paso a paso             | ✅      |
| 2         | Instrucciones sin asumir conocimiento de la ciudad        | ✅      |
| 3         | Placeholder y mensaje de ayuda en la pantalla de búsqueda | ✅      |

---

## ¿Cómo correr el proyecto? (Paso a paso)
### Requisitos previos
- Python 3.x instalado
- Git instalado

### 1. Clonar el repositorio y cambiar a esta rama
git clone https://github.com/SamuelCV12/Proyecto_RutasEAFIT.git
cd Proyecto_RutasEAFIT
git checkout AnaSofiaAngaritaBarrios

### 2. Instalar Django
pip install django

### 3. Aplicar las migraciones (crear la base de datos)
python manage.py migrate

### 4. Poblar la base de datos con rutas de prueba
python manage.py poblar_rutas

### 5. Correr el servidor
python manage.py runserver

### 6. Abrir en el navegador
Ir a: http://127.0.0.1:8000/rutas/buscar/

---

## ¿Cómo usar la aplicación?
1. Escribe un destino en el campo (por ejemplo: Hospital, Centro, Poblado, Laureles, Aeropuerto).
2. Haz clic en **Buscar rutas**.
3. Verás las rutas disponibles listadas con el tiempo estimado.
4. Haz clic en cualquier ruta para ver el detalle paso a paso de cómo llegar.

---

## Rutas de prueba disponibles

| Ruta            | Destino                    | Tiempo estimado |
|-----------------|----------------------------|-----------------|
| Ruta Hospital   | Hospital Pablo Tobón Uribe | 20 min          |
| Ruta Centro     | Centro de Medellín         | 35 min          |
| Ruta Poblado    | El Poblado                 | 15 min          |
| Ruta Laureles   | Laureles                   | 25 min          |
| Ruta Aeropuerto | Aeropuerto Olaya Herrera   | 40 min          |

---

## Tecnologías utilizadas

- **Django** — Framework web de Python (backend)
- **SQLite** — Base de datos local (entorno de desarrollo)
- **Bootstrap 5** — Estilos y componentes de UI
- **HTML / CSS** — Templates y diseño visual

---

*Desarrollado por Ana Sofia Angarita Barrios — Proyecto Integrador 1, EAFIT 2026-1*
=======
# Acceptance Criteria (Gherkin)

## US-04: Combined Bus Route Guidance

**As a** beginner user,  
**I want** the application to tell me how to combine specific bus routes  
**So that** I can complete my trip correctly without making mistakes.

---

**Scenario 1: Suggesting combined routes with clear instructions**

**Given** I am planning a trip that requires multiple buses to reach my destination  
**When** the system calculates the optimal path  
**Then** it must suggest alternative route options  
**And** each option must include clear instructions on how to combine the different bus routes.

**Scenario 2: Displaying transfer details and connections** 

**Given** the system has suggested a route that includes combinations  
**When** I view the specific route details  
**Then** the application must clearly indicate the transfer stops  
**And** it must show the departure times for each segment  
**And** it must provide specific instructions on how to connect between the different routes.

**Scenario 3: Handling incompatible schedules**

**Given** I am following a combined route option  
**When** a connection cannot be made due to schedule changes or delays  
**Then** the system must provide a clear warning message  
**And** it must automatically suggest viable alternatives to complete the trip.

---

# 🚀 Execution Guide: User Story 04

## 📋 Prerequisites
* **Docker** and **Docker-Compose** must be installed.
* Access to the project's Git repository.

---

## 🛠️ Step 1: Synchronization and Deployment

Run the following commands in your terminal to ensure you have the latest version and active services:

```bash
# 1. Fetch the latest code version
git pull

# 2. Spin up containers and rebuild images
docker-compose up -d --build

# 3. Apply pending database changes
docker-compose exec web python manage.py migrate

4. Restart and Final Access
Once the database is ready (migrated), restart the service to ensure all Python configurations are loaded correctly and access the interface.

# 5. Restart the web container to refresh processes
docker-compose restart web

# 6. Verify that the server is running without errors
docker-compose logs --tail=20 web
>>>>>>> origin/MariaLauraTafurGomez
