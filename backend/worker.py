from celery import Celery
import time

app = Celery('bitacora', broker='redis://redis:6379/0', backend='redis://redis:6379/1')

@app.task
def procesar_registro(registro_id, titulo, tipo, severidad):
    """Procesa registro en background"""
    time.sleep(2)  # Simular procesamiento
    print(f"✓ Procesando registro #{registro_id}: {titulo}")
    print(f"  Tipo: {tipo}, Severidad: {severidad}")
    return {"status": "procesado", "id": registro_id}

@app.task
def enviar_alerta(registro_id, severidad, titulo):
    """Envía alerta por severidad alta/crítica"""
    if severidad in ['alta', 'crítica']:
        print(f"🚨 ALERTA: Registro #{registro_id} - {titulo}")
        return {"alerta_enviada": True}
    return {"alerta_enviada": False}
