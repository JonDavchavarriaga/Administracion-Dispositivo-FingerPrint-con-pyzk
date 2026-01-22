
# 🖐️ Proyecto Huellero – Plataforma de Asistencia Biométrica

Sistema de gestión de asistencia basado en **dispositivos biométricos**, con arquitectura desacoplada **frontend + backend**, su backend con arquitectura hexagonal,preparado para ejecución local o despliegue mediante **Docker**.

---

## 🎯 Objetivo del Proyecto

Permitir el registro y sincronización de asistencia desde dispositivos biométricos físicos, exponiendo la información a través de una API y una interfaz web.



## 🧱 Esquema de Archivos
ProyectoHuellero/

├── backend/ 

├── frontend/ # React + Vite

├── docker-compose.yml

├── .env

└── README.md


---

## 🛠️ Tecnologías

### Backend
- Python 3.11
- FastAPI
- SQLAlchemy
- MySQL (externo)
- pyzk (libreria para dispositivos biométricos)

### Frontend
- React
- Vite
- Axios
- TailwindCSS

### Infraestructura
- Docker
- Docker Compose

---

## 🔄 Independencia de Servicios

**El frontend y el backend pueden ejecutarse de forma independiente o conjunta.**

- El frontend consume la API vía `VITE_API_URL`
- El backend se conecta a MySQL usando variables de entorno
- MySQL **NO está dockerizado** 


---

## ⚙️ Variables de Entorno

Crear un archivo `.env` en la raíz del proyecto, en el repositorio se explica por medio de `.env.example`.

---

## Instalación y Ejecución

### Requisitos

- Docker y Docker compose

- MySQl

### Levantar el sistema completo

- `docker comose up --build`

### Instalación desacoplada 

Si por alguna razón solo se desea levantar el backend o el frontend
se ingresa a cada carpeta la cual posé también un readme.md con las instrucciones de instalación


