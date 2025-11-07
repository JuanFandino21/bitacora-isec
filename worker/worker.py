import psycopg2
from psycopg2 import OperationalError
import time
import os

# Configuración de la base de datos
DB_CONFIG = {
    'dbname': os.getenv('POSTGRES_DB', 'bitacora_db'),
    'user': os.getenv('POSTGRES_USER', 'postgres'),
    'password': os.getenv('POSTGRES_PASSWORD', 'postgres'),
    'host': os.getenv('DB_HOST', 'db'),
    'port': os.getenv('DB_PORT', '5432')
}

def get_db_connection(max_retries=5, retry_delay=2):
    """
    Intenta conectarse a la base de datos con reintentos
    """
    for attempt in range(max_retries):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            print(f"✓ Worker conectado a PostgreSQL (intento {attempt + 1})")
            return conn
        except OperationalError as e:
            if attempt == max_retries - 1:
                print(f"✗ Worker: No se pudo conectar después de {max_retries} intentos")
                raise
            print(f"⚠ Worker intento {attempt + 1} fallido. Reintentando en {retry_delay}s...")
            time.sleep(retry_delay)

def main():
    """
    Función principal del worker
    """
    print("Iniciando worker de Bitácora ISEC...")
    
    # Conectar a la base de datos
    conn = get_db_connection()
    
    try:
        # Aquí puedes agregar la lógica de tu worker
        # Por ejemplo, procesar tareas en segundo plano
        print("✓ Worker iniciado correctamente")
        
        # Mantener el worker ejecutándose
        while True:
            # Tu lógica de procesamiento aquí
            time.sleep(10)
            
    except KeyboardInterrupt:
        print("\n✓ Worker detenido por el usuario")
    except Exception as e:
        print(f"✗ Error en worker: {e}")
    finally:
        if conn:
            conn.close()
            print("✓ Conexión cerrada")

if __name__ == '__main__':
    main()

