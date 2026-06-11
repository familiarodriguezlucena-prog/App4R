import streamlit as st
import urllib.parse
import pandas as pd

# 1. CONFIGURACIÓN DE LA PÁGINA (Estilo Premium)
st.set_page_config(
    page_title="Grupo Gastronómico Cuatro R", 
    page_icon="🥟", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. BASE DE DATOS EN MEMORIA (Estado de la Sesión)
# Datos iniciales del negocio por si se reinicia la app
if 'config_negocio' not in st.session_state:
    st.session_state.config_negocio = {
        "telefono": "584123856184",
        "pago_movil": "Bancamiga: RIF J-123456789, Tel: 0412-3856184",
        "logo_url": "https://i.ibb.co/6R0H63C/Logo-4R.png",
        "fondo_premium": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=1200"
    }

if 'productos' not in st.session_state:
    st.session_state.productos = {
        "Tequeños Full Relleno": {"precio": 3.00, "stock": 50, "foto": "https://images.unsplash.com/photo-1541532713592-79a0317b6b77?w=500", "desc": "Masa artesanal y relleno generoso."},
        "Chilenas Especiales": {"precio": 1.50, "stock": 30, "foto": "https://images.unsplash.com/photo-1600891964599-f61ba0e24092?w=500", "desc": "Sabor tradicional con receta premium."},
        "Empanadas Criollas": {"precio": 1.75, "stock": 25, "foto": "https://images.unsplash.com/photo-1555243833-c440d5c6f18f?w=500", "desc": "Masa perfecta con sazón de la casa."}
    }

if 'carrito' not in st.session_state:
    st.session_state.carrito = {}

if 'historial_ventas' not in st.session_state:
    st.session_state.historial_ventas = []

# 3. ESTILOS CSS INMERSIVOS (Look Cinematográfico y Móvil)
st.markdown(f"""
    <style>
    .stApp {{
        background-color: #0d0e12;
        color: #f3f4f6;
    }}
    .logo-container {{
        text-align: center;
        padding: 20px 10px;
    }}
    .logo-img {{
        max-width: 150px;
        border-radius: 50%;
        box-shadow: 0 0 30px rgba(230, 57, 70, 0.3);
        animation: pulse 3s infinite alternate;
    }}
    .product-card {{
        padding: 20px;
        border-radius: 20px;
        background: linear-gradient(145deg, #161920, #0f1115);
        border: 1px solid #232733;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        margin-bottom: 20px;
        animation: fadeInUp 0.8s ease;
    }}
    .product-title {{ font-size: 20px; font-weight: 700; color: #ffffff; margin-top: 10px; }}
    .product-price {{ font-size: 18px; color: #e63946; font-weight: 800; }}
    .stock-badge {{ font-size: 12px; color: #94a3b8; background: #1e293b; padding: 3px 8px; border-radius: 6px; display: inline-block; margin-bottom: 10px; }}
    
    .stButton>button {{
        background: linear-gradient(90deg, #e63946, #b11e2b);
        color: white !important;
        border-radius: 12px;
        border: none;
        padding: 10px;
        font-weight: bold;
        width: 100%;
    }}
    
    @keyframes pulse {{
        from {{ transform: scale(1); box-shadow: 0 0 20px rgba(230, 57, 70, 0.2); }}
        to {{ transform: scale(1.04); box-shadow: 0 0 35px rgba(230, 57, 70, 0.5); }}
    }}
    @keyframes fadeInUp {{
        from {{ opacity: 0; transform: translateY(15px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    </style>
    """, unsafe_allow_html=True)

# 4. SISTEMA DE PESTAÑAS (Menú Principal vs Panel de Administración)
tab_menu, tab_admin = st.tabs(["🔥 MENÚ INTERACTIVO", "⚙️ PANEL DE ADMINISTRACIÓN"])

# =========================================================
# PESTAÑA 1: VISTA DEL CLIENTE (MENÚ INTERACTIVO)
# =========================================================
with tab_menu:
    # Encabezado con Logo Dinámico
    st.markdown(f"""
        <div class="logo-container">
            <img class="logo-img" src="{st.session_state.config_negocio['logo_url']}" alt="Logo 4R">
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<h4 style='text-align: center; color: #94a3b8;'>Artesanal · Generoso · Premium</h4><br>", unsafe_allow_html=True)
    
    # Renderizar catálogo dinámicamente desde la "Base de Datos"
    items = list(st.session_state.productos.items())
    for i in range(0, len(items), 2):
        col1, col2 = st.columns(2)
        
        # Producto 1 de la fila
        name1, data1 = items[i]
        with col1:
            st.markdown('<div class="product-card">', unsafe_allow_html=True)
            st.image(data1["foto"], use_container_width=True)
            st.markdown(f'<div class="product-title">{name1}</div>', unsafe_allow_html=True)
            st.write(f"_{data1['desc']}_")
            st.markdown(f'<div class="product-price">${data1["precio"]:.2f}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="stock-badge">Disponibles: {data1["stock"]}</div>', unsafe_allow_html=True)
            
            if data1["stock"] > 0:
                if st.button("Agregar +", key=f"add_{name1}"):
                    st.session_state.carrito[name1] = st.session_state.carrito.get(name1, 0) + 1
                    st.session_state.productos[name1]["stock"] -= 1
                    st.rerun()
            else:
                st.error("Agotado temporalmente")
            st.markdown('</div>', unsafe_allow_html=True)
            
        # Producto 2 de la fila (si existe)
        if i + 1 < len(items):
            name2, data2 = items[i+1]
            with col2:
                st.markdown('<div class="product-card">', unsafe_allow_html=True)
                st.image(data2["foto"], use_container_width=True)
                st.markdown(f'<div class="product-title">{name2}</div>', unsafe_allow_html=True)
                st.write(f"_{data2['desc']}_")
                st.markdown(f'<div class="product-price">${data2["precio"]:.2f}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="stock-badge">Disponibles: {data2["stock"]}</div>', unsafe_allow_html=True)
                
                if data2["stock"] > 0:
                    if st.button("Agregar +", key=f"add_{name2}"):
                        st.session_state.carrito[name2] = st.session_state.carrito.get(name2, 0) + 1
                        st.session_state.productos[name2]["stock"] -= 1
                        st.rerun()
                else:
                    st.error("Agotado temporalmente")
                st.markdown('</div>', unsafe_allow_html=True)

    # El Carrito de Compras
    if st.session_state.carrito:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.subheader("🛒 Tu Pedido")
        texto_wa = "¡Hola, *Grupo Gastronómico 4R*! 🥟 Quisiera ordenar:\n\n"
        total = 0.0
        
        for prod, cant in st.session_state.carrito.items():
            sub = st.session_state.productos[prod]["precio"] * cant
            total += sub
            st.write(f"🔹 **{prod}** x{cant} — ${sub:.2f}")
            texto_wa += f"• {prod} x{cant} (${sub:.2f})\n"
            
        st.markdown(f"### **Total: ${total:.2f}**")
        st.info(f"💳 **Datos de Pago:** {st.session_state.config_negocio['pago_movil']}")
        
        texto_wa += f"\n💰 *Total Neto: ${total:.2f}*\n\n¿Me confirman disponibilidad para proceder al pago?"
        link_wa = f"https://wa.me/{st.session_state.config_negocio['telefono']}?text={urllib.parse.quote(texto_wa)}"
        
        st.markdown(f"""
            <a href="{link_wa}" target="_blank" style="text-decoration: none;">
                <div style="background-color: #25D366; color: white; text-align: center; padding: 15px; border-radius: 12px; font-weight: bold; font-size: 18px;">
                    💬 Enviar Pedido y Pagar
                </div>
            </a>
        """, unsafe_allow_html=True)
        
        st.write("")
        if st.button("Vaciar Lista 🗑️"):
            for p, c in st.session_state.carrito.items():
                st.session_state.productos[p]["stock"] += c
            st.session_state.carrito = {}
            st.rerun()

# =========================================================
# PESTAÑA 2: PANEL DE ADMINISTRACIÓN (EXCLUSIVO GERENCIA)
# =========================================================
with tab_admin:
    st.subheader("🔑 Acceso Administrativo")
    password = st.text_input("Introduce la clave de acceso para gestionar Cuatro R:", type="password")
    
    if password == "4R2026": # Puedes cambiar esta clave por la que quieras
        st.success("Acceso Concedido")
        
        admin_opcion = st.selectbox("¿Qué deseas gestionar hoy?", ["Modificar Precios/Stock", "Agregar Nuevo Producto", "Datos de Contacto y Pago", "Cierre de Caja / Lógica de Negocio"])
        
        # --- MODIFICAR PRODUCTOS EXISTENTES ---
        if admin_opcion == "Modificar Precios/Stock":
            st.markdown("### Ajuste de Inventario Activo")
            for prod, datos in st.session_state.productos.items():
                st.write(f"#### 📦 {prod}")
                col_p, col_s = st.columns(2)
                with col_p:
                    nuevo_precio = st.number_input(f"Precio de {prod} ($)", min_value=0.0, value=datos["precio"], key=f"price_in_{prod}")
                    st.session_state.productos[prod]["precio"] = nuevo_precio
                with col_s:
                    nuevo_stock = st.number_input(f"Stock Disponible de {prod}", min_value=0, value=datos["stock"], key=f"stock_in_{prod}")
                    st.session_state.productos[prod]["stock"] = nuevo_stock
            if st.button("Guardar Cambios de Inventario"):
                st.success("¡Precios y existencias actualizados con éxito!")
                st.rerun()
                
        # --- AGREGAR NUEVOS PRODUCTOS ---
        elif admin_opcion == "Agregar Nuevo Producto":
            st.markdown("### Introducir un nuevo producto al catálogo")
            nuevo_nombre = st.text_input("Nombre del producto (Ej: Combo Teque-Salsa)")
            nuevo_p = st.number_input("Precio de venta ($)", min_value=0.0, value=1.0)
            nuevo_st = st.number_input("Cantidad inicial en inventario", min_value=0, value=10)
            nueva_desc = st.text_input("Descripción breve (Relleno, estilo de masa...)")
            nueva_foto = st.text_input("Enlace URL de la foto", value="https://images.unsplash.com/photo-1541532713592-79a0317b6b77?w=500")
            
            if st.button("Dar de Alta Producto"):
                if nuevo_nombre:
                    st.session_state.productos[nuevo_nombre] = {
                        "precio": nuevo_p,
                        "stock": nuevo_st,
                        "foto": nueva_foto,
                        "desc": nueva_desc
                    }
                    st.success(f"¡{nuevo_nombre} se ha añadido al menú!")
                    st.rerun()
                else:
                    st.error("El nombre del producto es obligatorio")

        # --- DATOS DEL NEGOCIO ---
        elif admin_opcion == "Datos de Contacto y Pago":
            st.markdown("### Modificar Canales Oficiales")
            nuevo_tel = st.text_input("WhatsApp del negocio (Formato internacional, ej: 584123856184):", value=st.session_state.config_negocio["telefono"])
            nuevos_datos_pago = st.text_area("Datos para Pago Móvil o Transferencia:", value=st.session_state.config_negocio["pago_movil"])
            nuevo_logo = st.text_input("URL del Logotipo oficial de la marca:", value=st.session_state.config_negocio["logo_url"])
            
            if st.button("Actualizar Canales"):
                st.session_state.config_negocio["telefono"] = nuevo_tel
                st.session_state.config_negocio["pago_movil"] = nuevos_datos_pago
                st.session_state.config_negocio["logo_url"] = nuevo_logo
                st.success("Configuración de marca guardada de inmediato")
                st.rerun()

        # --- LOGICA DE NEGOCIO Y HISTORIAL ---
        elif admin_opcion == "Cierre de Caja / Lógica de Negocio":
            st.markdown("### Monitor de Ventas e Indicadores Financieros")
            
            # Simulador de inyección de ventas reales (Lógica de operaciones)
            st.write("Simular un cierre de terminal de punto o pago móvil recibido:")
            col_v1, col_v2 = st.columns(2)
            with col_v1:
                prod_vendido = st.selectbox("Producto despachado:", list(st.session_state.productos.keys()))
            with col_v2:
                cant_vendida = st.number_input("Cantidad despachada:", min_value=1, value=1)
                
            if st.button("Registrar Venta Manual (Cierre POS/Efectivo)"):
                monto_total = st.session_state.productos[prod_vendido]["precio"] * cant_vendida
                st.session_state.historial_ventas.append({
                    "Producto": prod_vendido,
                    "Cantidad": cant_vendida,
                    "Total ($)": monto_total
                })
                st.success("Venta guardada en el historial contable.")
            
            if st.session_state.historial_ventas:
                df_ventas = pd.DataFrame(st.session_state.historial_ventas)
                st.table(df_ventas)
                st.metric("Ingresos Totales Brutos", f"${df_ventas['Total ($)'].sum():.2f}")
                
                if st.button("Limpiar Historial / Iniciar Nueva Jornada"):
                    st.session_state.historial_ventas = []
                    st.rerun()
            else:
                st.info("No hay registros de ventas cargados en la jornada actual.")
                
    elif password != "":
        st.error("Contraseña administrativa incorrecta. Acceso restringido.")
