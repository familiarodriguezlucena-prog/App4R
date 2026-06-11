import streamlit as st

# 1. CONFIGURACIÓN DE LA PÁGINA (Minimalista y Oscura)
st.set_page_config(
    page_title="Grupo Gastronómico Cuatro R",
    page_icon="🥟",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. INYECCIÓN DE CSS LIMPIO (Sin conflictos de llaves en Python)
st.markdown("""
    <style>
    .stApp {
        background-color: #0D0D0D !important;
        color: #FFFFFF !important;
    }
    
    .product-card {
        background: linear-gradient(145deg, #1A1A1A, #121212);
        border-radius: 24px;
        padding: 0px;
        margin-bottom: 25px;
        border: 1px solid #222222;
        overflow: hidden;
        box-shadow: 0 8px 16px rgba(0,0,0,0.5);
    }
    
    .product-info {
        padding: 20px;
    }
    
    .product-title {
        font-size: 22px;
        font-weight: bold;
        color: #FFFFFF;
        margin-bottom: 5px;
    }
    
    .product-description {
        font-size: 14px;
        color: #AAAAAA;
        margin-bottom: 15px;
        line-height: 1.4;
    }
    
    .product-price {
        font-size: 24px;
        font-weight: bold;
        color: #E6C687;
        margin-top: 10px;
    }
    
    .price-label {
        font-size: 10px;
        color: #666666;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .footer-text {
        text-align: center;
        color: #444444;
        font-size: 11px;
        letter-spacing: 1px;
        margin-top: 50px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allowed_html=True)

# 3. INICIALIZACIÓN DE VARIABLES
if 'cart' not in st.session_state:
    st.session_state.cart = {}
if 'stock_chilenas' not in st.session_state:
    st.session_state.stock_chilenas = 50

# 4. ESTRUCTURA PRINCIPAL
tab1, tab2 = st.tabs(["🔥 MENÚ INTERACTIVO", "⚙️ PANEL DE ADMINISTRACIÓN"])

with tab1:
    st.write("")
    
    # Grid para centrar el contenido en pantallas móviles
    _, col_main_center, _ = st.columns([1, 8, 1])
    
    with col_main_center:
        # --- PRODUCTO 1: CHILENAS ESPECIALES ---
        st.markdown("""
            <div class="product-card">
                <img src="https://images.unsplash.com/photo-1608039829572-78524f79c4c7?w=500" style="width:100%; height:220px; object-fit:cover;">
                <div class="product-info">
                    <div class="product-title">Chilenas Especiales</div>
                    <div class="product-description">Empanadas fritas a la perfección. Relleno rico y abundante por dentro.</div>
                    <div class="price-label">PRECIO / UND.</div>
                    <div class="product-price">$ 1.50</div>
                </div>
            </div>
        """, unsafe_allowed_html=True)
        
        # Selectores de cantidad sencillos
        col_less, col_qty, col_more = st.columns([1, 2, 1])
        current_chilenas = st.session_state.cart.get('Chilenas', 0)
        
        with col_less:
            if st.button("—", key="less_c", use_container_width=True) and current_chilenas > 0:
                st.session_state.cart['Chilenas'] -= 1
                if st.session_state.cart['Chilenas'] == 0:
                    del st.session_state.cart['Chilenas']
                st.rerun()
        with col_qty:
            st.markdown(f"<h3 style='text-align: center; margin: 0; color: white;'>{current_chilenas}</h3>", unsafe_allowed_html=True)
        with col_more:
            if st.button("+", key="more_c", use_container_width=True) and current_chilenas < st.session_state.stock_chilenas:
                st.session_state.cart['Chilenas'] = current_chilenas + 1
                st.rerun()

        st.write("")
        st.write("")

        # --- PRODUCTO 2: TEQUEÑOS ---
        st.markdown("""
            <div class="product-card">
                <img src="https://images.unsplash.com/photo-1541532713592-79a0317b6b77?w=500" style="width:100%; height:220px; object-fit:cover;">
                <div class="product-info">
                    <div class="product-title">Tequeños Full Relleno</div>
                    <div class="product-description">Masa artesanal rellena generosamente. Receta clásica hecha con amor.</div>
                    <div class="price-label">PRECIO / UND.</div>
                    <div class="product-price">$ 3.00</div>
                </div>
            </div>
        """, unsafe_allowed_html=True)
        
        if st.button("Agregar al Pedido +", key="add_t", use_container_width=True):
            st.session_state.cart['Tequeños'] = st.session_state.cart.get('Tequeños', 0) + 1
            st.toast("Tequeños agregados 🥟")

        # --- TOTALIZADOR DEL CARRITO ---
        total_items = sum(st.session_state.cart.values())
        total_price = (st.session_state.cart.get('Tequeños', 0) * 3.00) + (st.session_state.cart.get('Chilenas', 0) * 1.50)
        
        if total_items > 0:
            st.markdown("---")
            st.markdown(f"### 🛒 Tu Pedido ({total_items} und.)")
            st.markdown(f"## Total: **${total_price:.2f}**")
            
            if st.button("💬 Enviar por WhatsApp", use_container_width=True, type="primary"):
                st.success("Abriendo WhatsApp...")

        st.markdown('<div class="footer-text">© 2026 GRUPO GASTRONÓMICO CUATRO R —<br>FABRICANTES ESPECIALIZADOS</div>', unsafe_allowed_html=True)

with tab2:
    st.write("")
    st.markdown("### 🔐 Acceso de Administración")
    password = st.text_input("Introduce la clave de acceso", type="password", key="admin_p")
    if password == "4R2026":
        st.success("Acceso concedido")
        st.session_state.stock_chilenas = st.number_input("Existencias de Chilenas", value=st.session_state.stock_chilenas)
