"""
Script para probar conexiones a PostgreSQL y Redis
"""
import os
import sys
import psycopg2
import redis
import time

def test_postgresql_connection():
    """Probar conexión a PostgreSQL"""
    print(" Probando conexión a PostgreSQL...")
    
    # Obtener variables de entorno
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '5432')
    db_name = os.getenv('DB_NAME', 'auth_db')
    db_user = os.getenv('DB_USER', 'postgres')
    db_password = os.getenv('DB_PASSWORD', 'password')
    
    print(f"   Host: {db_host}:{db_port}")
    print(f"   Database: {db_name}")
    print(f"   User: {db_user}")
    
    try:
        connection = psycopg2.connect(
            host=db_host,
            port=db_port,
            database=db_name,
            user=db_user,
            password=db_password,
            connect_timeout=10
        )
        
        # Probar consulta simple
        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        
        cursor.execute("SELECT current_database();")
        db_name = cursor.fetchone()
        
        print(" Conexión a PostgreSQL exitosa!")
        print(f"   PostgreSQL Version: {db_version[0]}")
        print(f"   Database conectada: {db_name[0]}")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f" Error conectando a PostgreSQL: {e}")
        return False

def test_redis_connection():
    """Probar conexión a Redis"""
    print("🔍 Probando conexión a Redis...")
    
    # Obtener variables de entorno
    redis_host = os.getenv('REDIS_HOST', 'localhost')
    redis_port = os.getenv('REDIS_PORT', '6379')
    redis_password = os.getenv('REDIS_PASSWORD', '')
    
    print(f"   Host: {redis_host}:{redis_port}")
    
    try:
        # Configurar conexión Redis
        redis_client = redis.Redis(
            host=redis_host,
            port=redis_port,
            password=redis_password if redis_password else None,
            db=0,
            socket_connect_timeout=10,
            decode_responses=True
        )
        
        # Probar ping
        ping_result = redis_client.ping()
        if ping_result:
            print(" Conexión a Redis exitosa!")
            
            # Probar escritura y lectura
            test_key = "test_connection"
            test_value = f"Hello from auth-service at {time.time()}"
            
            redis_client.set(test_key, test_value, ex=30)  # Expira en 30 segundos
            retrieved_value = redis_client.get(test_key)
            
            if retrieved_value == test_value:
                print("Lectura/escritura en Redis funcionando correctamente")
            else:
                print("Lectura/escritura en Redis con valores inesperados")
                
            return True
        else:
            print("Redis no respondió al ping")
            return False
            
    except Exception as e:
        print(f"Error conectando a Redis: {e}")
        return False

def test_environment_variables():
    """Verificar que las variables de entorno estén configuradas"""
    print("🔍 Verificando variables de entorno...")
    
    required_vars = ['DB_HOST', 'DB_NAME', 'DB_USER', 'DB_PASSWORD', 'REDIS_HOST']
    optional_vars = ['DB_PORT', 'REDIS_PORT', 'REDIS_PASSWORD']
    
    all_present = True
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"    {var}: {value[:3]}..." if var == 'DB_PASSWORD' else f"    {var}: {value}")
        else:
            print(f"   {var}: NO DEFINIDA")
            all_present = False
    
    for var in optional_vars:
        value = os.getenv(var)
        if value:
            print(f"    {var}: {value}")
        else:
            print(f"    {var}: No definida (usando valor por defecto)")

    return all_present

def main():
    """Función principal"""
    print(" Iniciando pruebas de conexión...")
    print("=" * 50)
    
    # Verificar variables de entorno
    env_ok = test_environment_variables()
    print("=" * 50)
    
    if not env_ok:
        print(" Algunas variables requeridas no están definidas")
        print(" Asegúrate de configurar todas las variables requeridas")
    
    # Probar conexiones
    postgres_ok = test_postgresql_connection()
    print("-" * 30)
    redis_ok = test_redis_connection()
    print("=" * 50)
    
    # Resumen
    print(" RESUMEN DE PRUEBAS:")
    print(f"   PostgreSQL: {' OK' if postgres_ok else ' FALLÓ'}")
    print(f"   Redis: {' OK' if redis_ok else ' FALLÓ'}")
    print(f"   Variables de entorno: {' OK' if env_ok else ' INCOMPLETAS'}")
    
    if postgres_ok and redis_ok:
        print(" ¡Todas las conexiones son exitosas!")
        sys.exit(0)
    else:
        print(" Revisa la configuración y que los servicios estén ejecutándose")
        sys.exit(1)

if __name__ == "__main__":
    main()