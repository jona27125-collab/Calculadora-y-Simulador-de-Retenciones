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
    .author {
        color: #cbd5e1;
        text-align: right;
        font-size: .85rem;
        line-height: 1.5;
    }
    .top-rule {
        height: 4px;
        border-radius: 10px;
        background: linear-gradient(90deg, #3b82f6, #8b5cf6, #10b981, #f59e0b);
        margin: 16px 0 18px 0;
    }
    .info-card {
        background: #131c31;
        border: 1px solid rgba(148, 163, 184, .18);
        border-radius: 12px;
        padding: 16px;
        height: 100%;
    }
    .info-card h4 {
        color: #38bdf8;
        margin-top: 0;
        margin-bottom: 8px;
        font-size: 1.05rem;
    }
    .info-card p, .info-card li {
        color: #cbd5e1;
        font-size: 0.9rem;
        line-height: 1.45;
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
    tarifa_iva = st.sidebar.selectbox(
        "Tarifa IVA vigente (Art. 65 LRTI)",
        [15.0, 8.0, 5.0, 0.0],
        index=[15.0, 8.0, 5.0, 0.0].index(tarifa_default),
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
        # Cálculo simplificado de tabla progresiva referencial
        if base_imponible <= 11902:
            impuesto_causado = 0.0
        elif base_imponible <= 15159:
            impuesto_causado = (base_imponible - 11902) * 0.05
        elif base_imponible <= 19682:
            impuesto_causado = 163 + (base_imponible - 15159) * 0.10
        elif base_imponible <= 26031:
            impuesto_causado = 615 + (base_imponible - 19682) * 0.12
        elif base_imponible <= 34255:
            impuesto_causado = 1377 + (base_imponible - 26031) * 0.15
        elif base_imponible <= 45407:
            impuesto_causado = 2611 + (base_imponible - 34255) * 0.20
        elif base_imponible <= 60450:
            impuesto_causado = 4841 + (base_imponible - 45407) * 0.25
        elif base_imponible <= 80605:
            impuesto_causado = 8602 + (base_imponible - 60450) * 0.30
        elif base_imponible <= 107199:
            impuesto_causado = 14648 + (base_imponible - 80605) * 0.35
        else:
            impuesto_causado = 23956 + (base_imponible - 107199) * 0.37

        # Rebaja gastos personales (18% según cargas)
        tope_cargas = [7, 9, 11, 14, 17, 20][cargas_familiares] * 795.0
        rebaja_gp = min(impuesto_causado, tope_cargas * 0.18)
        plazo_ir = "MARZO (P. Naturales)"
    else:
        tarifa_ir_texto = "1% - 2% RIMPE"
        base_imponible = ingresos_anuales  # RIMPE grava ingresos brutos
        impuesto_causado = ingresos_anuales * 0.015
        rebaja_gp = 0.0
        plazo_ir = "MARZO / ABRIL"

    ir_pagar = max(0.0, impuesto_causado - rebaja_gp - ret_renta)
    saldo_favor_ir = abs(min(0.0, impuesto_causado - rebaja_gp - ret_renta))


# ------------------------------------------------------------
# FUNCIONES PARA CONSTRUIR EL SVG NEURONAL CON NÚCLEO LRTI
# ------------------------------------------------------------
def money(val):
    return f"${val:,.2f}"

def svg_text(x, y, text, size=11, color="#eaf0ff", weight="600", anchor="middle"):
    return (
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" '
        f'font-family="Inter,Segoe UI,Arial,sans-serif" font-size="{size}" '
        f'font-weight="{weight}" fill="{color}">{html.escape(str(text))}</text>'
    )

def draw_node(x, y, title, pill_val, color, subtitle="", radius=27):
    parts = [
        f'<circle cx="{x}" cy="{y}" r="{radius+6}" fill="{color}" opacity=".12"/>',
        f'<circle cx="{x}" cy="{y}" r="{radius}" fill="#131e36" stroke="{color}" stroke-width="2.4"/>',
    ]
    lines = title.split("|")
    start_y = y - (len(lines) - 1) * 5
    for i, line in enumerate(lines):
        parts.append(svg_text(x, start_y + i * 10 + 3, line, 8.3, "#ffffff", "800"))

    label = str(pill_val)
    pill_w = max(46, min(115, 14 + len(label) * 6.0))
    parts.append(
        f'<rect x="{x - pill_w/2}" y="{y - radius - 18}" width="{pill_w}" height="16" '
        f'rx="8" fill="#fbbf24"/>'
    )
    parts.append(svg_text(x, y - radius - 7, label, 8.8, "#1e1b04", "800"))
    if subtitle:
        parts.append(svg_text(x, y + radius + 14, subtitle, 7.8, "#94a3b8", "500"))
    return "".join(parts)

# Definición de nodos según el módulo activo
if "IVA" in modulo:
    col1_nodes = [
        ("VENTAS|GRAVADAS", money(ventas_mes), "Base imponible ventas"),
        ("COMPRAS|LOCALES/IMP", money(compras_mes), "Adquisiciones con IVA"),
        ("TARIFA|APLICABLE", f"{tarifa_iva:g} %", "15% | 8% | 5% | 0%"),
        ("RETENCIONES|RECIBIDAS", money(ret_iva), "Agentes de retención"),
        ("9.° DÍGITO|DEL RUC", f"Dígito {noveno_digito}", "Calendario SRI"),
    ]
    col2_nodes = [
        ("HECHO|GENERADOR", "Art. 61 LRTI", "Entrega o pago"),
        ("SUJETOS|PASIVOS", "Art. 63 LRTI", "Percepción / Retención"),
