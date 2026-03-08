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
