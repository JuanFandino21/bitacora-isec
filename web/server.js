import express from "express";
const app = express();
app.use(express.urlencoded({extended:true}));
app.use(express.json());

const API = process.env.API_URL || "http://backend:8000/api";

async function getJSON(url, opts={}) {
  const r = await fetch(url, { ...opts, headers: {'Content-Type':'application/json', ...(opts.headers||{})}});
  return r.json();
}

app.get("/", async (_req,res) => {
  try{
    const registros = await getJSON(`${API}/registros`);
    const options = [
      ["prueba_red","Prueba de Red"],
      ["docker","Docker"],
      ["k8s","Kubernetes"],
      ["otro","Otro"]
    ].map(([v,t])=>`<option value="${v}">${t}</option>`).join("");
    const rows = registros.map(r=>`
      <tr>
        <td>${r.id}</td><td>${r.titulo}</td><td>${r.tipo}</td>
        <td>${r.severidad}</td><td>${r.estado}</td>
        <td>${r.evidencia_url?`<a href="${r.evidencia_url}" target="_blank">ver</a>`:"-"}</td>
      </tr>`).join("");
    res.send(`
      <meta charset="utf-8"/>
      <title>Bitácora ISec</title>
      <div style="max-width:920px;margin:24px auto;font-family:system-ui">
        <h1 style="margin:0 0 12px">Bitácora ISec</h1>
        <p style="margin:4px 0 16px;color:#555">Apunto lo que voy haciendo en infra/seguridad, sin enredos.</p>
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
        <p style="color:#777;margin-top:8px">La severidad se ajusta sola con el worker (segundos).</p>
      </div>
    `);
  }catch(e){ res.status(500).send("API caída o sin red"); }
});

app.post("/crear", async (req,res)=>{
  await fetch(`${API}/registros`, {method:"POST", body: JSON.stringify({
    titulo: req.body.titulo, descripcion: req.body.descripcion, tipo: req.body.tipo, evidencia_url: req.body.evidencia_url || null
  }), headers:{'Content-Type':'application/json'}});
  res.redirect("/");
});

app.listen(3000, ()=>console.log("Web Bitácora ISec en :3000"));
