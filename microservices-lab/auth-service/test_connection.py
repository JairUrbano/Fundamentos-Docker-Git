# auth-service/test_connection.py
import os
import sys
try:
    import psycopg2
    import redis
except ImportError:
    print("Faltan dependencias (psycopg2-binary, redis). Instálalas antes de ejecutar.")
    sys.exit(1)

def get_env():
    db_host = os.getenv('DB_HOST', os.getenv('POSTGRES_HOST', 'postgres'))
    db_name = os.getenv('DB_NAME', os.getenv('POSTGRES_DB', 'main_db'))
    db_user = os.getenv('DB_USER', os.getenv('POSTGRES_USER', 'devuser'))
    db_pass = os.getenv('DB_PASS', os.getenv('POSTGRES_PASSWORD', 'devpass'))
    redis_host = os.getenv('REDIS_HOST', 'redis')
    redis_port = int(os.getenv('REDIS_PORT', '6379'))
    return db_host, db_name, db_user, db_pass, redis_host, redis_port

def test_postgres(db_host, db_name, db_user, db_pass):
    try:
        conn = psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=db_pass, connect_timeout=5)
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        print("✅ PostgreSQL OK:", cur.fetchone())
        cur.close()
        conn.close()
    except Exception as e:
        print("❌ Error PostgreSQL:", e)

def test_redis(redis_host, redis_port):
    try:
        r = redis.Redis(host=redis_host, port=redis_port, socket_connect_timeout=5)
        r.ping()
        print("✅ Redis OK: PONG")
    except Exception as e:
        print("❌ Error Redis:", e)

if __name__ == '__main__':
    db_host, db_name, db_user, db_pass, redis_host, redis_port = get_env()
    print("Variables usadas:", dict(DB_HOST=db_host, DB_NAME=db_name, DB_USER=db_user, REDIS_HOST=redis_host, REDIS_PORT=redis_port))
    test_postgres(db_host, db_name, db_user, db_pass)
    test_redis(redis_host, redis_port)
