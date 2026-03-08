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
