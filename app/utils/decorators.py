from functools import wraps
from flask import session, redirect, url_for, request, make_response

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Verifica si el 'usuario' está en la sesión
        if 'usuario' not in session:
            # Si no está autenticado, redirige a la página de login
            # y guarda la URL original para redirigir después del login (opcional pero bueno para UX)
            return redirect(url_for('auth.buscarLogin', next=request.url))
        
        # Si está autenticado, ejecuta la función y agrega headers de caché
        response = f(*args, **kwargs)
        
        # Si la respuesta es un string (template renderizado), convertirlo a response
        if isinstance(response, str):
            response = make_response(response)
        
        # Agregar headers para prevenir caché
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        
        return response
    return decorated_function 