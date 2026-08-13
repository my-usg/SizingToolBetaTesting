import streamlit as st
import os
import pandas as pd

# ── page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="Model 496 Sizing Tool", page_icon="⚙️", layout="wide", initial_sidebar_state="collapsed")

st.markdown("<style>[data-testid='stSidebarCollapseButton'],[data-testid='stSidebarCollapsedControl'],[data-testid='collapsedControl']{display:none}</style><h1>Model 496 Sizing Tool</h1>", unsafe_allow_html=True)
st.markdown("Fill in the inputs above and click **Run Sizing**.")

# ── load script logic ─────────────────────────────────────────────────────────
_tool_path = os.path.join(os.path.dirname(__file__), "496 Script.py")

try:
    with open(_tool_path, "r") as f:
        _source = f.read()
except FileNotFoundError as e:
    st.error(f"Could not load sizing script: {e}")
    st.stop()

_lines  = _source.splitlines(keepends=True)
_code   = "".join(_lines[:469])   # stop before INPUT section

_globals = {}
try:
    exec(compile(_code, _tool_path, "exec"), _globals)
except Exception as e:
    st.error(f"Failed to load sizing script: {e}")
    st.stop()

for _k, _v in _globals.items():
    if not _k.startswith("__"):
        globals()[_k] = _v


# ── helper: build dataframe from result dict ──────────────────────────────────
def build_table(prefix, opp_type, result496):
    rows = []
    for reg, cap in result496.items():
        if not reg.startswith(prefix):
            continue
        orifice  = _globals["orifice_type496"](reg)
        cap_str  = f"{cap:,.0f}" if isinstance(cap, (int, float)) else str(cap)
        works    = _globals["will_work"](cap, reg, _globals["orifice_max496"](reg))
        if opp_type == "IRV":
            irv = _globals["will_irv_work496"](reg, opp_type)
            rows.append([orifice, cap_str, works, irv])
        else:
            rows.append([orifice, cap_str, works])

    if opp_type == "IRV":
        cols = ["Orifice Size", "Calculated Capacity (CFH)", "Will Reg Work", "Will IRV Work"]
    else:
        cols = ["Orifice Size", "Calculated Capacity (CFH)", "Will Reg Work"]

    return pd.DataFrame(rows, columns=cols)


# ── SIDEBAR: inputs ───────────────────────────────────────────────────────────
def _req_label(key, text):
    """Red label with a ! while a required field is empty; normal once filled."""
    return f":red[{text}] ❗" if not st.session_state.get(key) else text


# ── INPUTS (top of page, always visible) ──────────────────────
st.subheader("📋 Inputs")

st.markdown("**Pressures & Flow**")
_v1, _v2, _v3, _v4 = st.columns(4)
with _v1:
    inlet_input  = st.number_input(_req_label("k_inlet", "Inlet pressure"), min_value=0.0, max_value=1000.0, value=0.0, step=0.1, format="%.1f", key="k_inlet")
with _v2:
    outlet_input = st.number_input(_req_label("k_outlet", "Outlet pressure"), min_value=0.0, max_value=1000.0, value=0.0, step=0.1, format="%.1f", key="k_outlet")
with _v3:
    flow_rate    = st.number_input(_req_label("k_flow", "Gas load / flow rate"), min_value=0, max_value=10000000000, value=0, step=50, format="%d", key="k_flow")
with _v4:
    maop = st.number_input("Max Allowable Inlet Pressure (psi)", min_value=0, max_value=1000, value=0, step=1, format="%d", help="Not required: default 0.  Regulator sized based on inlet pressure, however program will ensure configuration can handle this max inlet pressure.")
_u1, _u2, _u3, _u4 = st.columns(4)
with _u1:
    inlet_units  = st.selectbox("Inlet pressure units",  ["psi", "bar", "kPa"])
with _u2:
    outlet_units = st.selectbox("Outlet pressure units", ["psi", "in wc", "oz", "bar", "kPa"])
with _u3:
    flowrate_units = st.selectbox("Gas load / flow rate units", ["CFH", "CMH", "BTUH"])

_design, _loadgas = st.columns(2)
with _design:
    st.markdown("**Design Parameters**")
    _pipe_options = ["N/A", '3/8"', '1/2"', '3/4"', '1"']
    _sz, _ = st.columns([1, 1])
    with _sz:
        pipesize_index = st.selectbox("Desired pipe size", range(len(_pipe_options)),
            index=0, format_func=lambda i: _pipe_options[i])
    pipesize_input_raw = _pipe_options[pipesize_index]
    pipesize_input = 0 if pipesize_input_raw == "N/A" else pipesize_input_raw
    opp_choice = st.radio("Overpressure protection required?", ["No", "Yes"])
    irv_input  = 0.0
    opp_type   = "None"

    if opp_choice == "Yes":
        irv_input = st.number_input("Internal relief valve should limit downstream pressure buildup to (psi)",
                                    min_value=0.0, max_value=500.0, value=2.0, step=0.1, format="%.1f")
        opp_type = "IRV"
with _loadgas:
    st.markdown("**Load Type & Gas**")
    higheff   = st.radio("Feeding a generator or high-efficiency boiler?", ["No", "Yes"], help="Program will select a regulator that has capacity for double the load feeding high-efficiency equipment")
    pload     = 0.0
    pload_pct = 0
    if higheff == "Yes":
        pload_pct = st.slider("% of total load feeding high-efficiency appliances", 0, 100, 100, help="Program will select a regulator that has capacity for double the load feeding high-efficiency equipment")
        pload = pload_pct / 100.0
    oversizeby      = 1.25 + (0.75 * pload)
    oversize_percent = (oversizeby - 1) * 100

    override_oversize = st.radio("Override percentage regulator is oversized by?", ["No", "Yes"], help="Default is set to 25% or 100% for high-efficiency appliances")
    if override_oversize == "Yes":
        oversizeby = st.slider("Oversize regulator by:", 0, 100, 25, help="Recommended to oversize regulator by 20-30%")
        oversizeby = 1 + (oversizeby / 100)
        oversize_percent = (oversizeby - 1) * 100

    gastype_input = st.selectbox("Gas type", ["Natural Gas", "Propane", "Other"])
    gastypemult   = 1.0
    if gastype_input == "Propane":
        gastypemult = 0.63
    elif gastype_input == "Other":
        sg = st.number_input("Specific gravity", min_value=0.01, max_value=10.0, value=0.6, step=0.01, format="%.2f")
        gastypemult = min(1.0, (0.6 / sg) ** 0.5)
        st.info("Contact USG for regulator compatibility with gases other than methane or propane.")

    elevation = st.radio("Altitude above 3,000 feet or atmospheric pressure below 13 psi", ["No", "Yes"])
    Patm = 14.4
    if elevation == "Yes":
        Patm  = st.number_input("Atmospheric Pressure (psi)",   min_value=8.80, max_value=14.73, value=14.40,   step=0.01,  format="%.1f")

run_btn = st.button("▶  Run Sizing", type="primary")
st.divider()


# ── validation ────────────────────────────────────────────────────────────────
def build_summary_pdf(inputs, selection, capacity, part_numbers, warnings, adjustments, tool_name="USG Sizing Tool"):
    """Build the PDF summary and return a BytesIO buffer.

    Auto-scales down until the whole summary fits on a single page.
    """
    from io import BytesIO
    from datetime import datetime
    from xml.sax.saxutils import escape
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph, Table, TableStyle)

    ORANGE    = colors.HexColor("#e85d26")
    DARK      = colors.HexColor("#111827")
    DARK_BLUE = colors.HexColor("#1F3864")
    GREY      = colors.HexColor("#6b7280")
    LINE      = colors.HexColor("#e5e7eb")

    PAGE_W, PAGE_H = letter

    sel_pairs = [(lbl, val) for lbl, val in selection if val]
    if capacity:
        sel_pairs.append(("Calculated Capacity (CFH)", capacity))
    pns   = part_numbers if isinstance(part_numbers, list) else [part_numbers]
    pns   = [p for p in pns if p]
    warns = [w for w in (warnings or []) if w]

    def _render(scale):
        base = getSampleStyleSheet()
        title_style = ParagraphStyle("USGTitle", parent=base["Title"], textColor=DARK_BLUE,
                                     fontSize=20 * scale, leading=22 * scale, spaceAfter=1 * scale,
                                     alignment=0, leftIndent=0)
        tool_style  = ParagraphStyle("USGTool", parent=base["Normal"], textColor=DARK,
                                     fontSize=11 * scale, leading=13 * scale, spaceAfter=1 * scale, leftIndent=0)
        gen_style   = ParagraphStyle("USGGen", parent=base["Normal"], textColor=GREY,
                                     fontSize=7.5 * scale, leading=9 * scale, spaceAfter=8 * scale, leftIndent=0)
        sec_style   = ParagraphStyle("USGSection", parent=base["Heading2"], textColor=ORANGE,
                                     fontSize=10.5 * scale, leading=12 * scale,
                                     spaceBefore=7 * scale, spaceAfter=2 * scale,
                                     leftIndent=0, firstLineIndent=0)
        cell_style  = ParagraphStyle("USGCell", parent=base["Normal"],
                                     fontSize=8 * scale, leading=9.5 * scale, textColor=DARK)
        label_style = ParagraphStyle("USGLabel", parent=cell_style, fontName="Helvetica-Bold")

        pad = 2.2 * scale
        margin_x = 0.7 * inch
        margin_y = 0.5 * inch
        avail_w = PAGE_W - 2 * margin_x

        def _grid_style():
            return TableStyle([
                ("VALIGN",        (0, 0), (-1, -1), "TOP"),
                ("LINEBELOW",     (0, 0), (-1, -1), 0.4, LINE),
                ("TOPPADDING",    (0, 0), (-1, -1), pad),
                ("BOTTOMPADDING", (0, 0), (-1, -1), pad),
                ("LEFTPADDING",   (0, 0), (-1, -1), 0),
                ("RIGHTPADDING",  (0, 0), (-1, -1), 0),
            ])

        def kv_table(pairs):
            data = [[Paragraph(escape(str(k)), label_style),
                     Paragraph(escape(str(v)), cell_style)] for k, v in pairs]
            t = Table(data, colWidths=[avail_w * 0.4, avail_w * 0.6])
            t.setStyle(_grid_style())
            return t

        def list_table(items):
            data = [[Paragraph(escape(str(i)), cell_style)] for i in items]
            t = Table(data, colWidths=[avail_w])
            t.setStyle(_grid_style())
            return t

        story = []
        story.append(Paragraph("USG Sizing Tool", title_style))
        story.append(Paragraph(escape(str(tool_name)), tool_style))
        story.append(Paragraph("Generated " + datetime.now().strftime("%b %d, %Y  %I:%M %p"), gen_style))

        story.append(Paragraph("Inputs", sec_style))
        story.append(kv_table(list(inputs.items())) if inputs else Paragraph("None", cell_style))

        story.append(Paragraph("Regulator Selection", sec_style))
        story.append(kv_table(sel_pairs) if sel_pairs else Paragraph("No regulator selected.", cell_style))

        story.append(Paragraph("Part Number(s)", sec_style))
        story.append(list_table(pns) if pns else Paragraph("None", cell_style))

        story.append(Paragraph("Warnings", sec_style))
        story.append(list_table(warns) if warns else Paragraph("None", cell_style))

        story.append(Paragraph("Sizing Adjustments", sec_style))
        story.append(kv_table(list(adjustments.items())) if adjustments else Paragraph("None", cell_style))

        buf = BytesIO()
        doc = BaseDocTemplate(buf, pagesize=letter,
                              topMargin=margin_y, bottomMargin=margin_y,
                              leftMargin=margin_x, rightMargin=margin_x,
                              title="USG Sizing Tool")
        _frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height,
                       leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id="body")
        doc.addPageTemplates([PageTemplate(id="main", frames=[_frame])])
        doc.build(story)
        buf.seek(0)
        return buf, doc.page

    buf = None
    for scale in (1.0, 0.95, 0.9, 0.85, 0.8, 0.75, 0.7, 0.65, 0.6):
        buf, pages = _render(scale)
        if pages <= 1:
            break
    return buf


def to_psi(val, units):
    if units == "in wc": return val * (1/28)
    if units == "bar":   return val * 14.5
    if units == "oz":    return val / 16
    if units == "kPa":   return val / 6.89476
    return val

inlet_psi  = to_psi(inlet_input, inlet_units)
outlet_psi = to_psi(outlet_input, outlet_units)

# Elevation Reduction Calculation
if Patm < 14.4:
    ratio = (inlet_psi + Patm)/(outlet_psi + Patm)
    if ratio < 1.894:
        elevation_reduction = 100 * (1 - (((outlet_psi+Patm)*((inlet_psi+Patm)-(outlet_psi+Patm)))**0.5) / (((outlet_psi+14.65)*((inlet_psi+14.65)-(outlet_psi+14.65)))**0.5))
    else:
        elevation_reduction = 100 * (1 - (inlet_psi+Patm)/(inlet_psi+14.65))
else:
    elevation_reduction = 0

errors = []
if inlet_psi > 0 and (inlet_psi > 125 or inlet_psi < 1):
    errors.append("Inlet pressure must be between 1 and 125 psi.")
if outlet_psi > 0 and (outlet_psi < 3.5/28 or outlet_psi > 2):
    errors.append("Outlet pressure must be between 3.5\" wc and 2 psi.")
if inlet_psi > 0 and outlet_psi > 0 and outlet_psi >= inlet_psi:
    errors.append("Outlet pressure must be less than inlet pressure.")
if int(maop) != 0 and maop < inlet_psi:
    errors.append("MAIP must be >= inlet pressure.")
if inlet_psi == 0:
    errors.append("Inlet pressure is required.")
if outlet_psi == 0:
    errors.append("Outlet pressure is required.")
if flow_rate == 0:
    errors.append("Please enter a gas load / flow rate.")


# ── main area ─────────────────────────────────────────────────────────────────
if run_btn:
    if errors:
        for e in errors:
            st.error(e)
    else:
        with st.spinner("Sizing regulator…"):
            try:
                # unit conversions
                flow_cfh   = float(flow_rate)
                maop_psi   = inlet_psi if maop == 0 else float(maop)

                if flowrate_units == "CMH":
                    flow_cfh *= 35.3147
                elif flowrate_units == "BTUH":
                    if gastype_input == "Natural Gas":
                        flow_cfh /= 1000
                    elif gastype_input == "Propane":
                        flow_cfh /= 2516
                    else:
                        st.error("BTUH conversion only supported for Natural Gas or Propane. Use CFH or CMH.")
                        st.stop()

                # inject globals
                _globals.update({
                    "inlet_input":    inlet_psi,
                    "outlet_input":   outlet_psi,
                    "flow_rate":      flow_cfh,
                    "maop":           maop_psi,
                    "pipesize_input": pipesize_input,
                    "opp_type":       opp_type,
                    "irv_input":      irv_input,
                    "oversizeby":     oversizeby,
                    "oversize_percent": oversize_percent,
                    "gastypemult":    gastypemult,
                    "pload":          pload,
                    "Patm":           Patm,
                    "result496":      {},
                })

                # run sizing
                result496, match496, apply496, warning496 = _globals["run_regulator_selection496"](
                    inlet_psi, outlet_psi, opp_type)

                # update result496 in globals for table builder
                _globals["result496"] = result496

                # table opp_type
                table_opp = opp_type

                # ── regulator selection ───────────────────────────────────────
                if apply496:
                    if warning496:
                        st.warning(warning496)

                    st.success("✅  Regulator selected!")

                    st.subheader("Regulator Selection")
                    fields = [
                        ("Model",          match496.get("model")),
                        ("Body Size",      match496.get("body")),
                        ("Orifice Size",   match496.get("orifice")),
                        ("Seat",           match496.get("seat")),
                        ("Spring",         f"{match496.get('color','')} {match496.get('range','')}".strip()),
                        ("Monitor Spring", f"{match496.get('mon_color','')} {match496.get('mon_range','')}".strip() if match496.get("mon_color") else None),
                    ]
                    for label, val in fields:
                        if val:
                            st.markdown(f"**{label}:** {val}")

                    cap = match496.get("capacity")
                    if cap and cap != "N/A":
                        try:
                            st.markdown(f"**Calculated Capacity (CFH):** {int(round(float(cap))):,}")
                        except Exception:
                            st.markdown(f"**Calculated Capacity (CFH):** {cap}")

                    st.subheader("HSC Part Number(s)")
                    pn = _globals["hsc_pnc496"](match496)
                    if isinstance(pn, list):
                        for p in pn:
                            st.code(p)
                    else:
                        st.code(pn)

                else:
                    if result496 is None:
                        if warning496:
                            st.warning(warning496)
                        st.error("❌  Model 496 will not work for this application.")
                        st.stop()
                    else:
                        st.error("❌  Model 496 will not work for this application.")

                # ── sizing tables ─────────────────────────────────────────────
                st.divider()
                st.subheader("Regulator Sizing Tables")

                body_sizes = [
                    ('Model 496, 3/8" Body', 'R49638'),
                    ('Model 496, 1/2" Body', 'R49612'),
                    ('Model 496, 3/4" Body', 'R49634'),
                    ('Model 496, 1" Body',   'R49610'),
                ]

                for title, prefix in body_sizes:
                    df = build_table(prefix, table_opp, result496)
                    if not df.empty:
                        st.markdown(f"**{title}**")
                        st.dataframe(df, use_container_width=True, hide_index=True)

                # ── sizing adjustments ───────────────────────────────────────
                st.divider()
                st.subheader("Sizing Adjustments")
                adj = {"Oversized By": f"{oversize_percent:.0f}%"}
                if apply496 and match496.get("opp") == "Monitor":
                    adj["Monitor Capacity Reduction"] = "30%"
                if gastypemult != 1:
                    adj["Gas Type Factor"] = f"{gastypemult:.4f}"
                if Patm < 14.4:
                    adj["Elevation capacity reduction"] = f"{elevation_reduction:.0f}%"
                df_adj = pd.DataFrame(adj.items(), columns=["Adjustment", "Value"])
                st.dataframe(df_adj, use_container_width=True, hide_index=True)

                # ── input summary ─────────────────────────────────────────────
                # st.divider()
                # st.subheader("Input Summary")
                summary = {
                    f"Inlet Pressure ({inlet_units})":   inlet_input,
                    f"Outlet Pressure ({outlet_units})": outlet_input,
                    f"Gas Load ({flowrate_units})":      f"{flow_rate:,}",
                    "Max Allowable Inlet Pressure (psi)":                        f"{int(maop)}",
                    "Requested Pipe Size":               _pipe_options[pipesize_index],
                    "Overpressure Protection Required":  "Yes" if opp_choice == "Yes" else "No",
                }
                if opp_choice == "Yes":
                    summary["IRV Protect Downstream Pressure To (psi)"] = f"{irv_input:.1f}"
                summary["Percent Load Feeding High-Efficiency Appliance"] = f"{pload_pct}%" if higheff == "Yes" else "N/A"
                summary["Gas Type"]             = gastype_input
                summary["Override Oversize %"] = f"{(oversizeby - 1) * 100:.0f}%" if override_oversize == "Yes" else "No"
                summary["Atmospheric Pressure (psi)"] = f"{Patm:.1f}" if Patm < 14.4 else "14.4"
                # df_summary = pd.DataFrame(summary.items(), columns=["Parameter", "Value"])
                # st.dataframe(df_summary, use_container_width=True, hide_index=True)

                # ── PDF summary download ──────────────────────────────────────
                if apply496:
                    st.divider()
                    st.subheader("Download PDF Summary")
                    try:
                        _cap = match496.get("capacity")
                        try:
                            _cap_str = f"{int(round(float(_cap))):,}" if _cap and _cap != "N/A" else ""
                        except Exception:
                            _cap_str = str(_cap) if _cap else ""
                        pdf_buf = build_summary_pdf(
                            inputs=summary,
                            selection=fields,
                            capacity=_cap_str,
                            part_numbers=pn,
                            warnings=[warning496] if warning496 else [],
                            adjustments=adj,
                            tool_name="Model 496 Sizing Tool",
                        )
                        st.download_button(
                            label="⬇️  Download PDF Summary",
                            data=pdf_buf,
                            file_name="USG_Sizing_Tool_Output.pdf",
                            mime="application/pdf",
                        )
                    except Exception as _pex:
                        st.warning(f"Could not generate PDF: {_pex}")

            except Exception as ex:
                st.error(f"Error during sizing: {ex}")
                import traceback; st.code(traceback.format_exc())

else:
    st.info("⬆️  Fill in the inputs above and click **Run Sizing**.")