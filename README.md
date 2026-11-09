# FERRUM

Sistema de gestión inteligente para ferreterías: inventario, ventas, analítica predictiva, alertas automáticas y tienda pública para clientes. Construido con Flask, PostgreSQL y JavaScript vanilla.
Intelligent management system for hardware stores: inventory, sales, predictive analytics, automatic alerts and a public customer store. Built with Flask, PostgreSQL and vanilla JavaScript.

[Español](#español) | [English](#english)

---

## Español

### Contenido

- [Descripción general](#descripción-general)
- [Características principales](#características-principales)
- [Tecnologías utilizadas](#tecnologías-utilizadas)
- [Estructura del repositorio](#estructura-del-repositorio)
- [Requisitos](#requisitos)
- [Instalación y ejecución local](#instalación-y-ejecución-local)
- [Variables de entorno](#variables-de-entorno)
- [Cuenta de administrador](#cuenta-de-administrador)
- [Uso](#uso)
- [Despliegue en Railway](#despliegue-en-railway)
- [Notas técnicas](#notas-técnicas)
- [Licencia](#licencia)

### Descripción general

FERRUM es una aplicación web completa para gestionar el día a día de una ferretería. Incluye:

- Un panel administrativo protegido por sesión.
- Un sistema de inventario con alertas automáticas de stock crítico y bajo.
- Un módulo de ventas con historial y estadísticas.
- Un panel de analítica con gráficos y predicciones de agotamiento de stock, basadas en el promedio ponderado de los últimos 30 días.
- Una tienda pública con carrito de compras, para que los clientes consulten el catálogo y realicen pedidos sin necesidad de iniciar sesión.

El sistema utiliza PostgreSQL como base de datos y se inicializa automáticamente con categorías, productos de ejemplo y 60 días de historial de ventas sintético, de modo que la analítica y las predicciones tengan datos desde el primer arranque.

### Características principales

- **Autenticación por sesión:** panel administrativo protegido, además de registro e inicio de sesión para clientes de la tienda.
- **Gestión de inventario:** alta, edición, baja lógica y reabastecimiento de productos, con categorías, proveedor, unidad, márgenes y estados de stock (crítico, bajo, normal).
- **Punto de venta:** búsqueda con autocompletado, carrito, descuentos, métodos de pago y cálculo automático de ganancia.
- **Historial de ventas:** filtros por fecha, detalle por transacción y estadísticas de hoy, del mes y acumuladas.
- **Analítica:** gráficos de ventas diarias, ventas por día de la semana, ingresos por categoría, métodos de pago y top 10 de productos.
- **Predicción de agotamiento:** cálculo por producto con promedio ponderado de los últimos 30 días, con fecha estimada y nivel de confianza.
- **Recomendaciones de reabastecimiento:** cantidad sugerida por producto, costo estimado y ganancia potencial, ordenadas por urgencia.
- **Alertas automáticas:** stock crítico, stock bajo, agotamiento próximo y oportunidades de ganancia por alto margen.
- **Tienda pública:** catálogo con búsqueda, filtros por categoría, ordenamiento, carrito persistente y checkout con método de pago.
- **Zona horaria de Bogotá:** las ventas se registran en hora local de Colombia.
- **Listo para múltiples workers:** inicialización de la base de datos tolerante a fallos, con reintento diferido.

### Tecnologías utilizadas

| Capa           | Tecnología                         |
|----------------|------------------------------------|
| Backend        | Python 3, Flask 3, Gunicorn        |
| Base de datos  | PostgreSQL (psycopg2)              |
| Sesión         | Flask-Session con cookies firmadas |
| Frontend       | HTML5, CSS3, JavaScript vanilla    |
| Gráficos       | Chart.js 4                         |
| Tipografía     | DM Sans                            |
| Despliegue     | Railway (Nixpacks)                 |

### Estructura del repositorio

```text
.
├── app.py                      # Punto de entrada, registro de blueprints y rutas
├── database.py                 # Conexión, esquema y datos de ejemplo
├── requirements.txt            # Dependencias de Python
├── railway.toml                # Configuración de despliegue en Railway
├── routes/
│   ├── auth.py                 # Login, registro, logout y sesión
│   ├── inventory.py            # CRUD de productos y categorías
│   ├── sales.py                # Registro y consulta de ventas
│   ├── analytics.py            # Dashboards, predicciones y recomendaciones
│   └── alerts.py               # Generación de alertas de inventario
├── templates/
│   ├── base.html               # Layout común del panel administrativo
│   ├── index.html              # Dashboard principal
│   ├── inventario.html         # Gestión de inventario
│   ├── ventas.html             # Punto de venta e historial
│   ├── analytics.html          # Analítica y predicciones
│   ├── alertas.html            # Panel de alertas
│   └── carrito.html            # Tienda pública con carrito
└── static/
    └── css/
        └── main.css            # Estilos del panel administrativo
```

### Requisitos

- Python 3.9 o superior
- PostgreSQL 12 o superior
- pip
- Navegador moderno

### Instalación y ejecución local

1. Clona el repositorio:

   ```bash
   git clone https://github.com/tu-usuario/ferreteria.git
   cd ferreteria
   ```

2. Crea un entorno virtual e instala las dependencias:

   ```bash
   python -m venv venv
   venv\Scripts\activate           # En Linux/macOS: source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Crea una base de datos PostgreSQL y configura la variable `DATABASE_URL`:

   En Windows (PowerShell):

   ```powershell
   $env:DATABASE_URL = "postgresql://usuario:password@localhost:5432/ferreteria"
   ```

   En Linux/macOS:

   ```bash
   export DATABASE_URL="postgresql://usuario:password@localhost:5432/ferreteria"
   ```

4. Inicia el servidor:

   ```bash
   python app.py
   ```

5. Abre `http://localhost:5000` en el navegador.

La base de datos se inicializa automáticamente con categorías, productos y 60 días de historial de ventas sintético.

### Variables de entorno

| Variable       | Descripción                                      | Valor por defecto            |
|----------------|--------------------------------------------------|------------------------------|
| `DATABASE_URL` | Cadena de conexión a PostgreSQL (obligatoria)    | Ninguno                      |
| `SECRET_KEY`   | Clave para firmar las sesiones de Flask          | `ferreteria-2024-secret-key` |
| `ADMIN_USER`   | Usuario del administrador maestro                | `admin`                      |
| `ADMIN_PASS`   | Contraseña del administrador maestro             | `ferreteria123`              |
| `PORT`         | Puerto de escucha del servidor                   | `5000`                       |

### Cuenta de administrador

La cuenta de administrador se define en `routes/auth.py`, al inicio del módulo:

```python
ADMIN_USER = os.environ.get('ADMIN_USER', 'admin')
ADMIN_PASS = os.environ.get('ADMIN_PASS', 'ferreteria123')
```

Credenciales por defecto:

| Campo      | Valor           |
|------------|-----------------|
| Usuario    | `admin`         |
| Contraseña | `ferreteria123` |

Para cambiarlas, define las variables de entorno `ADMIN_USER` y `ADMIN_PASS` antes de arrancar la aplicación (por ejemplo, en el panel de Railway o en un archivo `.env` cargado por tu entorno). El código las lee al arrancar, por lo que no es necesario modificar el código fuente.

Además, cualquier usuario registrado en la base de datos puede ser promovido a administrador actualizando su columna `rol` a `'admin'` directamente en la tabla `usuarios`. El endpoint de registro siempre crea usuarios con rol `cliente`, por lo que la promoción debe hacerse manualmente por SQL.

> **Importante:** las credenciales por defecto están escritas como valor de respaldo dentro del repositorio. Si despliegas este proyecto en producción, sobrescribe `ADMIN_USER`, `ADMIN_PASS` y `SECRET_KEY` con valores seguros mediante variables de entorno.

### Uso

**Panel administrativo (requiere iniciar sesión):**

| Ruta          | Descripción                                          |
|---------------|------------------------------------------------------|
| `/dashboard`  | Panel general con métricas y gráficos                |
| `/inventario` | CRUD de productos, búsqueda, filtros y reabastecimiento |
| `/ventas`     | Punto de venta e historial de transacciones          |
| `/analytics`  | Analítica, predicciones y recomendaciones            |
| `/alertas`    | Alertas y oportunidades de inventario                |

**Tienda pública (sin iniciar sesión):**

| Ruta | Descripción                                |
|------|--------------------------------------------|
| `/`  | Catálogo con carrito de compras y checkout |

El flujo de compra desde la tienda pública también descuenta stock y registra la venta en el historial, por lo que aparece en la analítica como cualquier otra transacción.

### Despliegue en Railway

El repositorio incluye un `railway.toml` listo para usar con Gunicorn y Nixpacks. Solo necesitas:

1. Crear un proyecto en Railway y agregar un plugin de PostgreSQL.
2. Conectar el repositorio de GitHub.
3. Dejar que Railway inyecte `DATABASE_URL` automáticamente al desplegar.
4. Definir `SECRET_KEY`, `ADMIN_USER` y `ADMIN_PASS` como variables de entorno del servicio.

El comando de arranque configurado es:

```bash
gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

### Notas técnicas

- La base de datos se inicializa en el arranque y se reintenta de forma diferida en la primera petición si el plugin de PostgreSQL aún no estaba disponible al levantar el proceso.
- Las contraseñas de los usuarios registrados se almacenan con SHA-256. La cuenta maestra se valida por comparación directa contra las variables de entorno, sin pasar por la base de datos.
- Los datos de ejemplo se siembran solo si la tabla `productos` está vacía, por lo que un reinicio no duplica información.
- Las fechas de venta se registran con la zona horaria `America/Bogota`, para que el dashboard y los reportes diarios sean consistentes.
- La predicción de agotamiento usa un promedio ponderado en el que los días más recientes pesan más, y reporta un nivel de confianza según la cantidad de días con datos.

### Licencia

Este proyecto se distribuye bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.

---

## English

### Contents

- [Overview](#overview)
- [Key features](#key-features)
- [Tech stack](#tech-stack)
- [Repository structure](#repository-structure)
- [Requirements](#requirements)
- [Local installation and run](#local-installation-and-run)
- [Environment variables](#environment-variables)
- [Admin account](#admin-account)
- [Usage](#usage)
- [Railway deployment](#railway-deployment)
- [Technical notes](#technical-notes)
- [License](#license)

### Overview

FERRUM is a full-featured web application for the day-to-day management of a hardware store. It includes:

- A session-protected admin panel.
- An inventory system with automatic low and critical stock alerts.
- A sales module with history and statistics.
- An analytics dashboard with charts and stock-out predictions based on a weighted average of the last 30 days.
- A public store with a shopping cart, so customers can browse the catalog and place orders without logging in.

The system uses PostgreSQL as its database and seeds itself automatically with categories, sample products and 60 days of synthetic sales history, so analytics and predictions have data from the first launch.

### Key features

- **Session-based authentication:** protected admin panel, plus customer registration and login for the store.
- **Inventory management:** create, edit, soft-delete and restock products, with categories, supplier, unit, margins and stock states (critical, low, normal).
- **Point of sale:** autocomplete search, cart, discounts, payment methods and automatic profit calculation.
- **Sales history:** date filters, per-transaction detail, and statistics for today, the month and lifetime.
- **Analytics:** charts for daily sales, sales by weekday, revenue by category, payment methods and top 10 products.
- **Stock-out prediction:** per-product calculation using a weighted average of the last 30 days, with estimated date and confidence level.
- **Restock recommendations:** suggested quantity per product, estimated cost and potential profit, sorted by urgency.
- **Automatic alerts:** critical stock, low stock, upcoming stock-out and high-margin profit opportunities.
- **Public storefront:** catalog with search, category filters, sorting, persistent cart and checkout with payment method.
- **Bogotá timezone:** sales are recorded in Colombia local time.
- **Multi-worker ready:** failure-tolerant database initialization with lazy retry.

### Tech stack

| Layer      | Technology                         |
|------------|------------------------------------|
| Backend    | Python 3, Flask 3, Gunicorn        |
| Database   | PostgreSQL (psycopg2)              |
| Session    | Flask-Session with signed cookies  |
| Frontend   | HTML5, CSS3, vanilla JavaScript    |
| Charts     | Chart.js 4                         |
| Typography | DM Sans                            |
| Deployment | Railway (Nixpacks)                 |

### Repository structure

```text
.
├── app.py                      # Entry point, blueprint registration and routes
├── database.py                 # Connection, schema and seed data
├── requirements.txt            # Python dependencies
├── railway.toml                # Railway deployment configuration
├── routes/
│   ├── auth.py                 # Login, registration, logout and session
│   ├── inventory.py            # Product and category CRUD
│   ├── sales.py                # Sales registration and queries
│   ├── analytics.py            # Dashboards, predictions and recommendations
│   └── alerts.py               # Inventory alert generation
├── templates/
│   ├── base.html               # Shared admin panel layout
│   ├── index.html              # Main dashboard
│   ├── inventario.html         # Inventory management
│   ├── ventas.html             # Point of sale and history
│   ├── analytics.html          # Analytics and predictions
│   ├── alertas.html            # Alerts panel
│   └── carrito.html            # Public store with cart
└── static/
    └── css/
        └── main.css            # Admin panel styles
```

### Requirements

- Python 3.9 or higher
- PostgreSQL 12 or higher
- pip
- A modern browser

### Local installation and run

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/ferreteria.git
   cd ferreteria
   ```

2. Create a virtual environment and install dependencies:

   ```bash
   python -m venv venv
   venv\Scripts\activate           # On Linux/macOS: source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Create a PostgreSQL database and set the `DATABASE_URL` variable:

   On Windows (PowerShell):

   ```powershell
   $env:DATABASE_URL = "postgresql://user:password@localhost:5432/ferreteria"
   ```

   On Linux/macOS:

   ```bash
   export DATABASE_URL="postgresql://user:password@localhost:5432/ferreteria"
   ```

4. Start the server:

   ```bash
   python app.py
   ```

5. Open `http://localhost:5000` in your browser.

The database initializes itself with categories, products and 60 days of synthetic sales history.

### Environment variables

| Variable       | Description                                  | Default                      |
|----------------|----------------------------------------------|------------------------------|
| `DATABASE_URL` | PostgreSQL connection string (required)      | None                         |
| `SECRET_KEY`   | Key for signing Flask sessions               | `ferreteria-2024-secret-key` |
| `ADMIN_USER`   | Master admin username                        | `admin`                      |
| `ADMIN_PASS`   | Master admin password                        | `ferreteria123`              |
| `PORT`         | Server listen port                           | `5000`                       |

### Admin account

The admin account is defined in `routes/auth.py`, at the top of the module:

```python
ADMIN_USER = os.environ.get('ADMIN_USER', 'admin')
ADMIN_PASS = os.environ.get('ADMIN_PASS', 'ferreteria123')
```

Default credentials:

| Field    | Value           |
|----------|-----------------|
| Username | `admin`         |
| Password | `ferreteria123` |

To change them, set the `ADMIN_USER` and `ADMIN_PASS` environment variables before starting the application (for example, in the Railway dashboard or in a `.env` file loaded by your environment). The code reads them at startup, so no source edit is required.

Additionally, any registered user in the database can be promoted to administrator by updating their `rol` column to `'admin'` directly in the `usuarios` table. The registration endpoint always creates users with the `cliente` role, so the promotion must be done manually via SQL.

> **Important:** the default credentials are hardcoded as fallbacks inside the repository. If you deploy this project to production, override `ADMIN_USER`, `ADMIN_PASS` and `SECRET_KEY` with secure values using environment variables.

### Usage

**Admin panel (login required):**

| Route         | Description                                       |
|---------------|---------------------------------------------------|
| `/dashboard`  | Main dashboard with metrics and charts            |
| `/inventario` | Product CRUD, search, filters and restocking      |
| `/ventas`     | Point of sale and transaction history             |
| `/analytics`  | Analytics, predictions and recommendations        |
| `/alertas`    | Inventory alerts and opportunities                |

**Public storefront (no login):**

| Route | Description                             |
|-------|-----------------------------------------|
| `/`   | Catalog with shopping cart and checkout |

Purchases made from the public storefront also deduct stock and record the sale in the history, so they appear in analytics just like any other transaction.

### Railway deployment

The repository ships with a `railway.toml` ready for Gunicorn and Nixpacks. You only need to:

1. Create a Railway project and add a PostgreSQL plugin.
2. Connect the GitHub repository.
3. Let Railway inject `DATABASE_URL` automatically on deploy.
4. Set `SECRET_KEY`, `ADMIN_USER` and `ADMIN_PASS` as environment variables on the service.

The configured start command is:

```bash
gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

### Technical notes

- The database is initialized at startup and lazily retried on the first request if the PostgreSQL plugin was not available when the process booted.
- Registered user passwords are stored using SHA-256. The master admin account is validated by direct comparison against the environment variables, bypassing the database.
- Seed data is only inserted if the `productos` table is empty, so a restart does not duplicate information.
- Sales dates are recorded using the `America/Bogota` timezone so the dashboard and daily reports stay consistent.
- The stock-out prediction uses a weighted average in which more recent days carry more weight, and reports a confidence level based on the number of days with data.

### License

This project is distributed under the MIT License. See the `LICENSE` file for details.
