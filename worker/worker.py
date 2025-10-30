import os, psycopg2, redis, time

DB = dict(host=os.getenv("POSTGRES_HOST","db"),
          dbname=os.getenv("POSTGRES_DB","isecdb"),
          user=os.getenv("POSTGRES_USER","isecuser"),
          password=os.getenv("POSTGRES_PASSWORD","isecpass"))
R = redis.Redis(host=os.getenv("REDIS_HOST","redis"), port=6379, db=0)

def conn(): return psycopg2.connect(**DB)

def regla_severidad(texto:str)->str:
    t = texto.lower()
    if any(w in t for w in ["credencial","expuesto","público","publico","root sin","comprometido","vulnerabilidad"]): return "alta"
    if any(w in t for w in ["sin cifrar","default","antiguo","obsoleto","permiso amplio","warning"]): return "media"
    return "baja"

if __name__=="__main__":
    print("Worker Bitácora ISec 👷 listo")
    while True:
        item = R.brpop("cola:clasificar")
        rid = int(item[1])
        with conn() as c, c.cursor() as cur:
            cur.execute("SELECT descripcion FROM registros WHERE id=%s;", (rid,))
            row = cur.fetchone()
            if not row: continue
            sev = regla_severidad(row[0])
            cur.execute("UPDATE registros SET severidad=%s WHERE id=%s;", (sev, rid))
        R.delete("cache:registros")
        print(f"[worker] Registro {rid} => severidad {sev}")
        time.sleep(0.2)
