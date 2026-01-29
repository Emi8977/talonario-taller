"""
Interfaz web para generar talonarios PDF 5x5cm
"""
from flask import Flask, render_template, request, send_file, jsonify
from flask_cors import CORS
from back import TalonarioServicio5x5
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Configuración
CARPETA_DESCARGAS = r"c:\Users\dell\Desktop\talonario taller\descargas"
os.makedirs(CARPETA_DESCARGAS, exist_ok=True)


@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')


@app.route('/api/items-predeterminados', methods=['GET'])
def obtener_items_predeterminados():
    """Retorna los items predeterminados"""
    try:
        talonario = TalonarioServicio5x5()
        return jsonify({
            'items': talonario.items
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/generar-talonario', methods=['POST'])
def generar_talonario():
    """Genera el talonario PDF 5x5"""
    try:
        datos = request.json
        
        # Crear talonario
        talonario = TalonarioServicio5x5()
        
        # Agregar items adicionales si los hay
        items_adicionales = datos.get('items_adicionales', [])
        for item in items_adicionales:
            talonario.agregar_item(
                tipo=item.get('tipo', 'checkbox'),
                valor=item.get('valor', '')
            )
        
        # Generar archivo
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        nombre_archivo = f"talonario_5x5_{timestamp}.pdf"
        
        # Ruta del logo - usar la nueva imagen con fondo removido
        ruta_logo = os.path.join(os.path.dirname(__file__), 'app_icon-removebg-preview.png')
        
        ruta_archivo = talonario.generar_pdf(
            nombre_archivo=nombre_archivo,
            ruta_salida=CARPETA_DESCARGAS,
            ruta_logo=ruta_logo
        )
        
        return jsonify({
            'success': True,
            'archivo': nombre_archivo,
            'ruta': ruta_archivo,
            'mensaje': f'Talonario 5x5cm generado exitosamente'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/descargar/<nombre_archivo>', methods=['GET'])
def descargar(nombre_archivo):
    """Descarga el archivo PDF"""
    try:
        ruta_archivo = os.path.join(CARPETA_DESCARGAS, nombre_archivo)
        
        if not os.path.exists(ruta_archivo):
            return jsonify({'error': 'Archivo no encontrado'}), 404
        
        return send_file(ruta_archivo, as_attachment=True)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/listar-archivos', methods=['GET'])
def listar_archivos():
    """Lista los archivos generados"""
    try:
        archivos = os.listdir(CARPETA_DESCARGAS)
        archivos_info = []
        
        for archivo in archivos:
            ruta_completa = os.path.join(CARPETA_DESCARGAS, archivo)
            if os.path.isfile(ruta_completa) and archivo.endswith('.pdf'):
                tamaño = os.path.getsize(ruta_completa) / 1024  # KB
                fecha_mod = os.path.getmtime(ruta_completa)
                archivos_info.append({
                    'nombre': archivo,
                    'tamaño': f"{tamaño:.2f} KB",
                    'fecha': datetime.fromtimestamp(fecha_mod).strftime('%d/%m/%Y %H:%M')
                })
        
        return jsonify({'archivos': archivos_info})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
