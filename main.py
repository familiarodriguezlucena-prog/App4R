import streamlit as st
import urllib.parse

# =====================================================================
# 1. CONFIGURACIÓN DE LA PÁGINA E IDENTIDAD VISUAL (PREMIUM DARK)
# =====================================================================
st.set_page_config(
    page_title="Cuatro R | Gourmet Experience",
    page_icon="🥟",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilos CSS avanzados para inyectar una experiencia de usuario única
st.markdown("""
    <style>
    /* Fondo general y fuentes */
    .stApp {
        background-color: #0d1117;
    }
    h1, h2, h3 {
        color: #ffffff !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Contenedor de producto estilo Tarjeta Premium */
    .product-card {
        background: linear-gradient(145deg, #161b22, #0f141c);
        border: 1px solid #30363d;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 25px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.2);
        transition: transform 0.3s ease;
    }
    
    /* Badge de precio flotante */
    .price-badge {
        background-color: #1f6feb;
        color: white;
        padding: 6px 12px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 16px;
        display: inline-block;
    }
    
    /* Botones Premium */
    div.stButton > button {
        border-radius: 12px;
        font-weight: 700;
        background: linear-gradient(90deg, #ff4b4b, #ff7676);
        color: white !important;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.3);
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 75, 75, 0.5);
    }
    </style>
    """, unsafe_allowed_html=True)

# =====================================================================
# 2. SISTEMA DE DATOS Y ESTADO DE LA APLICACIÓN (SESSION STATE)
# =====================================================================
# Base de datos adaptativa en memoria (Precios, Stock y Disponibilidad)
if 'productos' not in st.session_state:
    st.session_state.productos = {
        "Chilenas Especiales": {
            "precio": 1.50,
            "descripcion": "Empanadas gourmet fritas a la perfección, masa crujiente y relleno abundante de carne sazonada al estilo tradicional.",
            "imagen": "https://images.unsplash.com/photo-1608039829572-78524f79c4c7?w=800",
            "stock": 50,
            "disponible": True
        },
        "Tequeños Full Relleno": {
            "precio": 3.00,
            "descripcion": "Pasapalos premium con masa artesanal fina y un centro de queso llanero extra grande que se estira en cada bocado.",
            "imagen": "https://images.unsplash.com/photo-1541532713592-79a0317b6b77?w=800",
            "stock": 80,
            "disponible": True
        }
    }

if 'carrito' not in st.session_state:
    st.session_state.carrito = {}

# Datos fijos de contacto y pago (Centralizados)
TELEFONO_WHATSAPP = "584123856184"  # Formato internacional sin el '+'
DATOS_PAGO = """
🏦 **DATOS DE PAGO MÓVIL:**
- **Banco:** Bancamiga (0172)
- **Cédula / RIF:** J-123456789
- **Teléfono:** 0412-3856184
"""

# =====================================================================
# 3. CABECERA CORPORATIVA DE LA APP
# =====================================================================
st.title("🥟 Grupo Gastronómico Cuatro R")
st.markdown("##### *Alta Gastronomía Artesanal · Fabricantes Especializados*")
st.caption("📍 Barquisimeto, Edo. Lara | Pedidos en línea con despacho inmediato")

# =====================================================================
# 4. NAVEGACIÓN PREMIUM POR PESTAÑAS (TABS)
# =====================================================================
tab_menu, tab_checkout, tab_control = st.tabs([
    "✨ MENÚ EXCLUSIVO", 
    "🛒 MI COMPRA", 
    "🛡️ PANEL ADMINISTRATIVO"
])

# ---------------------------------------------------------------------
# PESTAÑA 1: EL MENÚ INTERACTIVO CAUTIVADOR
# ---------------------------------------------------------------------
with tab_menu:
    st.write("")
    st.markdown("### Selecciona tus productos favoritos:")
    
    for nombre, info in st.session_state.productos.items():
        if info["disponible"]:
            # Renderizado en tarjetas limpias contenedoras
            with st.container():
                st.markdown(f'<div class="product-card">', unsafe_allowed_html=True)
                
                # Imagen del producto optimizada para pantallas móviles
                st.image(info["imagen"], use_container_width=True)
                
                # Detalles de producto y precio alineados de forma limpia
                col_detalles, col_precio = st.columns([3, 1])
                with col_detalles:
                    st.subheader(nombre)
                    st.write(info["descripcion"])
                    st.caption(f"📦 Unidades disponibles en planta: {info['stock']}")
                with col_precio:
                    st.markdown(f'<span class="price-badge">${info["precio"]:.2f}</span>', unsafe_allowed_html=True)
                
                # Selector de cantidades nativo (Protección total contra TypeErrors)
                col_vacia, col_selector = st.columns([2, 2])
                with col_selector:
                    cantidad = st.number_input(
                        f"Cantidad para {nombre}", 
                        min_value=0, 
                        max_value=info["stock"], 
                        step=1, 
                        key=f"input_{nombre}"
                    )
                    
                    if st.button(f"Agregar {nombre}", key=f"btn_{nombre}", use_container_width=True):
                        if cantidad > 0:
                            st.session_state.carrito[nombre] = cantidad
                            st.toast(f"✨ ¡{cantidad} {nombre} añadidos al carrito!", icon="🛒")
                        else:
                            st.session_state.carrito.pop(nombre, None)
                
                st.markdown('</div>', unsafe_allowed_html=True)
                st.write("")

# ---------------------------------------------------------------------
# PESTAÑA 2: CARRO DE COMPRAS E INTEGRACIÓN DE COMPROBANTE
# ---------------------------------------------------------------------
with tab_checkout:
    st.write("")
    st.markdown("### 🛒 Resumen de tu Pedido")
    
    if not st.session_state.carrito:
        st.info("Tu carrito está vacío. Explora el menú y añade algunos productos para empezar.")
    else:
        total_general = 0.0
        lineas_pedido_wa = []
        
        # Tabla estructurada de compra
        for prod_name, cant in list(st.session_state.carrito.items()):
            if cant == 0:
                continue
            precio_unitario = st.session_state.productos[prod_name]["precio"]
            subtotal = cant * precio_unitario
            total_general += subtotal
            
            # Formateo visual del item seleccionado
            col_i, col_c, col_s = st.columns([2, 1, 1])
            with col_i:
                st.write(f"**{prod_name}**")
            with col_c:
                st.write(f"x{cant}")
            with col_s:
                st.write(f"${subtotal:.2f}")
            
            # Guardar el texto formateado para WhatsApp
            lineas_pedido_wa.append(f"- {prod_name} (x{cant}) -> Subtotal: ${subtotal:.2f}")
            
        st.divider()
        st.markdown(f"## Total Neto: ${total_general:.2f}")
        
        st.write("")
        st.info("Completa tu Pago Móvil usando los datos a continuación y adjunta tu capture para validar la orden en cocina.")
        
        # Desplegable elegante con datos de pago
        with st.expander("💳 Ver Datos de Pago de la Empresa", expanded=True):
            st.markdown(DATOS_PAGO)
            
        # INNOVACIÓN: Entrada nativa para captura de pantalla del pago
        soporte_pago = st.file_uploader("Adjuntar captura de Pago Móvil (Obligatorio)", type=["jpg", "png", "jpeg"])
        
        nombre_cliente = st.text_input("Tu Nombre y Apellido:")
        direccion_entrega = st.text_area("Dirección detallada de entrega (o indicar si retira en planta):")
        
        # Botón de validación y despacho hacia WhatsApp
        if st.button("🚀 Confirmar y Enviar Pedido vía WhatsApp", use_container_width=True):
            if not nombre_cliente or not direccion_entrega:
                st.error("Por favor, ingresa tu nombre y dirección de despacho para poder procesar la entrega.")
            elif not soporte_pago:
                st.warning("Para asegurar la validación inmediata de tu orden en administración, sub
