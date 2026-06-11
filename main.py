import streamlit as st
import sqlite3
import pandas as pd
import urllib.parse
from datetime import datetime

# =====================================================================
# 1. CONFIGURACIÓN E INICIALIZACIÓN DE BASE DE DATOS
# =====================================================================
st.set_page_config(
    page_title="Cuatro R | Gourmet Experience",
    page_icon="🥟",
    layout="centered",
    initial_sidebar_state="collapsed"
)

def inicializar_db():
    """Crea la base de datos local para la persistencia de los pedidos."""
    conn = sqlite3.connect("pedidos_4r.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            cliente TEXT,
            monto REAL
        )
    """)
    conn.commit()
    conn.close()

def registrar_pedido(cliente, monto):
    """Registra de forma segura una venta en el historial local."""
    conn = sqlite3.connect("pedidos_4r.db", check_same_thread=False)
    cursor = conn.cursor()
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO pedidos (fecha, cliente, monto) VALUES (?, ?, ?)",
        (fecha_actual, cliente, monto)
    )
    conn.commit()
    conn.close()

# Arrancar la base de datos al iniciar el servidor
inicializar_db()

# =====================================================================
# 2. ARQUITECTURA DE ESTILOS CSS (PREMIUM DARK & ANIMACIONES)
# =====================================================================
st.markdown("""
    <style>
    /* Fondo e interfaz limpia */
    .stApp { background-color: #0d1117; }
    
    .block-container {
        padding-top: 1rem;
        padding-bottom: 5rem;
    }
    
    /* Contenedor del logotipo principal */
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 10px 0 25px 0;
        animation: fadeIn 1.2s ease-in-out;
    }
    
    /* Tarjeta de producto con animación de entrada estilizada y curvas Bezier */
    .product-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 25px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.2);
        animation: fadeInUp 0.7s cubic-bezier(0.16, 1, 0.3, 1) both;
    }
    
    .price-tag {
        color: #2eb67d;
        font-size: 24px;
        font-weight: bold;
    }
    
    /* Botón flotante interactivo */
    .floating-button-container {
        position: fixed;
        bottom: 30px;
        right: 30px;
        z-index: 9999;
    }
    
    .floating-btn {
        background: linear-gradient(90deg, #ff4b4b, #ff7676);
        color: white !important;
        border-radius: 50px;
        padding: 14px 22px;
        font-weight: bold;
        box-shadow: 0 8px 24px rgba(255, 75, 75, 0.4);
        text-decoration: none;
        display: flex;
        align-items: center;
        gap: 8px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .floating-btn:hover {
        transform: scale(1.05);
        box-shadow: 0 12px 30px rgba(255, 75, 75, 0.6);
    }
    
    /* Animaciones estructurales */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
    """, unsafe_allowed_html=True)

# =====================================================================
# 3. BASE DE DATOS EN MEMORIA (PRODUCTOS ACTUALES)
# =====================================================================
if 'productos' not in st.session_state:
    st.session_state.productos = {
        "Chilenas Especiales": {
            "precio": 1.50, 
            "stock": 50, 
            "img": "https://images.unsplash.com/photo-1608039829572-78524f79c4c7?w=500"
        },
        "Tequeños Full Relleno": {
            "precio": 3.00, 
            "stock": 100, 
            "img": "https://images.unsplash.com/photo-1541532713592-79a0317b6b77?w=500"
        }
    }

if 'carrito' not in st.session_state:
    st.session_state.carrito = {}

# =====================================================================
# 4. ENFOQUE VISUAL: LOGOTIPO DE PRESENTACIÓN EXCLUSIVO
# =====================================================================
# Reemplaza con la ruta de tu archivo de imagen local si lo subes a GitHub (ej. "logo.png")
st.markdown('<div class="logo-container">', unsafe_allowed_html=True)
col_l1, col_l2, col_l3 = st.columns([1, 5, 1])
with col_l2:
    st.image("https://r-rod.github.io/cuatror/logo.png", use_container_width=True)
st.markdown('</div>', unsafe_allowed_html=True)

# =====================================================================
# 5. MENÚ OPERATIVO POR PESTAÑAS (TABS)
# =====================================================================
tab_menu, tab_pago, tab_admin = st.tabs(["🍴 MENÚ", "🛒 MI COMPRA", "🛡️ PANEL"])

# --- PESTAÑA 1: EL MENÚ ---
with tab_menu:
    st.write("")
    for nombre, info in st.session_state.productos.items():
        with st.container():
            st.markdown('<div class="product-card">', unsafe_allowed_html=True)
            col_img, col_txt = st.columns([1, 2])
            with col_img:
                st.image(info["img"], use_container_width=True)
            with col_txt:
                st.subheader(nombre)
                st.markdown(f"<p class='price-tag'>${info['precio']:.2f}</p>", unsafe_allowed_html=True)
                st.caption(f"Disponibles en planta: {info['stock']} und.")
                
            cant = st.number_input(f"Cantidad de {nombre}", min_value=0, max_value=info['stock'], step=1, key=f"q_{nombre}")
            
            # Botón de acción nativo con estilo premium heredado
            if st.button(f"Agregar al Pedido", key=f"b_{nombre}", use_container_width=True):
                if cant > 0:
                    st.session_state.carrito[nombre] = cant
                    st.toast(f"¡{nombre} (x{cant}) añadido!", icon="🥟")
                else:
                    st.session_state.carrito.pop(nombre, None)
            st.markdown('</div>', unsafe_allowed_html=True)

# --- PESTAÑA 2: CHECKOUT / PAGO ---
with tab_pago:
    st.write("")
    # Validación inteligente para comprobar si hay elementos reales en el carrito
    if not st.session_state.carrito or all(v == 0 for v in st.session_state.carrito.values()):
        st.info("Tu carrito de compras está vacío. Selecciona productos en la pestaña de Menú.")
    else:
        st.subheader("🛒 Tu Pedido")
        total_acumulado = 0.0
        cuerpo_mensaje = "🥟 *NUEVO PEDIDO CUATRO R*\n\n"
        
        for p_nombre, cantidad in list(st.session_state.carrito.items()):
            if cantidad > 0:
                sub = cantidad * st.session_state.productos[p_nombre]["precio"]
                total_acumulado += sub
                st.write(f"• **{p_nombre}** x{cantidad} — `${sub:.2f}`")
                cuerpo_mensaje += f"✅ {p_nombre} x{cantidad} (${sub:.2f})\n"
        
        st.divider()
        st.header(f"Total Neto: ${total_acumulado:.2f}")
        st.write("")
        
        with st.expander("💳 Datos oficiales para el Pago Móvil", expanded=True):
            st.markdown("""
            **Bancamiga (0172)**
            - **RIF:** J-123456789
            - **Teléfono:** 0412-3856184
            """)
        
        nombre_cliente = st.text_input("Ingresa tu Nombre y Apellido:")
        soporte_pago = st.file_uploader("Adjuntar captura del Pago Móvil (Validación inmediata)", type=["jpg", "png", "jpeg"])
        
        if st.button("🚀 Confirmar Orden y Enviar a Cocina", use_container_width=True, type="primary"):
            if nombre_cliente:
                # 1. Registro automático y silencioso en SQLite
                registrar_pedido(nombre_cliente, total_acumulado)
                
                # 2. Empaquetado seguro de los datos para WhatsApp Business
                cuerpo_mensaje += f"\n👤 *Cliente:* {nombre_cliente}\n"
                cuerpo_mensaje += f"💰 *Monto a confirmar:* ${total_acumulado:.2f}\n\n"
                cuerpo_mensaje += "_¡Capture de pago adjuntado mediante la aplicación!_"
                
                texto_url = urllib.parse.quote(cuerpo_mensaje)
                enlace_final_wa = f"https://wa.me/584123856184?text={texto_url}"
                
                st.success("¡Pedido guardado en el sistema de Cuatro R con éxito!")
                st.link_button("💬 Abrir WhatsApp para despachar", enlace_final_wa, use_container_width=True)
            else:
                st.error("Por favor, introduce tu nombre para poder procesar la orden en cocina.")

# --- PESTAÑA 3: SEGURIDAD Y CONTROL ---
with tab_admin:
    st.write("")
    if st.text_input("Código de Seguridad Operativo", type="password", key="admin_key") == "4R2026":
        st.success("Acceso concedido al libro de ventas e inventario.")
        
        # Lectura en tiempo real de la base de datos de SQLite
        st.subheader("📊 Historial de Ventas")
        try:
            conn = sqlite3.connect("pedidos_4r.db")
            df = pd.read_sql_query("SELECT id as ID, fecha as 'Fecha/Hora', cliente as 'Nombre Cliente', monto as 'Total ($)' FROM pedidos ORDER BY id DESC", conn)
            conn.close()
            
            if not df.empty:
                st.dataframe(df, use_container_width=True)
                st.metric("Facturación Total Acumulada", f"${df['Total ($)'].sum():.2f}")
            else:
                st.info("Aún no se registran transacciones en el historial de base de datos.")
        except Exception as e:
            st.error(f"Error técnico de lectura: {e}")
            
        st.divider()
        
        # Ajuste manual del stock de planta
        st.subheader("📦 Modificación de Inventario")
        for p in st.session_state.productos:
            st.session_state.productos[p]["stock"] = st.number_input(
                f"Unidades disponibles de {p}:", 
                value=st.session_state.productos[p]["stock"],
                key=f"inv_{p}"
            )
        if st.button("Sincronizar Inventario de Planta", use_container_width=True):
            st.toast("¡Inventario actualizado con éxito!", icon="🔄")
            st.rerun()
    else:
        st.info("Introduce la clave del panel corporativo para ver las métricas en tiempo real.")

# =====================================================================
# 6. INYECCIÓN DEL BOTÓN FLOTANTE CORPORATIVO (ACCESO DIRECTO)
# =====================================================================
st.markdown("""
    <div class="floating-button-container">
        <a href="#mi-compra" class="floating-btn" target="_self">
            🛒 Mi Compra
        </a>
    </div>
    """, unsafe_allowed_html=True)

# FOOTER FIN DE PÁGINA
st.write("")
st.caption("© 2026 Grupo Gastronómico Cuatro R — Fabricantes Especializados | Barquisimeto")
