"""
Generador de talonario en PDF optimizado para A4 con checkboxes imprimibles
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from datetime import datetime
import os


class TalonarioServicio5x5:
    """Generador de talonarios 5x5cm con checkboxes imprimibles"""
    
    # Items predeterminados
    ITEMS_PREDETERMINADOS = [
        {'tipo': 'titulo', 'valor': 'Service'},
        {'tipo': 'texto', 'valor': 'Fecha: _____/_____/_____'},
        {'tipo': 'texto', 'valor': 'KM: __________________'},
        {'tipo': 'checkbox', 'valor': 'Aceite de motor'},
        {'tipo': 'checkbox', 'valor': 'Filtro de aceite'},
        {'tipo': 'checkbox', 'valor': 'Filtro de aire'},
        {'tipo': 'checkbox', 'valor': 'Filtro de combustible'},
        {'tipo': 'checkbox', 'valor': 'Aceite de caja'},
        {'tipo': 'checkbox', 'valor': 'Otro: ________'},
    ]
    
    def __init__(self, titulo="TALONARIO SERVICIO"):
        """
        Inicializa el generador de talonarios
        
        Args:
            titulo: Título del talonario
        """
        self.titulo = titulo
        self.items = list(self.ITEMS_PREDETERMINADOS)  # Copiar items predeterminados
    
    def agregar_item(self, tipo, valor):
        """
        Agrega un item adicional al talonario
        
        Args:
            tipo: 'checkbox' o 'texto'
            valor: Descripción del item
        """
        self.items.append({
            'tipo': tipo,
            'valor': valor
        })
    
    def limpiar_items_adicionales(self):
        """Limpia los items adicionales manteniendo los predeterminados"""
        self.items = list(self.ITEMS_PREDETERMINADOS)
    
    def generar_pdf(self, nombre_archivo="talonario_5x5.pdf", ruta_salida=".", ruta_logo=None):
        """
        Genera PDF con una ficha optimizada de 7cm x 9cm
        
        Args:
            nombre_archivo: Nombre del archivo PDF
            ruta_salida: Ruta donde guardar el archivo
            ruta_logo: Ruta del logo/icono de marca (opcional)
        """
        ruta_completa = os.path.join(ruta_salida, nombre_archivo)
        
        # Crear canvas con tamaño A4
        c = canvas.Canvas(ruta_completa, pagesize=A4)
        ancho_pagina, alto_pagina = A4
        
        # Dimensiones fijas optimizadas: 7cm x 9cm
        tamaño_talonario_ancho = 7.0 * cm
        tamaño_talonario_alto = 9.0 * cm
        
        # Posición: centrada horizontalmente y verticalmente en la página
        x = (ancho_pagina - tamaño_talonario_ancho) / 2
        y = (alto_pagina - tamaño_talonario_alto) / 2
        
        # Dibujar la ficha
        self._dibujar_talonario(c, x, y, tamaño_talonario_ancho, tamaño_talonario_alto, ruta_logo)
        
        c.save()
        return ruta_completa
    
    def _agregar_logo_en_ficha(self, c, ruta_logo, x, y, ancho, alto):
        """Agrega el logo/icono de marca dentro de la ficha en la parte superior"""
        try:
            # Tamaño del logo proporcional al ancho de la ficha
            tamaño_logo = ancho * 0.35  # 35% del ancho de la ficha
            
            # Posición: esquina superior derecha de la ficha
            x_logo = x + ancho - tamaño_logo - 0.05 * cm
            y_logo = y + alto - tamaño_logo - 0.02 * cm
            
            # Dibujar logo
            c.drawImage(ruta_logo, x_logo, y_logo, width=tamaño_logo, height=tamaño_logo)
        except Exception as e:
            pass  # Silenciosamente ignorar si no hay logo
    
    def _agregar_logo(self, c, ruta_logo, ancho_pagina, alto_pagina):
        """Agrega el logo/icono de marca en la parte superior del PDF"""
        try:
            # Tamaño del logo: 1cm x 1cm
            tamaño_logo = 0.8 * cm
            margen = 0.4 * cm
            
            # Posición: esquina superior derecha
            x_logo = ancho_pagina - tamaño_logo - margen
            y_logo = alto_pagina - tamaño_logo - margen
            
            # Dibujar logo
            c.drawImage(ruta_logo, x_logo, y_logo, width=tamaño_logo, height=tamaño_logo)
        except Exception as e:
            print(f"Error al agregar logo: {e}")
    
    def _dibujar_talonario(self, c, x, y, ancho, alto, ruta_logo=None):
        """Dibuja una ficha de 7x9cm con diseño optimizado y coherente"""
        
        # Borde principal del talonario
        c.setStrokeColor(colors.black)
        c.setLineWidth(1.5)
        c.rect(x, y, ancho, alto)
        
        # Zona superior de "Service" con fondo gris mate
        # Altura fija: 1.3cm para proporciones adecuadas en 7x9cm
        zona_servicio_alto = 1.3 * cm
        c.setFillColor(colors.HexColor('#333333'))
        c.rect(x, y + alto - zona_servicio_alto, ancho, zona_servicio_alto, fill=1, stroke=0)
        
        # Línea divisoria de la zona de service
        c.setStrokeColor(colors.HexColor('#333333'))
        c.setLineWidth(0.5)
        c.line(x, y + alto - zona_servicio_alto, x + ancho, y + alto - zona_servicio_alto)
        
        # Tamaño del logo: igual a la altura del header (coincide perfectamente)
        tamaño_logo = zona_servicio_alto - 0.05 * cm  # 1.25cm
        
        # Dibujar el título "Service" - 14pt para mejor presencia
        tamaño_fuente_titulo = 14
        c.setFont("Helvetica-Bold", tamaño_fuente_titulo)
        c.setFillColor(colors.white)
        # Posicionar "Service" a la izquierda en el header
        x_texto = x + 0.25 * cm
        y_texto = y + alto - zona_servicio_alto + 0.42 * cm
        c.drawString(x_texto, y_texto, "Service")
        
        # Agregar fondo negro mate cuadrado para el logo (integrado en el header)
        if ruta_logo and os.path.exists(ruta_logo):
            try:
                # Posición del fondo del logo: esquina superior derecha, dentro del header
                # Margen mínimo desde el borde
                x_logo_bg = x + ancho - tamaño_logo - 0.02 * cm
                y_logo_bg = y + alto - tamaño_logo - 0.02 * cm
                
                # Dibujar fondo con el mismo color que el header
                c.setFillColor(colors.HexColor('#333333'))
                c.rect(x_logo_bg, y_logo_bg, tamaño_logo, tamaño_logo, fill=1, stroke=0)
                
                # Dibujar logo encima del fondo (centrado en el cuadrado)
                # Reducir ligeramente el logo dentro del fondo para margen interno
                tamaño_logo_interno = tamaño_logo * 0.85
                offset_interno = (tamaño_logo - tamaño_logo_interno) / 2
                c.drawImage(ruta_logo, 
                           x_logo_bg + offset_interno, 
                           y_logo_bg + offset_interno, 
                           width=tamaño_logo_interno, 
                           height=tamaño_logo_interno)
            except Exception as e:
                pass
        
        # Área de contenido: todo lo que queda bajo el header
        y_actual = y + alto - zona_servicio_alto
        espaciado_superior = 0.25 * cm
        y_actual -= espaciado_superior
        
        # Altura de línea: reducida para acomodar más items
        altura_linea = 0.60 * cm
        
        # Tamaños de fuente ajustados para mejor legibilidad sin cortes
        tamaño_fuente_checkbox = 9
        tamaño_fuente_texto = 8.5
        
        # Dibujar items (excluyendo el título)
        item_inicio = 1  # Saltar el primer item (título "Servicio")
        for i, item in enumerate(self.items[item_inicio:]):
            # Verificar si hay espacio
            if y_actual - altura_linea < y + 0.20 * cm:
                break
            
            if item['tipo'] == 'checkbox':
                # Checkbox con tamaño fijo: 0.25cm x 0.25cm
                c.setStrokeColor(colors.black)
                c.setLineWidth(0.7)
                checkbox_size = 0.25 * cm
                checkbox_x = x + 0.20 * cm
                checkbox_y = y_actual - 0.55 * cm
                c.rect(checkbox_x, checkbox_y, checkbox_size, checkbox_size)
                
                # Texto al lado del checkbox
                c.setFont("Courier-Bold", tamaño_fuente_checkbox)
                c.setFillColor(colors.HexColor('#1a1a1a'))
                text_x = checkbox_x + checkbox_size + 0.15 * cm
                text_y = y_actual - 0.38 * cm
                # Calcular el espacio disponible para el texto
                ancho_disponible = x + ancho - text_x - 0.20 * cm
                # Mostrar más caracteres: aproximadamente 22-24 caracteres caben sin corte
                max_chars = 24
                texto_truncado = item['valor'][:max_chars]
                c.drawString(text_x, text_y, texto_truncado)
            
            elif item['tipo'] == 'texto':
                # Texto simple (para Fecha y KM)
                c.setFont("Courier-Bold", tamaño_fuente_texto)
                c.setFillColor(colors.HexColor('#1a1a1a'))
                text_x = x + 0.20 * cm
                text_y = y_actual - 0.38 * cm
                # Calcular el espacio disponible para el texto
                ancho_disponible = x + ancho - text_x - 0.20 * cm
                # Mostrar más caracteres: aproximadamente 33-35 caracteres caben sin corte
                max_chars = 35
                texto_truncado = item['valor'][:max_chars]
                c.drawString(text_x, text_y, texto_truncado)
            
            y_actual -= altura_linea
        
        # Línea horizontal divisoria al final
        c.setStrokeColor(colors.black)
        c.setLineWidth(0.7)
        c.line(x + 0.15 * cm, y + 0.15 * cm, x + ancho - 0.15 * cm, y + 0.15 * cm)


# Ejemplo de uso
if __name__ == "__main__":
    # Crear generador
    talonario = TalonarioServicio5x5(titulo="TALONARIO SERVICIO")
    
    # Opcionalmente agregar items adicionales
    # talonario.agregar_item('checkbox', 'Revisión general')
    # talonario.agregar_item('checkbox', 'Ajustes varios')
    
    # Generar PDF
    ruta_salida = r"c:\Users\dell\Desktop\talonario taller"
    ruta_logo = os.path.join(ruta_salida, 'app_icon-removebg-preview.png')
    
    os.makedirs(ruta_salida, exist_ok=True)
    
    archivo = talonario.generar_pdf(
        nombre_archivo="talonario_5x5.pdf",
        ruta_salida=ruta_salida,
        ruta_logo=ruta_logo
    )
    
    print(f"✓ Talonario optimizado (3x5) generado exitosamente en: {archivo}")
