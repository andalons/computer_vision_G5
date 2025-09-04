
import uvicorn
import sys, os

def main():
    """
    Función principal para iniciar el servidor API de análisis de video.
    Organiza el arranque y muestra mensajes claros de error si la app no se encuentra.
    """
    print("\n🚀 Iniciando server API de Análisis de Video...")
    print("📡 La API estará disponible en:")
    print("   • Interfaz web: http://localhost:8000")
    print("   • Documentación automática: http://localhost:8000/docs")
    print("   • OpenAPI Schema: http://localhost:8000/openapi.json")
    print("   • Documentación alternativa: http://localhost:8000/redoc")
    print("💡 Para detener el servidor, presiona Ctrl+C")
    print("="*60)

    try:
        # Intentar importar la app principal
        from app.main import app
    except ImportError as e:
        print(f"❌ Error importando la aplicación FastAPI: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        sys.exit(1)

    try:
        # Iniciar el servidor Uvicorn (sin reload, para evitar error de import string)
        uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error al iniciar el servidor: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
