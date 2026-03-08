# EAFITrans — Medellín Bus Guide MVP

**Historia de Usuario:** Como usuario no familiarizado con el transporte público, quiero ver las rutas explicadas paso a paso.

## 🚀 Setup rápido (Quick Setup)

### 1. Instalar dependencias
```bash
pip install django
```

### 2. Aplicar migraciones
```bash
cd eafit_transport
python manage.py migrate
```

### 3. Cargar datos de ejemplo (rutas reales)
```bash
python manage.py seed_routes
```

### 4. Crear superusuario (opcional, para el admin)
```bash
python manage.py createsuperuser
```

### 5. Iniciar el servidor
```bash
python manage.py runserver
```

Visita: **http://localhost:8000**

---

## 📁 Estructura del proyecto

```
eafit_transport/
├── manage.py
├── eafitrans/
│   ├── settings.py          # Configuración Django
│   ├── urls.py              # URLs raíz
│   └── wsgi.py
├── routes/
│   ├── models.py            # Route, Stop, StepInstruction
│   ├── views.py             # route_list, route_guide
│   ├── admin.py             # Panel de administración
│   ├── urls.py
│   └── management/
│       └── commands/
│           └── seed_routes.py   # Datos demo
├── templates/
│   ├── base.html            # Layout base (navbar, footer, CSS)
│   └── routes/
│       ├── route_list.html  # Página de selección de ruta
│       └── route_guide.html # ⭐ Guía paso a paso
└── static/
    └── (CSS/JS adicional)
```

---

## 🎯 Criterios de aceptación cubiertos

| Escenario | Implementación |
|-----------|----------------|
| ✅ Escenario 1: Guía paso a paso | `route_guide.html` muestra todos los pasos desde origen hasta destino con `StepInstruction` ordenados |
| ✅ Escenario 2: Instrucciones detalladas | Cada paso incluye: dónde esperar, qué bus, cómo pagar, cuándo bajarse, transferencias |
| ✅ Escenario 3: Formato fácil de leer | Lista numerada con iconos por tipo de paso, lenguaje simple, sin jerga técnica |

---

## 🌐 Bilingüismo (EN/ES)

- Switch de idioma en la navbar (EN / ES)
- Todos los textos de las instrucciones en ambos idiomas
- Persiste en la sesión del usuario
- URL param: `?lang=en` o `?lang=es`

---

## 🔧 Agregar nuevas rutas

### Desde el admin (recomendado)
```
http://localhost:8000/admin/
```
1. Crear una `Route`
2. Agregar `Stop`s con orden y offset de tiempo
3. Agregar `StepInstruction`s con texto en EN y ES

### Tipos de pasos disponibles
- `walk` — Caminar
- `wait` — Esperar
- `board` — Subir al bus
- `ride` — Viajar
- `transfer` — Transbordo
- `exit` — Bajarse
- `arrive` — Llegada

---

## 🎨 Stack tecnológico

- **Backend:** Django 4+
- **Frontend:** Bootstrap 5.3 + Bootstrap Icons
- **Fonts:** Sora (títulos) + DM Sans (cuerpo) — Google Fonts
- **DB:** SQLite (dev) → cambiar a PostgreSQL en producción

---

## 📱 Responsive

Diseñado mobile-first. Funciona en celular, tablet y desktop.
