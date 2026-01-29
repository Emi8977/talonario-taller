// Funciones principales
const app = {
    itemsAdicionales: [],

    init() {
        this.setupEventListeners();
        this.cargarItemsPredeterminados();
        this.cargarArchivos();
    },

    setupEventListeners() {
        document.getElementById('btn-agregar-item').addEventListener('click', () => this.agregarItemAdicional());
        document.getElementById('btn-limpiar-adicionales').addEventListener('click', () => this.limpiarAdicionales());
        document.getElementById('btn-generar-pdf').addEventListener('click', () => this.generarPDF());

        // Permitir agregar item con Enter
        document.getElementById('item-valor').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.agregarItemAdicional();
        });
    },

    async cargarItemsPredeterminados() {
        try {
            const respuesta = await fetch('/api/items-predeterminados');
            const datos = await respuesta.json();

            if (!respuesta.ok) {
                throw new Error(datos.error || 'Error al cargar items');
            }

            const lista = document.getElementById('lista-predeterminados');
            const items = datos.items;

            if (items.length === 0) {
                lista.innerHTML = '<p class="cargando">No hay items predeterminados</p>';
                return;
            }

            lista.innerHTML = items.map(item => {
                let icono = '☐';
                if (item.tipo === 'titulo') icono = '📋';
                else if (item.tipo === 'texto') icono = '📝';

                return `
                    <div class="item-predeterminado">
                        <span class="icono">${icono}</span>
                        <span class="valor">${item.valor}</span>
                    </div>
                `;
            }).join('');

        } catch (error) {
            console.error('Error cargando items:', error);
            document.getElementById('lista-predeterminados').innerHTML = 
                `<p class="error">Error: ${error.message}</p>`;
        }
    },

    agregarItemAdicional() {
        const tipo = document.getElementById('item-tipo').value;
        const valor = document.getElementById('item-valor').value.trim();

        if (!valor) {
            alert('Por favor ingresa un valor');
            return;
        }

        this.itemsAdicionales.push({ tipo, valor });
        this.renderizarAdicionales();

        // Limpiar input
        document.getElementById('item-valor').value = '';
        document.getElementById('item-valor').focus();
    },

    renderizarAdicionales() {
        const lista = document.getElementById('lista-adicionales');
        
        if (this.itemsAdicionales.length === 0) {
            lista.innerHTML = '<p class="cargando">No hay items adicionales</p>';
            return;
        }

        lista.innerHTML = this.itemsAdicionales.map((item, index) => {
            let icono = '☐';
            if (item.tipo === 'texto') icono = '📝';

            return `
                <div class="item-entrada">
                    <div class="item-info">
                        <span class="icono">${icono}</span>
                        <span class="valor">${item.valor}</span>
                    </div>
                    <button class="btn-eliminar" onclick="app.eliminarAdicional(${index})">✕</button>
                </div>
            `;
        }).join('');
    },

    eliminarAdicional(index) {
        this.itemsAdicionales.splice(index, 1);
        this.renderizarAdicionales();
    },

    limpiarAdicionales() {
        if (confirm('¿Estás seguro? Esto eliminará todos los items adicionales')) {
            this.itemsAdicionales = [];
            this.renderizarAdicionales();
        }
    },

    async generarPDF() {
        const btn = document.getElementById('btn-generar-pdf');
        const estado = document.getElementById('estado-generacion');

        try {
            btn.disabled = true;
            estado.className = 'estado-generacion activo cargando';
            estado.innerHTML = '<span class="spinner"></span> Generando PDF...';

            const respuesta = await fetch('/api/generar-talonario', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    items_adicionales: this.itemsAdicionales
                })
            });

            const datos = await respuesta.json();

            if (!respuesta.ok) {
                throw new Error(datos.error || 'Error al generar PDF');
            }

            estado.className = 'estado-generacion activo exito';
            estado.innerHTML = `
                ✓ ${datos.mensaje}
                <br><a href="/api/descargar/${datos.archivo}" class="btn btn-primary" style="margin-top: 10px;">
                    ⬇️ Descargar PDF
                </a>
            `;

            this.cargarArchivos();

        } catch (error) {
            estado.className = 'estado-generacion activo error';
            estado.innerHTML = `✕ Error: ${error.message}`;
        } finally {
            btn.disabled = false;
        }
    },

    async cargarArchivos() {
        try {
            const respuesta = await fetch('/api/listar-archivos');
            const datos = await respuesta.json();

            const lista = document.getElementById('lista-descargas');

            if (datos.archivos.length === 0) {
                lista.innerHTML = '<div class="cargando">No hay archivos generados aún</div>';
                return;
            }

            lista.innerHTML = datos.archivos.map(archivo => `
                <div class="archivo-item">
                    <div class="archivo-info">
                        <div class="archivo-nombre">📄 ${archivo.nombre}</div>
                        <div class="archivo-detalles">${archivo.tamaño} • ${archivo.fecha}</div>
                    </div>
                    <a href="/api/descargar/${archivo.nombre}" class="btn-descargar">
                        ⬇️ Descargar
                    </a>
                </div>
            `).join('');

        } catch (error) {
            console.error('Error cargando archivos:', error);
        }
    }
};

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => app.init());
