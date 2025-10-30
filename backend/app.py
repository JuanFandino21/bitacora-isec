from flask import Flask, request, jsonify
import os, psycopg2, redis, json

app = Flask(__name__)
DB = dict(host=os.getenv("POSTGRES_HOST","db"),
          dbname=os.getenv("POSTGRES_DB","isecdb"),
          user=os.getenv("POSTGRES_USER","isecuser"),
          password=os.getenv("POSTGRES_PASSWORD","isecpass"))
R = redis.Redis(host=os.getenv("REDIS_HOST","redis"), port=6379, db=0)

def conn(): return psycopg2.connect(**DB)

def init_db():
    with conn() as c, c.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS registros(
          id SERIAL PRIMARY KEY,
          titulo TEXT NOT NULL,
          descripcion TEXT NOT NULL,
          tipo TEXT NOT NULL CHECK (tipo IN ('prueba_red','docker','k8s','otro')),
          estado TEXT NOT NULL CHECK (estado IN ('pendiente','en_proceso','cerrado')) DEFAULT 'pendiente',
          severidad TEXT NOT NULL CHECK (severidad IN ('baja','media','alta')) DEFAULT 'baja',
          evidencia_url TEXT
        );""")
    print("DB lista")

@app.get("/api/registros")
def listar():
    key="cache:registros"
    if (c:=R.get(key)): return jsonify(json.loads(c))
    with conn() as c, c.cursor() as cur:
        cur.execute("SELECT id,titulo,descripcion,tipo,estado,severidad,evidencia_url FROM registros ORDER BY id DESC;")
        rows=[{"id":i,"titulo":t,"descripcion":d,"tipo":tp,"estado":e,"severidad":s,"evidencia_url":u} for i,t,d,tp,e,s,u in cur.fetchall()]
    R.setex(key,5,json.dumps(rows))
    return jsonify(rows)

@app.post("/api/registros")
def crear():
    data = request.get_json(force=True)
    falta = [k for k in ["titulo","descripcion","tipo"] if not data.get(k)]
    if falta: return {"error": f"Falta: {', '.join(falta)}"},400
    with conn() as c, c.cursor() as cur:
        cur.execute("""INSERT INTO registros(titulo,descripcion,tipo,estado,severidad,evidencia_url)
                       VALUES (%s,%s,%s,'pendiente','baja',%s) RETURNING id;""",
                    (data["titulo"].strip(), data["descripcion"].strip(), data["tipo"], data.get("evidencia_url")))
        new_id = cur.fetchone()[0]
    # empujar a la cola para clasificar severidad
    R.lpush("cola:clasificar", new_id)
    R.delete("cache:registros")
    return {"ok": True, "id": new_id},201

@app.patch("/api/registros/<int:rid>")
def actualizar(rid):
    data = request.get_json(force=True)
    campos = []
    vals = []
    for k in ["titulo","descripcion","tipo","estado","severidad","evidencia_url"]:
        if k in data:
            campos.append(f"{k}=%s"); vals.append(data[k])
    if not campos: return {"error":"Nada para actualizar"},400
    vals.append(rid)
    with conn() as c, c.cursor() as cur:
        cur.execute(f"UPDATE registros SET {', '.join(campos)} WHERE id=%s;", vals)
    R.delete("cache:registros")
    return {"ok": True}

@app.get("/api/health")
def health(): return {"ok": True}

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=8000)
