# 🚀 Guía de Ejecución: Historia de Usuario 4



---

## 📋 Requisitos Previos
* Tener instalado **Docker** y **Docker-Compose**.
* Contar con acceso al repositorio Git del proyecto.

---

## 🛠️ Paso 1: Sincronización y Despliegue

Ejecute los siguientes comandos en su terminal para asegurar que tiene la última versión y los servicios activos:

```bash
# 1. Obtener la última versión del código
git pull

# 2. Levantar los contenedores y reconstruir imágenes
docker-compose up -d --build

# 3. Aplicar cambios pendientes en la base de datos
docker-compose exec web python manage.py migrate

#4. Reinicio y Acceso Final
Una vez que la base de datos está lista (migrada), reinicie el servicio para asegurar que todas las configuraciones de Python se carguen correctamente y acceda a la interfaz.

```bash
# 5. Reiniciar el contenedor de la web para refrescar procesos
docker-compose restart web

# 6. Verificar que el servidor esté corriendo sin errores
docker-compose logs --tail=20 web

