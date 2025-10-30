import express from "express";

//  Config API 
const raw = process.env.BACKEND_URL || process.env.API_URL || "http://backend:8000";
const API_BASE = raw.endsWith("/api") ? raw : `${raw}/api`;

const app = express();
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

const _fetch = global.fetch ?? ((...a) => import("node-fetch").then(({ default: f }) => f(...a)));

async function getJSON(url, opts = {}) {
  const r = await _fetch(url, {
    ...opts,
    headers: { "Content-Type": "application/json", ...(opts.headers || {}) },
  });
  if (!r.ok) throw new Error(`HTTP ${r.status} ${r.statusText}`);
  return r.json();
}

app.all("/api/*", async (req, res) => {
  try {
    const url = `${API_BASE}${req.path.replace(/^\/api/, "")}`;
    const init = { method: req.method, headers: { ...req.headers } };
    if (req.headers["content-type"]?.includes("application/json")) {
      init.headers["content-type"] = "application/json";
      init.body = JSON.stringify(req.body ?? {});
    } else if (["POST", "PUT", "PATCH"].includes(req.method)) {
      init.body = new URLSearchParams(req.body ?? {}).toString();
      init.headers["content-type"] = "application/x-www-form-urlencoded";
    }
    const r = await _fetch(url, init);
    const text = await r.text();
    res.status(r.status).send(text);
  } catch (e) {
    res.status(502).send("Error proxy API");
  }
});

app.get("/", async (_req, res) => {
  try {
    const registros = await getJSON(`${API_BASE}/registros`);
    const options = [
      ["prueba_red", "Prueba de Red"],
      ["docker", "Docker"],
      ["k8s", "Kubernetes"],
      ["otro", "Otro"],
    ]
      .map(([v, t]) => `<option value="${v}">${t}</option>`)
      .join("");
    const rows = registros
      .map(
        (r) => `
      <tr>
        <td>${r.id}</td><td>${r.titulo}</td><td>${r.tipo}</td>
        <td>${r.severidad}</td><td>${r.estado}</td>
        <td>${r.evidencia_url ? `<a href="${r.evidencia_url}" target="_blank">ver</a>` : "-"}</td>
      </tr>`
      )
      .join("");
    res.send(`
      <meta charset="utf-8"/>
      <title>Bitácora ISec</title>
      <div style="max-width:920px;margin:24px auto;font-family:system-ui">
        <h1 style="margin:0 0 12px">Bitácora ISec</h1>
        <p style="margin:4px 0 16px;color:#555">
          Aquí anoto de forma sencilla lo que voy haciendo o encontrando para la materia.
          Escribir, guardar y listo.
        </p>
        <form method="post" action="/crear" style="display:flex;gap:8px;flex-wrap:wrap">
          <input name="titulo" placeholder="Título rápido" required style="flex:1;padding:8px">
          <input name="descripcion" placeholder="¿Qué pasó?" required style="flex:2;padding:8px">
          <select name="tipo" style="padding:8px">${options}</select>
          <input name="evidencia_url" placeholder="URL evidencia (opcional)" style="flex:1;padding:8px">
          <button style="padding:8px 12px">Guardar</button>
        </form>
        <hr style="margin:16px 0"/>
        <table border="1" cellpadding="6" cellspacing="0" width="100%">
          <tr><th>ID</th><th>Título</th><th>Tipo</th><th>Severidad</th><th>Estado</th><th>Evidencia</th></tr>
          ${rows}
        </table>
        <p style="color:#777;margin-top:8px">
          Después de guardar, la prioridad se completa sola al rato.
        </p>
      </div>
    `);
  } catch (e) {
    res.status(500).send("API caída o sin red");
  }
});

app.post("/crear", async (req, res) => {
  try {
    await _fetch(`${API_BASE}/registros`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        titulo: req.body.titulo,
        descripcion: req.body.descripcion,
        tipo: req.body.tipo,
        evidencia_url: req.body.evidencia_url || null,
      }),
    });
    res.redirect("/");
  } catch (e) {
    res.status(502).send("No se pudo crear el registro");
  }
});

app.get("/health", (_req, res) => res.json({ web: "ok", api: API_BASE }));

app.listen(3000, () => console.log("Web Bitácora ISec en :3000"));
