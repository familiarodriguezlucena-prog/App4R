import streamlit as st

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Grupo Gastronómico Cuatro R",
    page_icon="🥟",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. INICIALIZACIÓN DE VARIABLES DE ESTADO
if 'cart' not in st.session_state:
    st.session_state.cart = {}
if 'stock_chilenas' not in st.session_state:
    st.session_state.stock_chilenas = 50

# TÍTULO DE LA APP
st.title("🥟 Cuatro R · Menú")
st.caption("Fabricantes Especializados | Alta Gastronomía")

# 3. ESTRUCTURA DE PESTAÑAS NATIVAS
tab1, tab2 = st.tabs(["🔥 MENÚ INTERACTIVO", "⚙️ ADMINISTRACIÓN"])

with tab1:
    st.write("")
    
    # --- PRODUCTO 1: CHILENAS ESPECIALES ---
    with st.container(border=True):
        st.image("https://images.unsplash.com/photo-1608039829572-78524f79c4c7?w=500", use_container_width=True)
        st.subheader("Chilenas Especiales")
        st.write("Empanadas fritas a la perfección. Relleno rico y abundante por dentro.")
        
        # Fila de precio y stock
        col_p1, col_s1 = st.columns(2)
        with col_p1:
            st.metric(label="PRECIO / UND.", value="$ 1.50")
        with col_s1:
            st.write(f"📦 **Disponibles:** {st.session_state.stock_chilenas}")
        
        # Controles de cantidad
        col_less, col_qty, col_more = st.columns([1, 2, 1])
        current_chilenas = st.session_state.cart.get('Chilenas', 0)
        
        with col_less:
            if st.button("—", key="less_c", use_container_width=True) and current_chilenas > 0:
                st.session_state.cart['Chilenas'] -= 1
                if st.session_state.cart['Chilenas'] == 0:
                    del st.session_state.cart['Chilenas']
                st.rerun()
        with col_qty:
            st.markdown(f"<h3 style='text-align: center; margin: 0;'>{current_chilenas}</h3>", unsafe_allowed_html=True)
        with col_more:
            if st.button("+", key="more_c", use_container_width=True) and current_chilenas < st.session_state.stock_chilenas:
                st.session_state.cart['Chilenas'] = current_chilenas + 1
                st.rerun()

    st.write("")

    # --- PRODUCTO 2: TEQUEÑOS PREMIUM ---
    with st.container(border=True):
        st.image("https://images.unsplash.com/photo-1541532713592-79a0317b6b77?w=500", use_container_width=True)
        st.subheader("Tequeños Full Relleno")
        st.write("Masa artesanal rellena generosamente. Receta clásica hecha con amor.")
        
        st.metric(label="PRECIO / UND.", value="$ 3.00")
        
        if st.button("Agregar al Pedido +", key="add_t", use_container_width=True):
            st.session_state.cart['Tequeños'] = st.session_state.cart.get('Tequeños', 0) + 1
            st.toast("Tequeños agregados al carrito 🥟")

    # --- TOTALIZADOR Y RESUMEN DEL PEDIDO ---
    total_items = sum(st.session_state.cart.values())
    total_price = (st.session_state.cart.get('Tequeños', 0) * 3.00) + (st.session_state.cart.get('Chilenas', 0) * 1.50)
    
    if total_items > 0:
        st.write("")
        st.divider()
        st.subheader(f"🛒 Tu Pedido ({total_items} und.)")
        
        for prod, qty in st.session_state.cart.items():
            st.write(f"• **{prod}** x{qty}")
        
        st.header(f"Total: ${total_price:.2f}")
        
        # Datos de pago fijos
        with st.expander("💳 Ver datos de Pago Móvil"):
            st.write("**Bancamiga**")
            st.write("RIF: J-123456789")
            st.write("Tlf: 0412-3856184")
        
        if st.button("💬 Enviar pedido por WhatsApp", use_container_width=True, type="primary"):
            st.success("Abriendo WhatsApp...")

    st.write("")
    st.caption("© 2026 GRUPO GASTRONÓMICO CUATRO R — FABRICANTES ESPECIALIZADOS")

with tab2:
    st.write("")
    st.subheader("🔐 Acceso Administrativo")
    password = st.text_input("Introduce la clave", type="password", key="admin_p")
    if password == "4R2026":
        st.success("Acceso concedido")
        st.session_state.stock_chilenas = st.number_input("Modificar stock de Chilenas", value=st.session_state.stock_chilenas, min_value=0)
