from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
from celery import Celery

app = Flask(__name__)
CORS(app)

celery = Celery('bitacora', broker='redis://redis:6379/0', backend='redis://redis:6379/1')

DB = {
    'dbname': 'bitacora_db',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'db',
    'port': '5432'
}

def get_db_connection():
    conn = psycopg2.connect(**DB)
    return conn

@app.route('/registros', methods=['GET'])
def get_registros():
    """Obtener todos los registros"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id, titulo, descripcion, tipo, severidad, fecha_creacion FROM registros ORDER BY fecha_creacion DESC')
        registros = cur.fetchall()
        cur.close()
        conn.close()
        
        resultado = []
        for reg in registros:
            resultado.append({
                'id': reg[0],
                'titulo': reg[1],
                'descripcion': reg[2],
                'tipo': reg[3],
                'severidad': reg[4],
                'fecha_creacion': str(reg[5])
            })
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/registros', methods=['POST'])
def crear_registro():
    """Crear un nuevo registro"""
    try:
        data = request.get_json(force=True)
        
        titulo = data.get('titulo', '')
        descripcion = data.get('descripcion', '')
        tipo = data.get('tipo', '')
        severidad = data.get('severidad', 'BAJA')
        
        if not titulo or not descripcion or not tipo:
            return jsonify({'error': 'Faltan campos requeridos'}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO registros (titulo, descripcion, tipo, severidad) VALUES (%s, %s, %s, %s) RETURNING id',
            (titulo, descripcion, tipo, severidad)
        )
        registro_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        
        if severidad in ['Alta', 'Media']:
            celery.send_task('worker.enviar_alerta', args=[registro_id, titulo, severidad])
        
        return jsonify({'id': registro_id, 'mensaje': 'Registro guardado correctamente'}), 201
    except Exception as e:
        return jsonify({'error': f'Error al guardar: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health():
    """Verificar que el backend está corriendo"""
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

