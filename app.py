import html
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Red neuronal tributaria | IVA e Impuesto a la Renta",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

DEVELOPER_NAME = "Jonathan Toasa"

# ------------------------- ESTILOS -------------------------
st.markdown("""
<style>
.stApp {
    background: #080f1e;
    color: #e8eefc;
}
.block-container {
    max-width: 1500px;
    padding-top: 1.4rem;
    padding-bottom: 3rem;
}
.main-title {
    color: #f4f7ff;
    font-size: clamp(1.7rem, 3vw, 2.55rem);
    font-weight: 850;
    line-height: 1.15;
    margin: 0;
}
.sub-title {
    color: #9fb1d2;
    font-size: 1rem;
    margin: .55rem 0 1rem;
}
.section-title {
    color: #f2f6ff;
    font-size: 1.35rem;
    font-weight: 800;
    margin: 1.5rem 0 .3rem;
}
div[data-testid="stNumberInput"], div[data-testid="stSelectbox"] {
    background: #111d33;
    border: 1px solid rgba(148,163,184,.18);
    border-radius: 12px;
    padding: 10px 12px 2px;
}
.metric-card {
    background: linear-gradient(145deg,#14233e,#101a2d);
    border: 1px solid rgba(148,163,184,.18);
    border-radius: 14px;
    padding: 15px 17px;
    min-height: 92px;
}
.metric-label {
    color: #9fb1d2;
    font-size: .76rem;
    text-transform: uppercase;
    font-weight: 750;
    letter-spacing: .5px;
}
.metric-value {
    color: #f8faff;
    font-size: 1.35rem;
    font-weight: 850;
    margin-top: 5px;
}
.note {
    color: #91a2c1;
    font-size: .82rem;
}
hr { border-color: rgba(148,163,184,.18); }
</style>
""", unsafe_allow_html=True)

def money(value):
    return f"${value:,.2f}"

# ------------------------- ENCABEZADO -------------------------
st.markdown('<p class="main-title">🧠 Red neuronal tributaria</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="sub-title">Ley Orgánica de Régimen Tributario Interno (LRTI): '
    'explora cómo sus disposiciones se ramifican hacia el IVA y el Impuesto a la Renta.</p>',
    unsafe_allow_html=True,
)

# ------------------------- DATOS INICIALES Y CÁLCULOS -------------------------
# Los valores iniciales son únicamente demostrativos. Se pueden editar debajo del gráfico.
if "ventas_mes" not in st.session_state:
    st.session_state.ventas_mes = 10000.0
if "compras_mes" not in st.session_state:
    st.session_state.compras_mes = 6000.0
if "tipo_tarifa" not in st.session_state:
    st.session_state.tipo_tarifa = 15.0
if "retenciones_recibidas" not in st.session_state:
    st.session_state.retenciones_recibidas = 1290.0
if "ingresos_anual" not in st.session_state:
    st.session_state.ingresos_anual = 200000.0
if "costos_anual" not in st.session_state:
    st.session_state.costos_anual = 160000.0

ventas_mes = st.session_state.ventas_mes
compras_mes = st.session_state.compras_mes
tipo_tarifa = st.session_state.tipo_tarifa
retenciones_recibidas = st.session_state.retenciones_recibidas
ingresos_anual = st.session_state.ingresos_anual
costos_anual = st.session_state.costos_anual

iva_en_ventas = ventas_mes * (tipo_tarifa / 100.0)
credito_tributario = compras_mes * (tipo_tarifa / 100.0)
iva_retenido = retenciones_recibidas * 0.07
iva_pagar_calc = iva_en_ventas - credito_tributario - iva_retenido
iva_a_pagar = max(0.0, iva_pagar_calc)
iva_a_favor = abs(min(0.0, iva_pagar_calc))

base_imponible_renta = max(0.0, ingresos_anual - costos_anual)
impuesto_causado_renta = base_imponible_renta * 0.25
renta_retenida = retenciones_recibidas * 0.90
renta_a_pagar = max(0.0, impuesto_causado_renta - renta_retenida)

# ------------------------- RED NEURONAL INTERACTIVA -------------------------
# Los nodos se pueden pulsar: el panel inferior del gráfico muestra su explicación.
def esc(value):
    return html.escape(str(value), quote=True)

nodes = [
    # Rama IVA - lado izquierdo
    ("iva_entrada", 150, 205, "DATOS IVA", money(ventas_mes), "#438cff",
     "Entradas del IVA", "Ventas y compras del período, tarifa aplicable y retenciones recibidas."),
    ("iva_ley", 390, 205, "LRTI · IVA", "Arts. 52–67", "#a96af5",
     "Marco legal del IVA", "La LRTI regula el objeto, hecho generador, sujetos pasivos, base imponible, tarifas, crédito tributario y declaración del IVA."),
    ("iva_calc", 630, 205, "CÁLCULO IVA", money(iva_en_ventas), "#12c8b5",
     "Procesamiento del IVA", f"IVA generado: {money(iva_en_ventas)}. Crédito estimado: {money(credito_tributario)}. Retención estimada: {money(iva_retenido)}."),
    ("iva_out", 870, 205, "RESULTADO IVA", money(iva_a_pagar), "#ff9b50",
     "Resultado del IVA", f"IVA a pagar: {money(iva_a_pagar)}. Saldo a favor estimado: {money(iva_a_favor)}."),
    # Rama IR - lado derecho
    ("ir_entrada", 1530, 555, "DATOS IR", money(ingresos_anual), "#438cff",
     "Entradas del Impuesto a la Renta", "Ingresos anuales y costos o gastos deducibles declarados para el ejercicio fiscal."),
    ("ir_ley", 1290, 555, "LRTI · RENTA", "Arts. 1–10, 16+", "#a96af5",
     "Marco legal del Impuesto a la Renta", "La LRTI define la renta, sujetos pasivos, ejercicio impositivo, deducciones, base imponible y tarifas aplicables."),
    ("ir_calc", 1050, 555, "CÁLCULO IR", money(base_imponible_renta), "#12c8b5",
     "Procesamiento del Impuesto a la Renta", f"Base imponible simplificada: {money(base_imponible_renta)}. Impuesto causado estimado: {money(impuesto_causado_renta)}."),
    ("ir_out", 810, 555, "RESULTADO IR", money(renta_a_pagar), "#ff9b50",
     "Resultado del Impuesto a la Renta", f"Impuesto a la renta estimado por pagar: {money(renta_a_pagar)}."),
]

# Posiciones adaptadas a un lienzo panorámico; la LRTI es el nodo central.
W, H = 1680, 780
def text_svg(x, y, value, size=13, color="#eaf0ff", weight=600):
    return (f'<text x="{x}" y="{y}" text-anchor="middle" '
            f'font-family="Inter,Segoe UI,Arial,sans-serif" font-size="{size}" '
            f'font-weight="{weight}" fill="{color}">{esc(value)}</text>')

def circle_node(node_data):
    node_id, x, y, title, value, color, heading, detail = node_data
    safe_heading, safe_detail = esc(heading), esc(detail)
    lines = [
        f'<g class="node" tabindex="0" role="button" aria-label="{safe_heading}" '
        f'data-title="{safe_heading}" data-detail="{safe_detail}" data-node="{node_id}" '
        f'style="cursor:pointer">',
        f'<circle cx="{x}" cy="{y}" r="61" fill="{color}" opacity=".10" class="halo"/>',
        f'<circle cx="{x}" cy="{y}" r="49" fill="#14223b" stroke="{color}" stroke-width="2.5"/>',
        f'<circle cx="{x}" cy="{y}" r="39" fill="none" stroke="{color}" stroke-opacity=".28"/>',
        text_svg(x, y-5, title, 11, "#ffffff", 800),
        text_svg(x, y+15, value, 11, color, 800),
        text_svg(x, y+78, heading, 12, "#cbd8f0", 700),
        '<circle cx="0" cy="0" r="0" fill="none"/>',
        '</g>',
    ]
    return "".join(lines)

svg = [f"""
<div id="neural-wrap" style="width:100%;overflow-x:auto;border:1px solid #233653;
     border-radius:22px;background:#0b1528;box-shadow:0 18px 55px rgba(0,0,0,.25)">
<svg id="neural-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}"
     style="display:block;width:100%;min-width:900px;height:auto" aria-label="Red neuronal tributaria interactiva">
<defs>
  <pattern id="grid" width="34" height="34" patternUnits="userSpaceOnUse">
    <path d="M 34 0 L 0 0 0 34" fill="none" stroke="#263958" stroke-width="1" opacity=".55"/>
  </pattern>
  <filter id="glow"><feGaussianBlur stdDeviation="5" result="blur"/>
    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <linearGradient id="centerFill" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#253d70"/><stop offset="1" stop-color="#172344"/>
  </linearGradient>
</defs>
<rect width="{W}" height="{H}" rx="22" fill="#0b1528"/>
<rect width="{W}" height="{H}" rx="22" fill="url(#grid)"/>
"""]

# Encabezados de las dos ramas.
svg += [
    text_svg(420, 55, "RAMA DEL IMPUESTO AL VALOR AGREGADO", 17, "#64a5ff", 850),
    text_svg(1260, 55, "RAMA DEL IMPUESTO A LA RENTA", 17, "#64a5ff", 850),
    '<path d="M80 78 H780" stroke="#438cff" stroke-opacity=".35" stroke-width="1.5"/>',
    '<path d="M900 78 H1600" stroke="#438cff" stroke-opacity=".35" stroke-width="1.5"/>',
]

# Rutas ramificadas desde LRTI a los dos impuestos.
edges = [
    (840, 390, 760, 245, "#438cff"),
    (840, 390, 920, 535, "#a96af5"),
    (150, 205, 390, 205, "#438cff"),
    (390, 205, 630, 205, "#a96af5"),
    (630, 205, 870, 205, "#12c8b5"),
    (1530, 555, 1290, 555, "#438cff"),
    (1290, 555, 1050, 555, "#a96af5"),
    (1050, 555, 810, 555, "#12c8b5"),
]
for x1, y1, x2, y2, color in edges:
    svg.append(
        f'<path class="flow-line" d="M{x1},{y1} C{(x1+x2)/2},{y1} '
        f'{(x1+x2)/2},{y2} {x2},{y2}" fill="none" stroke="{color}" '
        'stroke-width="2.5" stroke-dasharray="8 8" opacity=".75"/>'
    )

# Ramificaciones secundarias desde el nodo central a cada etapa.
svg += [
    '<path d="M840 390 C700 390 700 205 870 205" fill="none" stroke="#438cff" stroke-width="1.6" opacity=".24"/>',
    '<path d="M840 390 C980 390 980 555 810 555" fill="none" stroke="#a96af5" stroke-width="1.6" opacity=".24"/>',
]

# Nodo central LRTI.
svg += [
    '<g id="central-node" class="node central" tabindex="0" role="button" '
    'data-title="Ley Orgánica de Régimen Tributario Interno (LRTI)" '
    'data-detail="La LRTI es el marco legal que organiza las reglas del IVA y del Impuesto a la Renta. Selecciona una rama para explorar sus etapas." style="cursor:pointer">',
    '<circle cx="840" cy="390" r="105" fill="#8b5cf6" opacity=".12" filter="url(#glow)"/>',
    '<circle cx="840" cy="390" r="82" fill="url(#centerFill)" stroke="#b28aff" stroke-width="3"/>',
    '<circle cx="840" cy="390" r="68" fill="none" stroke="#b28aff" stroke-opacity=".45" stroke-width="1.5"/>',
    text_svg(840, 378, "LRTI", 29, "#ffffff", 900),
    text_svg(840, 405, "LEY TRIBUTARIA", 11, "#c4b5fd", 800),
    text_svg(840, 426, "ECUADOR · 2026", 10, "#aebddb", 650),
    '</g>',
]

for nd in nodes:
    svg.append(circle_node(nd))

# Leyenda.
svg += [
    '<circle cx="560" cy="710" r="6" fill="#438cff"/>',
    text_svg(620, 714, "ENTRADAS", 11, "#aebddb", 700),
    '<circle cx="735" cy="710" r="6" fill="#a96af5"/>',
    text_svg(795, 714, "MARCO LEGAL", 11, "#aebddb", 700),
    '<circle cx="930" cy="710" r="6" fill="#12c8b5"/>',
    text_svg(990, 714, "PROCESAMIENTO", 11, "#aebddb", 700),
    '<circle cx="1165" cy="710" r="6" fill="#ff9b50"/>',
    text_svg(1220, 714, "RESULTADOS", 11, "#aebddb", 700),
    '</svg>',
    """
<div id="node-info" style="margin:0 18px 18px;padding:15px 18px;border-radius:13px;
     background:#111f36;border:1px solid #2a3d5d;color:#dce7fb">
  <div id="node-title" style="font-weight:800;color:#c4b5fd;margin-bottom:5px">
    LEY ORGÁNICA DE RÉGIMEN TRIBUTARIO INTERNO
  </div>
  <div id="node-detail" style="font-size:14px;line-height:1.55;color:#b8c7e2">
    Pulsa cualquier nodo de la red para conocer su función y su relación con el proceso tributario.
  </div>
</div>
</div>
<style>
#neural-svg .node {outline:none}
#neural-svg .node:hover circle:first-child,
#neural-svg .node:focus circle:first-child {opacity:.28;filter:url(#glow)}
#neural-svg .node.selected circle:nth-child(2) {stroke-width:4;filter:url(#glow)}
#neural-svg .flow-line {animation:flow 5s linear infinite}
@keyframes flow {to {stroke-dashoffset:-64}}
@media (prefers-reduced-motion: reduce) {.flow-line {animation:none}}
</style>
<script>
(function() {
  const root = document.getElementById('neural-wrap');
  if (!root) return;
  const nodes = root.querySelectorAll('.node');
  const title = root.querySelector('#node-title');
  const detail = root.querySelector('#node-detail');
  function activate(el) {
    nodes.forEach(n => n.classList.remove('selected'));
    el.classList.add('selected');
    title.textContent = el.dataset.title || 'Nodo tributario';
    detail.textContent = el.dataset.detail || '';
  }
  nodes.forEach(el => {
    el.addEventListener('click', () => activate(el));
    el.addEventListener('keydown', ev => {
      if (ev.key === 'Enter' || ev.key === ' ') {
        ev.preventDefault(); activate(el);
      }
    });
  });
})();
</script>
"""
]

components.html("".join(svg), height=820, scrolling=False)

st.markdown(
    '<p class="note">Interacción: selecciona el nodo central LRTI o cualquier nodo de las ramas IVA e IR. '
    'Las líneas animadas representan el flujo conceptual de la información.</p>',
    unsafe_allow_html=True,
)

# ------------------------- CONTROLES DEBAJO DEL GRÁFICO -------------------------
st.markdown('<div class="section-title">⚙️ Centro de control y datos de entrada</div>', unsafe_allow_html=True)
st.markdown("Modifica los valores para actualizar los nodos y los resultados de la red.")

col_iva, col_ir = st.columns(2, gap="large")
with col_iva:
    st.markdown("#### 🔵 1. Datos del IVA")
    ventas_mes = st.number_input(
        "Ventas del mes (USD sin IVA)", min_value=0.0, step=500.0,
        key="ventas_mes", format="%.2f"
    )
    compras_mes = st.number_input(
        "Compras del mes (USD sin IVA)", min_value=0.0, step=500.0,
        key="compras_mes", format="%.2f"
    )
    tipo_tarifa = st.selectbox(
        "Tarifa IVA aplicable", [15.0, 5.0, 0.0],
        key="tipo_tarifa", format_func=lambda x: f"{x:g}%"
    )
    retenciones_recibidas = st.number_input(
        "Retenciones recibidas (USD)", min_value=0.0, step=50.0,
        key="retenciones_recibidas", format="%.2f"
    )

with col_ir:
    st.markdown("#### 🟣 2. Datos del Impuesto a la Renta")
    ingresos_anual = st.number_input(
        "Ingresos del año (USD)", min_value=0.0, step=5000.0,
        key="ingresos_anual", format="%.2f"
    )
    costos_anual = st.number_input(
        "Costos y gastos deducibles (USD)", min_value=0.0, step=5000.0,
        key="costos_anual", format="%.2f"
    )
    st.info("En este prototipo, la tarifa de sociedades del 25% se utiliza como supuesto simplificado para estimar el IR. No sustituye la tabla progresiva de personas naturales ni los cálculos especiales del RIMPE.")

# Recalcular con los valores actuales.
iva_en_ventas = ventas_mes * (tipo_tarifa / 100.0)
credito_tributario = compras_mes * (tipo_tarifa / 100.0)
iva_retenido = retenciones_recibidas * 0.07
iva_pagar_calc = iva_en_ventas - credito_tributario - iva_retenido
iva_a_pagar = max(0.0, iva_pagar_calc)
iva_a_favor = abs(min(0.0, iva_pagar_calc))
base_imponible_renta = max(0.0, ingresos_anual - costos_anual)
impuesto_causado_renta = base_imponible_renta * 0.25
renta_retenida = retenciones_recibidas * 0.90
renta_a_pagar = max(0.0, impuesto_causado_renta - renta_retenida)

# Botón para forzar una nueva renderización del gráfico con los valores actualizados.
if st.button("🔄 Actualizar red neuronal", type="primary", use_container_width=True):
    st.rerun()

# ------------------------- RESULTADOS -------------------------
st.markdown('<div class="section-title">📊 Resultados del procesamiento</div>', unsafe_allow_html=True)
metrics = [
    ("IVA generado", money(iva_en_ventas)),
    ("Crédito tributario estimado", money(credito_tributario)),
    ("IVA a pagar", money(iva_a_pagar)),
    ("Saldo IVA a favor", money(iva_a_favor)),
    ("Base imponible de renta", money(base_imponible_renta)),
    ("Impuesto a la renta causado", money(impuesto_causado_renta)),
    ("Retenciones de renta estimadas", money(renta_retenida)),
    ("Impuesto a la renta a pagar", money(renta_a_pagar)),
]
metric_cols = st.columns(4)
for i, (label, value) in enumerate(metrics):
    with metric_cols[i % 4]:
        st.markdown(
            f'<div class="metric-card"><div class="metric-label">{esc(label)}</div>'
            f'<div class="metric-value">{esc(value)}</div></div>',
            unsafe_allow_html=True
        )

st.markdown("---")
st.markdown(
    '<p class="note">Modelo educativo. Los cálculos conservan las fórmulas simplificadas del archivo original '
    '(incluidos los porcentajes de retención parametrizados). Antes de utilizarlo para una declaración real, '
    'deben validarse las tarifas, porcentajes de retención, crédito tributario, régimen y tabla aplicable '
    'según la normativa vigente del SRI.</p>',
    unsafe_allow_html=True,
)
st.caption(f"Desarrollado por {DEVELOPER_NAME} · Ecuador · Modelo académico")
