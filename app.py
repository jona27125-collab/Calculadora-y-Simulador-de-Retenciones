import pandas as pd
import plotly.express as px
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Simulador de Retenciones SRI - Ecuador",
    page_icon="🧾",
    layout="wide",
)

# --- CRÉDITO OBLIGATORIO ---
DEVELOPER_NAME = "Estefany Remache"

# Estilo visual personalizado (CSS limpio)
st.markdown(
    """
    <style>
    .main-header { font-size: 2.2rem; color: #1f77b4; font-weight: 700; }
    .credit-tag { background-color: #f0f2f6; padding: 10px 15px; border-radius: 8px; font-weight: 600; color: #333; border-left: 5px solid #1f77b4; }
    </style>
""",
    unsafe_allow_html=True,
)

# Encabezado principal
st.markdown(
    '<p class="main-header">Calculadora & Simulador de Retenciones SRI 🇪🇨</p>',
    unsafe_allow_html=True,
)
st.markdown(
    f'<div class="credit-tag">Desarrollado por {DEVELOPER_NAME}</div>',
    unsafe_allow_html=True,
)
st.markdown("<br>", unsafe_allow_html=True)

# --- BARRA LATERAL ---
st.sidebar.markdown(
    f"### ⚙️ Parámetros de Retención\n**Desarrollado por {DEVELOPER_NAME}**"
)
st.sidebar.markdown("---")

tipo_contribuyente_comprador = st.sidebar.selectbox(
    "Condición del Agente de Retención (Comprador):",
    [
        "Sociedad / Empresa Ordinaria",
        "Contribuyente Especial",
        "Entidad del Sector Público",
        "Persona Natural Obligada a Llevar Contabilidad",
    ],
)

iva_vigente = (
    st.sidebar.number_input("Tarifa IVA Vigente (%)", value=15.0, step=1.0) / 100.0
)

# --- CUERPO PRINCIPAL / CALCULADORA ---
st.subheader("💼 Datos de la Transacción Comercial")

col1, col2 = st.columns(2)

with col1:
    base_imponible = st.number_input(
        "Monto Base Imponible (USD sin IVA):",
        min_value=0.0,
        value=1000.0,
        step=50.0,
    )
    aplica_iva = st.checkbox("¿La transacción grava IVA?", value=True)

with col2:
    concepto_retencion = st.selectbox(
        "Concepto de Retención en la Renta:",
        [
            (
                "Honorarios profesionales y servicios con predominio intelectual"
                " (8%)"
            ),
            "Servicios en los que prevalece la mano de obra (2%)",
            "Compraventa de bienes muebles de naturaleza corporal (1%)",
            "Arrendamiento de bienes inmuebles (8%)",
            (
                "Servicios prestados por medios de comunicación y agencias de"
                " publicidad (1%)"
            ),
            "Otras compras de bienes o servicios no especificados (2%)",
        ],
    )

# Lógica de porcentajes de Renta e IVA según normativa SRI
if "8%" in concepto_retencion:
    porcentaje_renta = 0.08
    porcentaje_iva_ret = (
        1.00  # 100% de retención de IVA para servicios profesionales
    )
elif "mano de obra" in concepto_retencion or "especificados" in concepto_retencion:
    porcentaje_renta = 0.02
    porcentaje_iva_ret = 0.70  # 70% de retención de servicios habituales
elif "bienes muebles" in concepto_retencion:
    porcentaje_renta = 0.01
    porcentaje_iva_ret = 0.30  # 30% de retención de bienes
elif "Arrendamiento" in concepto_retencion:
    porcentaje_renta = 0.08
    porcentaje_iva_ret = 1.00
elif "publicidad" in concepto_retencion:
    porcentaje_renta = 0.01
    porcentaje_iva_ret = 0.70
else:
    porcentaje_renta = 0.02
    porcentaje_iva_ret = 0.30

# Cálculos matemáticos
monto_iva = base_imponible * iva_vigente if aplica_iva else 0.0
valor_retenido_renta = base_imponible * porcentaje_renta
valor_retenido_iva = monto_iva * porcentaje_iva_ret if aplica_iva else 0.0

total_a_pagar = (base_imponible + monto_iva) - (
    valor_retenido_renta + valor_retenido_iva
)

st.markdown("---")
st.subheader("📊 Resultados del Cálculo y Liquidación")

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("Subtotal Base", f"${base_imponible:,.2f}")
with m2:
    st.metric(f"IVA ({int(iva_vigente*100)}%)", f"${monto_iva:,.2f}")
with m3:
    st.metric(
        "Total Retenciones",
        f"${(valor_retenido_renta + valor_retenido_iva):,.2f}",
    )
with m4:
    st.metric(
        "Total Líquido a Pagar",
        f"${total_a_pagar:,.2f}",
        delta="Neto proveedor",
    )

st.markdown("<br>", unsafe_allow_html=True)

# Detalle de Retenciones
col_d1, col_d2 = st.columns(2)

with col_d1:
    st.info(
        f"**Retención en la Fuente de Impuesto a la Renta:**\n- Porcentaje"
        f" aplicado: `{porcentaje_renta*100}%`\n- Valor Retenido:"
        f" **${valor_retenido_renta:,.2f}**"
    )

with col_d2:
    st.info(
        f"**Retención de IVA:**\n- Porcentaje de retención sobre IVA:"
        f" `{porcentaje_iva_ret*100}%`\n- Valor Retenido de IVA:"
        f" **${valor_retenido_iva:,.2f}**"
    )

# Tabla resumen ejecutiva para comprobante de retención
st.markdown(
    "### 📄 Comprobante de Retención Electrónico (Simulación de Emisión)"
)

df_comprobante = pd.DataFrame(
    {
        "Impuesto": ["Impuesto a la Renta", "IVA"],
        "Base Imponible": [
            base_imponible,
            monto_iva if aplica_iva else 0.0,
        ],
        "Porcentaje Retención": [
            f"{porcentaje_renta*100}%",
            f"{porcentaje_iva_ret*100}% (del IVA)",
        ],
        "Valor Retenido (USD)": [valor_retenido_renta, valor_retenido_iva],
    }
)

st.dataframe(df_comprobante, use_container_width=True)

st.markdown("---")
st.markdown(
    f"<p style='text-align: center; color: gray;'>Simulador Tributario Oficial"
    f" • Desarrollado por {DEVELOPER_NAME}</p>",
    unsafe_allow_html=True,
)
