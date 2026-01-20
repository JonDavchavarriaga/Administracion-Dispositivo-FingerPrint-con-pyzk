# Sistema de Asistencia Biométrica - Backend

Backend desarrollado en **Python + FastAPI** para la gestión de dispositivos biométricos (ZKTeco) y registros de asistencia.

---

## 🧩 Arquitectura

El proyecto sigue una arquitectura por capas:

backend/

├── app/
│ ├── domain/ # Modelos de dominio
│ ├── application/ # Casos de uso / servicios
│ ├── infrastructure/ # APIs, dispositivos, repositorios
│ └── main.py # Punto de entrada
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md

---

## 🚀 Requisitos

- Python 3.10+
- pip
- Dispositivo biométrico ZKTeco (opcional para ambientes Reales y productivos)

---

## ⚙️ Instalación

- python -m venv venv
- source venv/bin/activate  # Linux / Mac
- venv\Scripts\activate     # Windows
- pip install -r requirements.txt
- Editar variables de entorno

## Ejecución 