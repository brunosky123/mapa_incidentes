import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'clave_secreta_por_defecto')
    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    
    # Configuraciones de sesión para mayor seguridad
    SESSION_COOKIE_SECURE = True  # Solo cookies HTTPS
    SESSION_COOKIE_HTTPONLY = True  # Prevenir acceso desde JavaScript
    SESSION_COOKIE_SAMESITE = 'Lax'  # Protección CSRF
    PERMANENT_SESSION_LIFETIME = 3600  # Sesión expira en 1 hora
    SESSION_REFRESH_EACH_REQUEST = True  # Renovar sesión en cada request 