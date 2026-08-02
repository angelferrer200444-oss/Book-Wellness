# 📚 Book Wellness

<p align="center">
  <img src="static/css/logo1.png" width="180" alt="Book Wellness Logo">
</p>

<p align="center">
  <strong>Tu biblioteca personal inteligente.</strong><br>
  Organiza, registra y mejora tus hábitos de lectura mediante inteligencia artificial, estadísticas y herramientas diseñadas para crear una experiencia de lectura completa.
</p>

---

# 📖 ¿Qué es Book Wellness?

Book Wellness es una aplicación web desarrollada en **Python (Flask)** cuyo objetivo es ayudar a cualquier lector a organizar su biblioteca personal, registrar su progreso, establecer metas y descubrir nuevas lecturas mediante un sistema inteligente de recomendaciones.

A diferencia de un simple catálogo de libros, Book Wellness busca convertirse en un verdadero asistente para el bienestar lector, ofreciendo herramientas de seguimiento, análisis y planificación adaptadas a cada usuario.

---

# ✨ Funcionalidades actuales

## 📚 Gestión de Biblioteca

- Registro de libros leídos.
- Libros en lectura.
- Libros pendientes.
- Organización automática de la biblioteca.
- Sistema de búsqueda de libros.
- Filtros y ordenamiento.
- Registro manual de libros personalizados.
- Soporte para portadas propias mediante **Cloudinary**.

---

## 📖 Seguimiento de lectura

- Registro del progreso.
- Seguimiento por páginas.
- Historial de lectura.
- Registro de fechas importantes.
- Calendario de lectura.
- Estado del libro (Leyendo, Pendiente, Finalizado).
- Notas personales por libro.

---

## 🎯 Productividad

- Objetivos personales.
- Generador de rutinas de lectura.
- Recordatorios.
- Calendario de planificación.
- Seguimiento del cumplimiento de metas.

---

## 😊 Bienestar del lector

Book Wellness también incorpora herramientas enfocadas en el bienestar del usuario.

- Registro del estado de ánimo.
- Asociación del estado emocional con las sesiones de lectura.
- Seguimiento de hábitos.

---

## 🤖 Inteligencia Artificial

El recomendador inteligente analiza:

- Géneros favoritos.
- Historial de lectura.
- Nivel del lector.
- Preferencias personales.
- Libros ya registrados.
- Disponibilidad de portada.
- Información bibliográfica.

Las recomendaciones priorizan resultados en español cuando es posible.

---

# 📚 Formatos compatibles

Book Wellness permite registrar distintos tipos de lectura.

- 📖 Libros físicos
- 📱 eBooks
- 🎧 Audiolibros
- 🇯🇵 Manga
- 💬 Cómics
- 🎨 Novelas gráficas
- 🌐 Web Novels

---

# 🌎 APIs y servicios utilizados

Actualmente el proyecto integra distintos servicios externos.

| Servicio | Uso |
|----------|-----|
| Google Books API | Información principal de libros |
| Open Library | API de respaldo |
| Gemini AI | Sistema de recomendaciones |
| Cloudinary | Almacenamiento de portadas personalizadas |

---

# 📊 Estadísticas

El sistema genera estadísticas sobre:

- Libros leídos.
- Libros pendientes.
- Libros en lectura.
- Progreso individual.
- Tiempo estimado de lectura.
- Objetivos completados.
- Rachas de lectura.
- Actividad del usuario.

---

# 🏗 Arquitectura

Book Wellness está siendo desarrollado utilizando Programación Orientada a Objetos (POO).

Algunas de las clases implementadas incluyen:

- Usuario
- Libro
- Preferencias
- Seguimiento
- Estadística
- Calendario
- SeccionLectura
- Notas

---

# 🛠 Tecnologías

### Backend

- Python
- Flask
- Flask-CORS

### Base de datos

- MySQL
- MariaDB

### Frontend

- HTML5
- CSS3
- JavaScript

### APIs y Servicios

- Google Books API
- Open Library API
- Gemini AI
- Cloudinary

---

# 📂 Estructura del proyecto

```
Book-Wellness/

│

├── app.py

├── models/

├── routes/

├── templates/

├── static/

│ ├── css/

│ ├── js/

│ ├── img/

│

├── GoogleLibros.py

├── recomendador.py

├── utilidades.py

└── README.md
```

---

# 🚀 Instalación

```bash
git clone https://github.com/TU-USUARIO/Book-Wellness.git

cd Book-Wellness

pip install -r requirements.txt

python app.py
```

---

# 🚧 Estado del proyecto

> **Book Wellness continúa en desarrollo activo.**

El proyecto evoluciona constantemente con nuevas funcionalidades y mejoras enfocadas en ofrecer una experiencia cada vez más completa para los lectores.

Actualmente se trabaja en:

- 👥 Comunidad de lectores.
- 🏆 Sistema de logros.
- 📈 Estadísticas avanzadas.
- 🎖 Sistema de niveles.
- ❤️ Mejoras del recomendador inteligente.
- 📱 Optimización de la experiencia de usuario.
- 🎨 Mejoras de interfaz y accesibilidad.

---

# 👥 Equipo

| Integrante | Rol |
|------------|-----|
| Angel Ferrer | Desarrollo Full Stack · Arquitectura · Backend · Frontend · Inteligencia Artificial |
| ENDERGM | Desarrollo |
| Boxocean | Desarrollo |

---

# 🎨 Diseño gráfico

**Logo oficial de Book Wellness**

**Instagram:** **@ArteValentia**

*Creadora del logo de la web.*

---

# 📄 Licencia

Este proyecto fue desarrollado con fines educativos y de aprendizaje.

---

<p align="center">

📚 **Book Wellness**

*"Leer no solo cambia lo que sabes; también transforma quién eres."*

</p>
### 🤖 Agente de IA tipo “bibliotecario inteligente”
- Recomendación de libros basada en tus lecturas
- Sugerencias según estado de ánimo (mood reading)
- Análisis de hábitos de lectura
- Conversación con un asistente que entiende tus gustos

### 📊 Sistema de bienestar lector
- Estadísticas de lectura (progreso, constancia, géneros)
- Seguimiento de hábitos saludables de lectura
- Objetivos personales de lectura

### 🧩 Recomendaciones inteligentes
- Libros similares a los que has leído
- Recomendaciones personalizadas con IA
- Posible integración de modelos externos o APIs de IA

---

## 🗄️ Base de datos (en construcción)

Actualmente estamos construyendo una base de datos para:

- 👤 Gestión de usuarios
- 📚 Registro de libros leídos / en progreso / por leer
- 📊 Almacenamiento de estadísticas de lectura

Tecnologías planeadas:
- MySQL (actualmente en desarrollo)
- Posible migración futura a base de datos en la nube

---

## 🌐 Despliegue

El proyecto se encuentra en fase local, pero próximamente será desplegado en:

- 🚀 Render (planificado)
- Posible integración con servicios cloud para base de datos

---

## 🛠️ Tecnologías utilizadas

- Python 3
- Flask
- Requests
- Flask-CORS
- HTML5 / CSS3
- Open Library API
- MySQL (en desarrollo)

---

## 📦 Instalación

Asegúrate de tener las librerias necesarias instaladas, pero recuerda que tenemos intenciones de subirlo en un Hosting.
