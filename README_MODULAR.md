# Estructura Modular de la Aplicación

## Nueva Estructura de Archivos

```
mapa_incidentes/
├── app/                          # Paquete principal de la aplicación
│   ├── __init__.py              # Factory de la aplicación Flask
│   ├── routes/                  # Rutas de la aplicación
│   │   ├── __init__.py
│   │   ├── auth.py             # Rutas de autenticación (login, registro)
│   │   ├── main.py             # Rutas principales (páginas)
│   │   └── api.py              # Rutas de la API (incidentes, zonas)
│   ├── models/                  # Modelos de datos (futuro)
│   │   └── __init__.py
│   └── utils/                   # Utilidades y helpers
│       ├── __init__.py
│       ├── database.py         # Conexión a la base de datos
│       └── decorators.py       # Decoradores (login_required)
├── config.py                    # Configuración centralizada
├── run.py                       # Punto de entrada de la aplicación
├── app.py                       # Archivo original (ahora obsoleto)
├── static/                      # Archivos estáticos
├── plantillas/                  # Plantillas HTML
└── README_MODULAR.md           # Este archivo
```

## Beneficios de la Modularización

1. **Separación de Responsabilidades**: Cada módulo tiene una función específica
2. **Mantenibilidad**: Es más fácil encontrar y modificar código
3. **Escalabilidad**: Fácil agregar nuevas funcionalidades
4. **Reutilización**: Los módulos pueden ser reutilizados
5. **Testing**: Más fácil escribir pruebas unitarias

## Cómo Ejecutar la Aplicación

### Opción 1: Usar el nuevo archivo run.py
```bash
python run.py
```

### Opción 2: Usar Flask directamente
```bash
export FLASK_APP=run.py
export FLASK_ENV=development
flask run
```

## Estructura de Blueprints

### Auth Blueprint (`app/routes/auth.py`)
- `/login` - Página de login
- `/loginUsuario` - Procesar login
- `/register` - Página de registro
- `/registrarUsuario` - Procesar registro

### Main Blueprint (`app/routes/main.py`)
- `/home` - Página de inicio
- `/principal` - Página principal (protegida)
- `/segura` - Ruta segura 1 (protegida)
- `/segura2` - Ruta segura 2 (protegida)

### API Blueprint (`app/routes/api.py`)
- `/incidentes` - Obtener incidentes
- `/zonas_seguridad` - Obtener zonas de seguridad
- `/zonas_peligrosas` - Obtener zonas peligrosas

## Configuración

La configuración está centralizada en `config.py` y usa variables de entorno desde un archivo `.env`:

```env
SECRET_KEY=tu_clave_secreta
DB_NAME=nombre_base_datos
DB_USER=usuario_db
DB_PASSWORD=password_db
DB_HOST=localhost
DB_PORT=5432
```

## Próximos Pasos

1. **Modelos**: Crear modelos en `app/models/` para manejar datos
2. **Servicios**: Crear servicios en `app/services/` para lógica de negocio
3. **Tests**: Agregar pruebas unitarias
4. **Logging**: Implementar sistema de logs
5. **Error Handling**: Manejo centralizado de errores 