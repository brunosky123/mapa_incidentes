#!/usr/bin/env python3
"""
Script de prueba para verificar la funcionalidad de la aplicación modular
"""

import requests
import time
import sys

# URL base de la aplicación
BASE_URL = "http://localhost:5000"

def test_route(url, expected_status=200, description=""):
    """Prueba una ruta específica"""
    try:
        response = requests.get(f"{BASE_URL}{url}", timeout=5)
        status = response.status_code
        success = status == expected_status
        
        print(f"✅ {description} - {url}")
        print(f"   Status: {status} (esperado: {expected_status})")
        
        if success:
            print(f"   ✅ PASÓ")
        else:
            print(f"   ❌ FALLÓ")
            
        return success
        
    except requests.exceptions.ConnectionError:
        print(f"❌ {description} - {url}")
        print(f"   ❌ No se pudo conectar al servidor")
        return False
    except Exception as e:
        print(f"❌ {description} - {url}")
        print(f"   ❌ Error: {str(e)}")
        return False

def test_api_endpoint(url, description=""):
    """Prueba un endpoint de la API"""
    try:
        response = requests.get(f"{BASE_URL}{url}", timeout=5)
        status = response.status_code
        
        if status == 200:
            data = response.json()
            if 'features' in data:
                print(f"✅ {description} - {url}")
                print(f"   Status: {status}")
                print(f"   Features encontradas: {len(data['features'])}")
                print(f"   ✅ PASÓ")
                return True
            else:
                print(f"❌ {description} - {url}")
                print(f"   ❌ Respuesta no tiene formato GeoJSON esperado")
                return False
        else:
            print(f"❌ {description} - {url}")
            print(f"   Status: {status}")
            print(f"   ❌ FALLÓ")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"❌ {description} - {url}")
        print(f"   ❌ No se pudo conectar al servidor")
        return False
    except Exception as e:
        print(f"❌ {description} - {url}")
        print(f"   ❌ Error: {str(e)}")
        return False

def main():
    """Función principal de pruebas"""
    print("🧪 INICIANDO PRUEBAS DE LA APLICACIÓN MODULAR")
    print("=" * 50)
    
    # Esperar un momento para que el servidor se inicie
    print("⏳ Esperando que el servidor se inicie...")
    time.sleep(3)
    
    # Lista de pruebas
    tests = [
        # Rutas principales
        ("/home", 200, "Página de inicio"),
        ("/login", 200, "Página de login"),
        ("/register", 200, "Página de registro"),
        
        # Rutas protegidas (deberían redirigir a login)
        ("/principal", 302, "Página principal (protegida)"),
        ("/segura", 302, "Ruta segura 1 (protegida)"),
        ("/segura2", 302, "Ruta segura 2 (protegida)"),
    ]
    
    # Ejecutar pruebas de rutas
    print("\n📋 PRUEBAS DE RUTAS:")
    print("-" * 30)
    
    passed_routes = 0
    total_routes = len(tests)
    
    for url, expected_status, description in tests:
        if test_route(url, expected_status, description):
            passed_routes += 1
        print()
    
    # Pruebas de API
    print("\n📡 PRUEBAS DE API:")
    print("-" * 30)
    
    api_tests = [
        ("/incidentes", "Endpoint de incidentes"),
        ("/zonas_seguridad", "Endpoint de zonas de seguridad"),
        ("/zonas_peligrosas", "Endpoint de zonas peligrosas"),
    ]
    
    passed_api = 0
    total_api = len(api_tests)
    
    for url, description in api_tests:
        if test_api_endpoint(url, description):
            passed_api += 1
        print()
    
    # Resumen
    print("\n📊 RESUMEN DE PRUEBAS:")
    print("=" * 50)
    print(f"Rutas: {passed_routes}/{total_routes} pasaron")
    print(f"API: {passed_api}/{total_api} pasaron")
    print(f"Total: {passed_routes + passed_api}/{total_routes + total_api} pasaron")
    
    if passed_routes == total_routes and passed_api == total_api:
        print("\n🎉 ¡TODAS LAS PRUEBAS PASARON! La aplicación modular funciona correctamente.")
        return True
    else:
        print("\n⚠️  Algunas pruebas fallaron. Revisa los errores arriba.")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Pruebas interrumpidas por el usuario")
        sys.exit(1) 