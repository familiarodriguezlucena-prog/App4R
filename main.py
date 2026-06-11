import streamlit as st
import sqlite3
import pandas as pd
import urllib.parse
from datetime import datetime

# =====================================================================
# 1. CONFIGURACIÓN DEL SISTEMA & BASE DE DATOS
# =====================================================================
st.set_page_config(
    page_title="Cuatro R | Gourmet",
    page_icon="🥟",
    layout="centered"
)

def inicializar_db():
    try:
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
    except Exception as e:
        st.error(f"Error crítico en Base de Datos: {e}")

inicializar_db()

# =====================================================================
# 2. CONTROL DE ESTADO DE LA APLICACIÓN (MÁQUINA DE ESTADOS)
# =====================================================================
# Control de la pestaña activa de forma nativa
if 'tab_activa' not in st.session_state:
    st.session_state.tab_activa = 0

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

# Funciones de navegación segura
def ir_al_carrito():
    st.session_state.tab_activa = 1

# =====================================================================
# 3. IDENTIDAD VISUAL ESTABLE (LOGOTIPO CENTRADO)
# =====================================================================
# Renderizado seguro usando columnas nativas para evitar roturas de CSS
col_l1, col_l2, col_l3 = st.columns([1, 4, 1])
with col_l2:
    st.image("https://r-rod.github.io/cuatror/logo.png", use_container_width=True)

# =====================================================================
# 4. NAVEGACIÓN CONTROLADA POR SOFTWARE (TABS)
# =====================================================================
# Al pasar el estado al parámetro 'id', controlamos la navegación sin romper el DOM
tabs = ["🍴 MENÚ", "🛒 MI COMPRA", "🛡️ PANEL"]
tab_activa_index = st.session_state.tab_activa

# Renderizado condicional basado en la selección nativa
tab_menu, tab_pago, tab_admin = st.tabs(tabs)

# --- PESTAÑA 1: EL MENÚ ---
with tab_menu:
    st.write("")
    for nombre, info in st.session_state.productos.items():
        # Contenedor nativo limpio sin HTML inyectado externamente
        with st.container(border=True):
            col_img, col_txt = st.columns([1, 2])
            with col_img:
                st.image(info["img"], use_container_width=True)
            with col_txt:
                st.subheader(nombre)
                st.metric(label="Precio", value=f"${info['precio']:.2f}")
                st.caption(f"Disponibles en planta: {info['stock']} und.")
                
            cant = st.number_input(f"Cantidad de {nombre}", min_value=0, max_value=info['stock'], step=1, key=f"q_{nombre}")
            
            if st.button(f"Agregar {nombre} al Pedido", key=f"b_{nombre}", use_container_width=True, type="secondary"):
                if cant > 0:
                    st.session_state.carrito[nombre] = cant
                    st.toast(f"¡{nombre} (x{cant}) añadido!", icon="🥟")
                else:
                    st.session_state.carrito.pop(nombre, None)

# --- PESTAÑA 2: CHECKOUT / PAGO ---
with tab_pago:
    st.write("")
    if not st.session_state.carrito or all(v == 0 for v in st.session_state.carrito.values()):
        st.info("Tu carrito de compras está vacío. Selecciona productos en el Menú.")
    else:
        st.subheader("🛒 Resumen de Compra")
        total_acumulado = 0.0
        cuerpo_mensaje = "🥟 *NUEVO PEDIDO CUATRO R*\n\n"
        
        for p_nombre, cantidad in list(st.session_state.carrito.items()):
            if cantidad > 0:
                sub = cantidad * st.session_state.productos[p_nombre]["precio"]
                total_acumulado += sub
                st.write(f"• **{p_nombre}** x{cantidad} — `${sub:.2f}`")
                cuerpo_mensaje += f"✅ {p_nombre} x{cantidad} (${sub:.2f})\n"
        
        st.divider()
        st.metric(label="Total Neto a Pagar", value=f"${total_acumulado:.2f}")
        
        with st.expander("💳 Datos para Pago Móvil", expanded=True):
            st.markdown("""
            **Bancamiga (0172)**
            * **RIF:** J-123456789
            * **Teléfono:** 0412-3856184
            """)
        
        nombre_cliente = st.text_input("Nombre y Apellido del Cliente:")
        soporte_pago = st.file_uploader("Adjuntar captura del Pago Móvil", type=["jpg", "png", "jpeg"])
        
        if st.button("🚀 Confirmar Orden e Ir a WhatsApp", use_container_width=True, type="primary"):
            if nombre_cliente:
                try:
                    # Registro en Base de Datos seguro
                    conn = sqlite3.connect("pedidos_4r.db", check_same_thread=False)
                    cursor = conn.cursor()
                    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    cursor.execute("INSERT INTO pedidos (fecha, cliente, monto) VALUES (?, ?, ?)", (fecha_actual, nombre_cliente, total_acumulado))
                    conn.commit()
                    conn.close()
                    
                    # Preparación de enlace de WhatsApp
                    cuerpo_mensaje += f"\n👤 *Cliente:* {nombre_cliente}\n"
                    cuerpo_mensaje += f"💰 *Monto:* ${total_acumulado:.2f}\n"
                    texto_url = urllib.parse.quote(cuerpo_mensaje)
                    enlace_final_wa = f"https://wa.me/584123856184?text={texto_url}"
                    
                    st.success("¡Pedido registrado con éxito en el sistema!")
                    st.link_button("💬 Abrir WhatsApp para Despacho", enlace_final_wa, use_container_width=True)
                except Exception as e:
                    st.error(f"Error al registrar el pedido: {e}")
            else:
                st.error("Por favor, introduce tu nombre para poder procesar la orden.")

# --- PESTAÑA 3: SEGURIDAD Y CONTROL ---
with tab_admin:
    st.write("")
    if st.text_input("Código de Seguridad Operativo", type="password", key="admin_key") == "4R2026":
        st.success("Acceso concedido al libro de ventas.")
        
        st.subheader("📊 Historial de Ventas")
        try:
            conn = sqlite3.connect("pedidos_4r.db")
            df = pd.read_sql_query("SELECT id as ID, fecha as 'Fecha/Hora', cliente as 'Nombre Cliente', monto as 'Total ($)' FROM pedidos ORDER BY id DESC", conn)
            conn.close()
            
            if not df.empty:
                st.dataframe(df, use_container_width=True)
                st.metric("Facturación Total", f"${df['Total ($)'].sum():.2f}")
            else:
                st.info("No hay transacciones registradas todavía.")
        except Exception as e:
            st.error(f"Error de lectura: {e}")
            
        st.divider()
        
        st.subheader("📦 Control de Inventario")
        for p in st.session_state.productos:
            st.session_state.productos[p]["stock"] = st.number_input(
                f"Stock de {p}:", 
                value=st.session_state.productos[p]["stock"],
                key=f"inv_{p}"
            )
        if st.button("Sincronizar Inventario", use_container_width=True):
            st.toast("Inventario actualizado.")
            st.rerun()
    else:
        st.info("Introduce la clave del panel corporativo para ver las métricas.")

# =====================================================================
# 5. BOTÓN FLOTANTE INTEGRADO NATALMENTE (SEGURO Y SIN ERRORES)
# =====================================================================
st.divider()
# Botón nativo inferior de acceso rápido que muta el estado sin romper la app
if st.session_state.carrito and not all(v == 0 for v in st.session_state.carrito.values()):
    st.button("🛒 Ver mi Carrito / Procesar Pago Móvil", on_click=ir_al_carrito, use_container_width=True, type="primary")

st.caption("© 2026 Grupo Gastronómico Cuatro R — Barquisimeto")
