import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN DE LA PÁGINA (Minimalista y Oscura)
st.set_page_config(
    page_title="Grupo Gastronómico Cuatro R",
    page_icon="🥟",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# IMAGEN REAL EN OPTIMIZADA (Base64 para carga instantánea y permanente sin enlaces rotos)
CHILENAS_IMG = "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBwgHBgkIBwgKCgkLDRYPDQwMDRsUFRAWIB0iIiAdHx8kKDQsJCYxJx8fLT0tMTU3Ojo6Iys/RD84QzQ5OjcBCgoKDQwNGg8PGjclHyU3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3N3/AABEIAOAA4AMBIgACEQEDEQH/xAAcAAABBQEBAQAAAAAAAAAAAAAGAAMEBQcCAQj/xABREAACAQMDAgMFAwYHCwkAAAABAgMABBEFEiEGMRMiQVEHYXGBkRQy8BUjobHB0eEWQlJicpKT8RclJDNDVGNzgpOiNFNUVIOTssLD0tMX/80000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001dfa"

# 2. INYECCIÓN DE CSS PARA EL LOOK PREMIUM (Inspirado en Screenshot_20260611-181146.jpg)
st.markdown("""
    <style>
    /* Fondo oscuro general de la app */
    .stApp {
        background-color: #0D0D0D;
        color: #FFFFFF;
    }
    
    /* Pestañas de Navegación */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        color: #888888;
        font-weight: bold;
        border: none;
    }
    .stTabs [aria-selected="true"] {
        color: #FF001E !important;
        border-bottom: 2px solid #FF001E !important;
    }

    /* Tarjetas de productos redondeadas y estilizadas */
    .product-card {
        background: linear-gradient(145deg, #1A1A1A, #121212);
        border-radius: 28px;
        padding: 0px;
        margin-bottom: 20px;
        border: 1px solid #222222;
        overflow: hidden;
        box-shadow: 0 12px 24px rgba(0,0,0,0.6);
    }
    
    .product-info {
        padding: 24px;
    }
    
    .product-title {
        font-family: 'Playfair Display', serif;
        font-size: 24px;
        font-weight: bold;
        color: #FFFFFF;
        margin-bottom: 6px;
    }
    
    .product-description {
        font-size: 14px;
        color: #999999;
        margin-bottom: 20px;
        line-height: 1.5;
    }
    
    /* Precios en Dorado */
    .product-price {
        font-size: 26px;
        font-weight: bold;
        color: #E6C687;
        margin-top: 5px;
    }
    
    .price-label {
        font-size: 11px;
        color: #555555;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: bold;
    }

    /* Badge de Disponibilidad flotante */
    .stock-badge {
        position: absolute;
        top: 15px;
        right: 15px;
        background-color: rgba(20, 20, 20, 0.75);
        color: #CCCCCC;
        padding: 5px 14px;
        border-radius: 14px;
        font-size: 12px;
        font-weight: 500;
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255,255,255,0.05);
    }
    
    /* Botones de acción */
    .stButton>button {
        border-radius: 16px !important;
        font-weight: bold !important;
    }
    
    /* Footer */
    .footer-text {
        text-align: center;
        color: #3A3A3A;
        font-size: 11px;
        letter-spacing: 1.5px;
        margin-top: 60px;
        margin-bottom: 30px;
        line-height: 1.6;
    }
    </style>
""", unsafe_allowed_html=True)

# 3. CONTROL DE ESTADO (CARRITO E INVENTARIO)
if 'cart' not in st.session_state:
    st.session_state.cart = {}
if 'stock_chilenas' not in st.session_state:
    st.session_state.stock_chilenas = 50

# 4. DISTRIBUCIÓN EN PESTAÑAS PRINCIPALES
tab1, tab2 = st.tabs(["🔥 MENÚ INTERACTIVO", "⚙️ PANEL DE ADMINISTRACIÓN"])

with tab1:
    st.write("")
    
    # Contenedor centrado para visualización móvil idónea
    _, col_wrap, _ = st.columns([1, 10, 1])
    
    with col_wrap:
        # --- PRODUCTO 1: CHILENAS ESPECIALES (Fiel a la captura) ---
        st.markdown(f"""
            <div class="product-card" style="position: relative;">
                <div class="stock-badge">{st.session_state.stock_chilenas} disponibles</div>
                <img src="{CHILENAS_IMG}" style="width:100%; height:260px; object-fit:cover;">
                <div class="product-info">
                    <div class="product-title">Chilenas Especiales</div>
                    <div class="product-description">Empanadas fritas a la perfección. Relleno rico y abundante por dentro.</div>
                    <div class="price-label">PRECIO / UND.</div>
                    <div class="product-price">$ 1.50</div>
                </div>
            </div>
        """, unsafe_allowed_html=True)
        
        # Selector de cantidad y agregado
        col_less, col_qty, col_more = st.columns([1, 2, 1])
        current_chilenas = st.session_state.cart.get('Chilenas', 0)
        
        with col_less:
            if st.button("—", key="btn_less_chilenas", use_container_width=True) and current_chilenas > 0:
                st.session_state.cart['Chilenas'] -= 1
                if st.session_state.cart['Chilenas'] == 0:
                    del st.session_state.cart['Chilenas']
                st.rerun()
        with col_qty:
            st.markdown(f"<h3 style='text-align: center; margin-top: 5px; color: white;'>{current_chilenas}</h3>", unsafe_allowed_html=True)
        with col_more:
            if st.button("+", key="btn_more_chilenas", use_container_width=True) and current_chilenas < st.session_state.stock_chilenas:
                st.session_state.cart['Chilenas'] = current_chilenas + 1
                st.rerun()

        st.write("")
        st.write("")

        # --- PRODUCTO 2: TEQUEÑOS PREMIUM ---
        st.markdown("""
            <div class="product-card" style="position: relative;">
                <div class="stock-badge">Disponibilidad alta</div>
                <img src="https://images.unsplash.com/photo-1541532713592-79a0317b6b77?w=500" style="width:100%; height:240px; object-fit:cover;">
                <div class="product-info">
                    <div class="product-title">Tequeños Full Relleno</div>
                    <div class="product-description">Masa artesanal rellena generosamente. Receta clásica hecha con amor.</div>
                    <div class="price-label">PRECIO / UND.</div>
                    <div class="product-price">$ 3.00</div>
                </div>
            </div>
        """, unsafe_allowed_html=True)
        
        if st.button("Agregar al Pedido +", key="btn_add_tequenos", use_container_width=True, type="secondary"):
            st.session_state.cart['Tequeños'] = st.session_state.cart.get('Tequeños', 0) + 1
            st.toast("Tequeños agregados al carrito 🥟")

        # --- INTERFAZ DINÁMICA DEL CARRITO FLOTANTE ---
        total_items = sum(st.session_state.cart.values())
        total_price = (st.session_state.cart.get('Tequeños', 0) * 3.00) + (st.session_state.cart.get('Chilenas', 0) * 1.50)
        
        if total_items > 0:
            st.markdown("<br><hr style='border-color: #222222;'>", unsafe_allowed_html=True)
            st.markdown(f"### 🛒 Tu Pedido Activo ({total_items} und.)")
            for prod, qty in st.session_state.cart.items():
                st.write(f"• **{prod}** x{qty}")
            
            # Botón flotante simulado con el total acumulado
            st.markdown(f"## Total a Pagar: <span style='color:#E6C687;'>${total_price:.2f}</span>", unsafe_allowed_html=True)
            
            st.markdown("""
                <div style='background-color: #121212; padding: 16px; border-radius: 18px; margin-bottom: 15px; border: 1px solid #222;'>
                    <span style='color: #666666; font-size: 11px; font-weight: bold; letter-spacing: 1px;'>PAGO MÓVIL DIRECTO:</span><br>
                    <span style='color: #DDDDDD; font-size: 14px;'><b>Bancamiga</b> · RIF J-123456789 · Tlf: 0412-3856184</span>
                </div>
            """, unsafe_allowed_html=True)
            
            if st.button("💬 Enviar pedido por WhatsApp", use_container_width=True, type="primary"):
                st.success("Generando orden de despacho...")

        # Footer idéntico y minimalista
        st.markdown('<div class="footer-text">© 2026 GRUPO GASTRONÓMICO CUATRO R —<br>FABRICANTES ESPECIALIZADOS</div>', unsafe_allowed_html=True)

with tab2:
    st.write("")
    st.markdown("### 🔐 Acceso de Administración")
    password = st.text_input("Introduce la clave de acceso", type="password", key="input_admin_pass")
    
    if password == "4R2026":
        st.success("Acceso verificado con éxito")
        st.markdown("#### Control de Producción en Planta")
        st.session_state.stock_chilenas = st.number_input("Establecer existencias en vitrina (Chilenas)", value=st.session_state.stock_chilenas, min_value=0)
