import html
import streamlit as st
import streamlit.components.v1 as components

# ------------------------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# ------------------------------------------------------------
st.set_page_config(
    page_title="Red Neuronal Tributaria - LRTI y SRI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

DEVELOPER_NAME = "Jonathan Toasa"

# ------------------------------------------------------------
# ESTILOS CSS
# ------------------------------------------------------------
st.markdown("""
<style>
    .stApp {
        background: #090e1c;
        color: #e8eefc;
    }
    [data-testid="stSidebar"] {
        background: #0f172a;
        border-right: 1px solid rgba(148, 163, 184, .16);
    }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #eaf0ff;
    }
    .main-title {
        color: #f3f6ff;
        font-size: clamp(1.55rem, 2.8vw, 2.3rem);
        font-weight: 800;
        line-height: 1.15;
        margin: 0;
    }
    .sub-title {
        color: #94a3b8;
        font-size: 0.98rem;
        margin-top: 6px;
        margin-bottom: 0;
    }
    .result-strip {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 12px;
        margin-top: 12px;
        margin-bottom: 18px;
    }
    .result-box {
        background: #131c31;
        border: 1px solid rgba(148,163,184,.22);
        border-radius: 11px;
        padding: 14px;
    }
    .result-label {
        color: #94a3b8;
        font-size: .75rem;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: .5px;
    }
    .result-value {
        color: #f8fafc;
        font-size: 1.25rem;
        font-weight: 800;
        margin-top: 4px;
    }
    .footnote {
        color: #64748b;
        text-align: center;
        font-size: .78rem;
        margin-top: 22px;
    }
    @media (max-width: 750px) {
        .result-strip { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# PANEL DE CONTROL INTERACTIVO (SIDEBAR)
# ------------------------------------------------------------
st.sidebar.markdown("## 🧠 Centro de Control LRTI")
modulo = st.sidebar.radio(
    "Selecciona el impuesto a procesar en la red:",
    [
        "🔵 Impuesto al Valor Agregado (IVA)",
        "🟣 Impuesto a la Renta (IR)",
    ],
)

st.sidebar.markdown("---")

if "IVA" in modulo:
    st.sidebar.markdown("### 📥 Parámetros IVA (Título II LRTI)")
    escenario_iva = st.sidebar.selectbox(
        "Cargar caso rápido:",
        [
            "Tarifa General (15%)",
            "Servicios Turísticos Feriado (8%)",
            "Construcción Vivienda Social (5%)",
            "Bienes de Primera Necesidad (0%)",
        ],
    )
    tarifa_map = {
        "Tarifa General (15%)": 15.0,
        "Servicios Turísticos Feriado (8%)": 8.0,
        "Construcción Vivienda Social (5%)": 5.0,
        "Bienes de Primera Necesidad (0%)": 0.0,
    }
    tarifa_default = tarifa_map[escenario_iva]

    ventas_mes = st.sidebar.number_input(
        "Ventas gravadas del mes (USD sin IVA)", min_value=0.0, value=12000.0, step=500.0
    )
    compras_mes = st.sidebar.number_input(
        "Compras con derecho a crédito (USD sin IVA)", min_value=0.0, value=7500.0, step=500.0
    )
    tarifas_opciones = [15.0, 8.0, 5.0, 0.0]
    tarifa_iva = st.sidebar.selectbox(
        "Tarifa IVA vigente (Art. 65 LRTI)",
        tarifas_opciones,
        index=tarifas_opciones.index(tarifa_default),
        format_func=lambda x: f"{x:g} %",
    )
    ret_iva = st.sidebar.number_input(
        "Retenciones de IVA recibidas (USD)", min_value=0.0, value=360.0, step=50.0
    )
    noveno_digito = st.sidebar.slider("9.° dígito del RUC (Plazo SRI)", 1, 9, 4)

    # Cálculos IVA según LRTI
    iva_ventas = ventas_mes * (tarifa_iva / 100.0)
    credito_tributario = compras_mes * (tarifa_iva / 100.0)
    saldo_iva = iva_ventas - credito_tributario - ret_iva
    iva_pagar = max(0.0, saldo_iva)
    credito_favor = abs(min(0.0, saldo_iva))
    dia_vencimiento = 10 + (noveno_digito - 1) * 2

else:
    st.sidebar.markdown("### 📥 Parámetros Renta (Título I LRTI)")
    tipo_sujeto = st.sidebar.selectbox(
        "Sujeto Pasivo (Art. 4 LRTI):",
        [
            "Sociedad (Tarifa General 25%)",
            "Persona Natural (Tabla Progresiva 0% - 37%)",
            "RIMPE Emprendedor (1% - 2%)",
        ],
    )
    ingresos_anuales = st.sidebar.number_input(
        "Ingresos gravados anuales (USD)", min_value=0.0, value=150000.0, step=5000.0
    )
    gastos_deducibles = st.sidebar.number_input(
        "Costos y gastos deducibles (Art. 10 LRTI)", min_value=0.0, value=95000.0, step=5000.0
    )
    ret_renta = st.sidebar.number_input(
        "Retenciones en la fuente recibidas (USD)", min_value=0.0, value=2500.0, step=100.0
    )
    cargas_familiares = st.sidebar.slider(
        "Cargas familiares (Persona Natural)", 0, 5, 0
    )

    # Cálculos Impuesto a la Renta según LRTI
    base_imponible = max(0.0, ingresos_anuales - gastos_deducibles)

    if "Sociedad" in tipo_sujeto:
        tarifa_ir_texto = "25 % (Art. 37)"
        impuesto_causado = base_imponible * 0.25
        rebaja_gp = 0.0
        plazo_ir = "ABRIL (Sociedades)"
    elif "Persona Natural" in tipo_sujeto:
        tarifa_ir_texto = "0% a 37% (Art. 36)"
        if base_imponible <= 12208:
            impuesto_causado = 0.0
        elif base_imponible <= 15549:
            impuesto_causado = (base_imponible - 12208) * 0.05
        elif base_imponible <= 20188:
            impuesto_causado = 167 + (base_imponible - 15549) * 0.10
        elif base_imponible <= 26700:
            impuesto_causado = 631 + (base_imponible - 20188) * 0.12
        elif base_imponible <= 35136:
            impuesto_causado = 1412 + (base_imponible - 26700) * 0.15
        elif base_imponible <= 46575:
            impuesto_causado = 2678 + (base_imponible - 35136) * 0.20
        elif base_imponible <= 62005:
            impuesto_causado = 4965 + (base_imponible - 46575) * 0.25
        elif base_imponible <= 82679:
            impuesto_causado = 8823 + (base_imponible - 62005) * 0.30
        elif base_imponible <= 109956:
            impuesto_causado = 15025 + (base_imponible - 82679) * 0.35
        else:
            impuesto_causado = 24572 + (base_imponible - 109956) * 0.37

        limites_cargas = [5565.0, 7155.0, 8745.0, 11130.0, 13515.0, 15900.0]
        tope_cargas = limites_cargas[cargas_familiares]
        rebaja_gp = min(impuesto_causado, tope_cargas * 0.18)
        plazo_ir = "MARZO (P. Naturales)"
    else:
        tarifa_ir_texto = "1% - 2% RIMPE"
        base_imponible = ingresos_anuales
        impuesto_causado = ingresos_anuales * 0.015
        rebaja_gp = 0.0
        plazo_ir = "MARZO / ABRIL"

    ir_pagar = max(0.0, impuesto_causado - rebaja_gp - ret_renta)
    saldo_favor_ir = abs(min(0.0, impuesto_causado - rebaja_gp - ret_renta))

# ------------------------------------------------------------
# INTERFAZ PRINCIPAL Y RENDERIZADO DE MÉTRICAS
# ------------------------------------------------------------
st.markdown('<p class="main-title">🧠 Red Neuronal Tributaria - Núcleo LRTI</p>', unsafe_allow_html=True)
st.markdown(f'<p class="sub-title">Simulador interactivo basado en la Ley Orgánica de Régimen Tributario Interno y normativas del SRI 2026 | Desarrollado por {DEVELOPER_NAME}</p>', unsafe_allow_html=True)
st.markdown('<div style="height:4px; border-radius:10px; background:linear-gradient(90deg, #3b82f6, #8b5cf6, #10b981, #f59e0b); margin:16px 0 18px 0;"></div>', unsafe_allow_html=True)

if "IVA" in modulo:
    st.markdown("### 📊 Resultados Dinámicos - Impuesto al Valor Agregado (Formulario 104)")
    st.markdown(f"""
    <div class="result-strip">
        <div class="result-box">
            <div class="result-label">IVA Ventas (Débito)</div>
            <div class="result-value">${iva_ventas:,.2f}</div>
        </div>
        <div class="result-box">
            <div class="result-label">Crédito Tributario</div>
            <div class="result-value">${credito_tributario:,.2f}</div>
        </div>
        <div class="result-box">
            <div class="result-label">IVA a Pagar</div>
            <div class="result-value" style="color: #38bdf8;">${iva_pagar:,.2f}</div>
        </div>
        <div class="result-box">
            <div class="result-label">Vencimiento RUC (...{noveno_digito})</div>
            <div class="result-value" style="color: #10b981;">Día {dia_vencimiento} del mes</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("### 📊 Resultados Dinámicos - Impuesto a la Renta (Formularios 101 / 102)")
    st.markdown(f"""
    <div class="result-strip">
        <div class="result-box">
            <div class="result-label">Base Imponible</div>
            <div class="result-value">${base_imponible:,.2f}</div>
        </div>
        <div class="result-box">
            <div class="result-label">Impuesto Causado</div>
            <div class="result-value">${impuesto_causado:,.2f}</div>
        </div>
        <div class="result-box">
            <div class="result-label">Impuesto a Pagar</div>
            <div class="result-value" style="color: #38bdf8;">${ir_pagar:,.2f}</div>
        </div>
        <div class="result-box">
            <div class="result-label">Plazo Declaración</div>
            <div class="result-value" style="color: #f59e0b; font-size: 1.05rem;">{plazo_ir}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown(f'<div class="footnote">Simulación fiscal en tiempo real calculada bajo el marco jurídico ecuatoriano vigente. Creado por {DEVELOPER_NAME}.</div>', unsafe_allow_html=True)
