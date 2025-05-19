## 🧰 Requisitos previos

Asegúrate de tener instalado:

### ✅ Python 3

```bash
python3 --version
```

### ✅ pip (gestor de paquetes de Python)

```bash
sudo apt install python3-pip -y
```

### ✅ venv (para entornos virtuales)

```bash
sudo apt install python3-venv -y
```

---

## 🚀 Crear un nuevo proyecto Django

### 1. 📁 Crea una carpeta para tu proyecto

```bash
mkdir mi_proyecto_django
cd mi_proyecto_django
```

---

### 2. 🧪 Crea un entorno virtual

```bash
python3 -m venv venv
```

Actívalo:

```bash
source venv/bin/activate
```

Verás que el prompt cambia a algo como `(venv)`.

---

### 3. 📦 Instala Django

```bash
pip install django
```

Confirma que se instaló:

```bash
django-admin --version
```

---

### 4. ⚙️ Crea el proyecto Django

```bash
django-admin startproject mi_proyecto .
```

El punto (`.`) al final indica que se cree en la carpeta actual.

---

### 5. 🛠️ Prueba que funciona

Ejecuta el servidor de desarrollo:

```bash
python manage.py runserver
```

Abre tu navegador y visita:
👉 [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

Deberías ver la pantalla de bienvenida de Django.

---

En Django, la configuración de la base de datos se hace en el archivo:

```bash
mi_proyecto/settings.py
```

Aquí tienes la ruta completa si estás en el directorio raíz del proyecto:

```bash
mi_proyecto_django/mi_proyecto/settings.py
```

---

## 🛠️ Paso a paso para configurar la base de datos

### 1. Abre el archivo `settings.py`

Puedes usar `nano`, `vim`, o VS Code. Por ejemplo:

```bash
nano mi_proyecto/settings.py
```

---

### 2. Busca la sección `DATABASES`

Por defecto, se ve así (usa SQLite):

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

---

### 3. Configura para PostgreSQL (ejemplo):

Primero, instala el conector:

```bash
pip install psycopg2-binary
```

Luego cambia la configuración:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nombre_base_datos',
        'USER': 'usuario',
        'PASSWORD': 'contraseña',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

### 4. Aplica las migraciones iniciales

Después de configurar la base:

```bash
python manage.py migrate
```

---

### 5. (Opcional) Crear superusuario para el admin

```bash
python manage.py createsuperuser
```

---

¿Necesitas que te genere la configuración exacta si ya tienes los datos de tu base?
