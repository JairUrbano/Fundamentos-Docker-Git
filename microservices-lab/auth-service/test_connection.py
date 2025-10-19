import os
import psycopg2
import redis

# Variables de entorno
pg_user = os.getenv("POSTGRES_USER")
pg_pass = os.getenv("POSTGRES_PASSWORD")
pg_db   = os.getenv("POSTGRES_DB")
pg_host = "postgres"

# Conexión a PostgreSQL
try:
    conn = psycopg2.connect(
        host=pg_host,
        database=pg_db,
        user=pg_user,
        password=pg_pass
    )
    print("✅ Conexión a PostgreSQL exitosa")
    conn.close()
except Exception as e:
    print("❌ Error PostgreSQL:", e)

# Conexión a Redis
try:
    r = redis.Redis(host="redis", port=6379)
    r.ping()
    print("✅ Conexión a Redis exitosa")
except Exception as e:
    print("❌ Error Redis:", e)
