import streamlit as st
import os
import pandas as pd

# ── page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="Model 046 Sizing Tool", page_icon="⚙️", layout="wide", initial_sidebar_state="expanded")

st.markdown("<style>[data-testid='stSidebarCollapseButton'],[data-testid='stSidebarCollapsedControl'],[data-testid='collapsedControl']{display:none}</style><h1>Model 046 Sizing Tool</h1>", unsafe_allow_html=True)
st.markdown("Fill in the inputs on the left and click **Run Sizing**.")

# ── load script logic ─────────────────────────────────────────────────────────
_tool_path = os.path.join(os.path.dirname(__file__), "046 Script.py")

try:
    with open(_tool_path, "r") as f:
        _source = f.read()
except FileNotFoundError as e:
    st.error(f"Could not load sizing script: {e}")
    st.stop()

_lines  = _source.splitlines(keepends=True)
_code   = "".join(_lines[:763])

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
def build_table(prefix, opp_type, result, irv_input_val):
    rows = []
    for reg, cap in result.items():
        if not reg.startswith(prefix):
            continue
        orifice = _globals["orifice_typeSMALL"](reg)
        cap_str = f"{cap:,.0f}" if isinstance(cap, (int, float)) else str(cap)
        works   = _globals["will_work"](cap, reg, _globals["orifice_max046"](reg))
        if opp_type == "IRV":
            irv = _globals["will_irv_work046"](reg, opp_type)
            rows.append([orifice, cap_str, works, irv])
        else:
            rows.append([orifice, cap_str, works])

    if opp_type == "IRV":
        cols = ["Orifice Size", "Calculated Capacity (CFH)", "Will Reg Work?", "Will IRV Work?"]
    else:
        cols = ["Orifice Size", "Calculated Capacity (CFH)", "Will It Work?"]

    return pd.DataFrame(rows, columns=cols)


# ── SIDEBAR: inputs ───────────────────────────────────────────────────────────
with st.sidebar:
    st.header("📋 Inputs")

    st.subheader("Pressures & Flow")
    inlet_units  = st.selectbox("Inlet pressure units",  ["psi", "bar"], help="Required")
    inlet_input  = st.number_input("Inlet pressure", min_value=0.0, max_value=100000.0, value=0.0, step=0.1, format="%.1f", help="Required")

    outlet_units = st.selectbox("Outlet pressure units", ["psi", "in wc", "bar", "oz"], help="Required")
    outlet_input = st.number_input("Outlet pressure", min_value=0.0, max_value=10000.0, value=0.0, step=0.1, format="%.1f", help="Required")

    flowrate_units = st.selectbox("Gas load / flow rate units", ["CFH", "CMH", "BTUH"], help="Required")
    flow_rate    = st.number_input("Gas load / flow rate", min_value=0, max_value=500000000, value=0, step=50, format="%d", help="Required")

    maop = st.number_input("Max inlet pressure / MAOP (psi)", min_value=0, max_value=1000, value=0, step=1, format="%d",
                           help="Not required: default 0.  Regulator sized based on inlet pressure, however program will ensure configuration can handle this max inlet pressure/MAOP.")

    st.subheader("Design Parameters")
    _pipe_options = ["N/A", '3/8"', '1/2"', '3/4"', '1"', '1-1/4"', '1-1/2"', '2"', '2-1/2"', '3"']
    pipesize_index = st.selectbox("Desired pipe size", range(len(_pipe_options)),
        index=0, format_func=lambda i: _pipe_options[i])
    pipesize_input_raw = _pipe_options[pipesize_index]
    pipesize_input = 0 if pipesize_input_raw == "N/A" else pipesize_input_raw

    opp_choice = st.radio("Overpressure protection required?", ["No", "Yes"])
    irv_input  = 0.0
    opp_type   = "None"
    opp_pref   = ""

    if opp_choice == "Yes":
        opp_pref = st.radio("If applicable should the program prioritize sizing with an internal relief valve or default to monitor regulator sizing?",
                            ["IRV (Internal Relief Valve)", "Monitor regulator"])
        if "IRV" in opp_pref:
            irv_input = st.number_input("Internal relief valve should limit downstream pressure buildup to (psi)",
                                        min_value=0.0, max_value=500.0, value=2.0, step=0.1, format="%.1f")
            opp_type = "IRV"
        else:
            opp_type = "Monitor"
    else:
        partial_choice = st.radio("If applicable, select regulator with an internal relief valve for partial overpressure protection?", ["No", "Yes"])
        if partial_choice == "Yes":
            opp_type = "Partial"

    st.subheader("Load Type & Gas")
    higheff   = st.radio("Feeding a generator or high-efficiency boiler?", ["No", "Yes"])
    pload     = 0.0
    pload_pct = 0
    if higheff == "Yes":
        pload_pct = st.slider("% of total load feeding generator / high-eff boiler", 0, 100, 50, help="Program will select a regulator that has capacity for double the load feeding high-efficiency equipment")
        pload = pload_pct / 100.0
    oversizeby       = 1.25 + (0.75 * pload)
    oversize_percent = (oversizeby - 1) * 100

    gastype_input = st.selectbox("Gas type", ["Natural Gas", "Propane", "Other"])
    gastypemult   = 1.0
    if gastype_input == "Propane":
        gastypemult = 0.63
    elif gastype_input == "Other":
        sg = st.number_input("Specific gravity", min_value=0.01, max_value=10.0, value=0.6, step=0.01, format="%.2f")
        gastypemult = min(1.0, (0.6 / sg) ** 0.5)
        st.info("Contact USG for regulator compatibility with gases other than methane or propane.")

    # Altitude
    elevation = st.radio("Altitude above 3,000 feet or atmospheric pressure below 13 psi", ["No", "Yes"])
    Patm = 14.4
    if elevation == "Yes":
        Patm  = st.number_input("Atmospheric Pressure (psi)",   min_value=8.80, max_value=14.73, value=14.40,   step=0.01,  format="%.1f")

    run_btn = st.button("▶  Run Sizing", type="primary", use_container_width=True)


# ── validation ────────────────────────────────────────────────────────────────
def build_summary_pdf(inputs, selection, capacity, part_numbers, warnings, adjustments):
    """Build the 'USG Sizing Tool Output' PDF summary and return a BytesIO buffer.

    The layout is compact and auto-scales down until the whole summary fits on a
    single page.

    inputs       : dict of Parameter -> Value
    selection    : list of (label, value) tuples for the chosen regulator
    capacity     : pre-formatted capacity string (or "")
    part_numbers : list or str of HSC part number(s)
    warnings     : list of warning strings
    adjustments  : dict of Adjustment -> Value
    """
    from io import BytesIO
    from datetime import datetime
    from xml.sax.saxutils import escape
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Table, TableStyle)

    ORANGE = colors.HexColor("#e85d26")
    DARK   = colors.HexColor("#111827")
    GREY   = colors.HexColor("#6b7280")
    LINE   = colors.HexColor("#e5e7eb")

    PAGE_W, PAGE_H = letter

    # normalise the section data once
    sel_pairs = [(lbl, val) for lbl, val in selection if val]
    if capacity:
        sel_pairs.append(("Calculated Capacity (CFH)", capacity))
    pns   = part_numbers if isinstance(part_numbers, list) else [part_numbers]
    pns   = [p for p in pns if p]
    warns = [w for w in (warnings or []) if w]

    def _render(scale):
        """Render the whole summary at a given scale; return (buffer, page_count)."""
        base = getSampleStyleSheet()
        title_style = ParagraphStyle("USGTitle", parent=base["Title"], textColor=DARK,
                                     fontSize=18 * scale, leading=20 * scale, spaceAfter=1 * scale, alignment=0)
        sub_style   = ParagraphStyle("USGSub", parent=base["Normal"], textColor=GREY,
                                     fontSize=7.5 * scale, leading=9 * scale, spaceAfter=8 * scale)
        sec_style   = ParagraphStyle("USGSection", parent=base["Heading2"], textColor=ORANGE,
                                     fontSize=10.5 * scale, leading=12 * scale,
                                     spaceBefore=7 * scale, spaceAfter=2 * scale)
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
        story.append(Paragraph("USG Sizing Tool Output", title_style))
        story.append(Paragraph(
            "United Sales Group \u00b7 Regulator Sizing Platform \u00b7 Generated "
            + datetime.now().strftime("%b %d, %Y  %I:%M %p"), sub_style))

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
        doc = SimpleDocTemplate(buf, pagesize=letter,
                                topMargin=margin_y, bottomMargin=margin_y,
                                leftMargin=margin_x, rightMargin=margin_x,
                                title="USG Sizing Tool Output")
        doc.build(story)
        buf.seek(0)
        return buf, doc.page

    # Shrink until it fits on one page (or we hit the readability floor).
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
if inlet_input > 0 and (inlet_psi > 1000 or inlet_psi < 10):
    errors.append("Inlet pressure must be between 10 and 1,000 psi.")
if outlet_input > 0 and (outlet_psi < 3 or outlet_psi > 200):
    errors.append("Outlet pressure must be between 3 and 200 psi.")
if inlet_input > 0 and outlet_input > 0 and outlet_psi >= inlet_psi:
    errors.append("Outlet pressure must be less than inlet pressure.")
if int(maop) != 0 and maop < inlet_psi:
    errors.append("MAOP must be ≥ inlet pressure.")
if inlet_input == 0:
    errors.append("Inlet pressure is required.")
if outlet_input == 0:
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

                # outlet pressure adjustment (mirror script: 3–5 psi → 5 psi)
                outlet_input046 = 5 if 3 <= outlet_psi < 5 else outlet_psi

                # inject globals
                _globals.update({
                    "inlet_input":       inlet_psi,
                    "outlet_input":      outlet_psi,
                    "flow_rate":         flow_cfh,
                    "maop":              maop_psi,
                    "pipesize_input":    pipesize_input,
                    "opp_type":          opp_type,
                    "irv_input":         irv_input,
                    "oversizeby":        oversizeby,
                    "oversize_percent":  oversize_percent,
                    "gastypemult":       gastypemult,
                    "pload":             pload,
                    "Patm":              Patm,
                })

                # run sizing
                result046, match046, apply046, warning046 = _globals["run_regulator_selection046"](
                    inlet_psi, outlet_input046, opp_type)

                # for IRV: also compute separate irv/monitor results for tables
                if opp_type == "IRV":
                    result_irv = _globals["interpolate_capacity"](_globals["data046"], inlet_psi, outlet_input046, False, False)
                    result_mon = _globals["interpolate_capacity"](_globals["data046"], inlet_psi, outlet_input046, True, False)
                else:
                    result_irv = result046
                    result_mon = result046

                # ── regulator selection ───────────────────────────────────────
                if apply046:
                    if warning046:
                        st.warning(warning046)

                    st.success("✅  Regulator selected!")

                    st.subheader("Regulator Selection")
                    fields = [
                        ("Model",          match046.get("model")),
                        ("Body Size",      match046.get("body")),
                        ("Orifice Size",   match046.get("orifice")),
                        ("Seat",           match046.get("seat")),
                        ("Spring",         f"{match046.get('color','')} {match046.get('range','')}".strip()),
                        ("Monitor Spring", f"{match046.get('mon_color','')} {match046.get('mon_range','')}".strip() if match046.get("mon_color") else None),
                    ]
                    for label, val in fields:
                        if val:
                            st.markdown(f"**{label}:** {val}")

                    cap = match046.get("capacity")
                    if cap and cap != "N/A":
                        try:
                            st.markdown(f"**Calculated Capacity (CFH):** {int(round(float(cap))):,}")
                        except Exception:
                            st.markdown(f"**Calculated Capacity (CFH):** {cap}")

                    st.subheader("HSC Part Number(s)")
                    pn = _globals["hsc_pnc046"](match046)
                    if isinstance(pn, list):
                        for p in pn:
                            st.code(p)
                    else:
                        st.code(pn)

                else:
                    if result046 is None:
                        if warning046:
                            st.warning(warning046)
                        st.error("❌  Model 046 will not work for this application.")
                        st.stop()
                    else:
                        st.error("❌  Model 046 will not work for this application.")

                # ── sizing tables ─────────────────────────────────────────────
                st.divider()
                st.subheader("Regulator Sizing Tables")

                if opp_type == "IRV":
                    st.markdown("**Regulator Sizing Tables with IRV**")
                    for title, prefix in [
                        ('Model 046-2, 3/4" Body',     'R046234'),
                        ('Model 046-2, 1" Body',        'R046210'),
                        ('Model 046-2, 1-1/4" Body',    'R04621Q'),
                    ]:
                        df = build_table(prefix, "IRV", result_irv, irv_input)
                        if not df.empty:
                            st.markdown(f"**{title}**")
                            st.dataframe(df, use_container_width=True, hide_index=True)

                    st.markdown("**Regulator Sizing Tables with Monitor**")
                    for title, prefix in [
                        ('Model 046, 046-M or 046-2M, 3/4" Body',   'R046134'),
                        ('Model 046, 046-M or 046-2M, 1" Body',      'R046110'),
                        ('Model 046, 046-M or 046-2M, 1-1/4" Body',  'R04611Q'),
                    ]:
                        df = build_table(prefix, "Monitor", result_mon, irv_input)
                        if not df.empty:
                            st.markdown(f"**{title}**")
                            st.dataframe(df, use_container_width=True, hide_index=True)

                elif opp_type == "Partial":
                    st.markdown("**Regulator Sizing Tables with Partial IRV**")
                    for title, prefix in [
                        ('Model 046-2, 3/4" Body',     'R046234'),
                        ('Model 046-2, 1" Body',        'R046210'),
                        ('Model 046-2, 1-1/4" Body',    'R04621Q'),
                    ]:
                        df = build_table(prefix, "Partial", result046, irv_input)
                        if not df.empty:
                            st.markdown(f"**{title}**")
                            st.dataframe(df, use_container_width=True, hide_index=True)

                elif opp_type == "Monitor":
                    st.markdown("**Regulator Sizing Tables with Monitor**")
                    for title, prefix in [
                        ('Model 046, 046-M or 046-2M, 3/4" Body',   'R046134'),
                        ('Model 046, 046-M or 046-2M, 1" Body',      'R046110'),
                        ('Model 046, 046-M or 046-2M, 1-1/4" Body',  'R04611Q'),
                    ]:
                        df = build_table(prefix, "Monitor", result046, irv_input)
                        if not df.empty:
                            st.markdown(f"**{title}**")
                            st.dataframe(df, use_container_width=True, hide_index=True)

                else:
                    for title, prefix in [
                        ('Model 046, 046-M or 046-2M, 3/4" Body',   'R046134'),
                        ('Model 046, 046-M or 046-2M, 1" Body',      'R046110'),
                        ('Model 046, 046-M or 046-2M, 1-1/4" Body',  'R04611Q'),
                    ]:
                        df = build_table(prefix, opp_type, result046, irv_input)
                        if not df.empty:
                            st.markdown(f"**{title}**")
                            st.dataframe(df, use_container_width=True, hide_index=True)

                # ── sizing adjustments ───────────────────────────────────────
                st.divider()
                st.subheader("Sizing Adjustments")
                adj = {"Oversized By": f"{oversize_percent:.0f}%"}
                if apply046 and match046.get("opp") == "Monitor":
                    adj["Monitor Capacity Reduction"] = "30%"
                if gastypemult != 1:
                    adj["Gas Type Factor"] = f"{gastypemult:.4f}"
                if Patm < 14.4:
                    adj["Elevation capacity reduction"] = f"{elevation_reduction:.0f}%"
                df_adj = pd.DataFrame(adj.items(), columns=["Adjustment", "Value"])
                st.dataframe(df_adj, use_container_width=True, hide_index=True)

                # ── input summary ─────────────────────────────────────────────
                st.divider()
                st.subheader("Input Summary")
                summary = {
                    f"Inlet Pressure ({inlet_units})":   inlet_input,
                    f"Outlet Pressure ({outlet_units})": outlet_input,
                    f"Gas Load ({flowrate_units})":      f"{flow_rate:,}",
                    "MAOP (psi)":                        f"{int(maop)}",
                    "Requested Pipe Size":               _pipe_options[pipesize_index],
                    "Overpressure Protection Required":  "Yes" if opp_choice == "Yes" else "No",
                }
                if opp_type == "Partial":
                    summary["Select Regulator with IRV"] = "Yes"
                if opp_choice == "Yes":
                    summary["Protection Type"] = "IRV" if "IRV" in opp_pref else "Monitor"
                    if "IRV" in opp_pref:
                        summary["IRV Protect Downstream Pressure To (psi)"] = f"{irv_input:.1f}"
                summary["% Load Feeding Generator / High-Eff Boiler"] = f"{pload_pct}%" if higheff == "Yes" else "N/A"
                summary["Gas Type"]             = gastype_input
                summary["Atmospheric Pressure (psi)"] = f"{Patm:.1f}" if Patm < 14.4 else "14.4"
                df_summary = pd.DataFrame(summary.items(), columns=["Parameter", "Value"])
                st.dataframe(df_summary, use_container_width=True, hide_index=True)

                # ── PDF summary download ──────────────────────────────────────
                if apply046:
                    st.divider()
                    st.subheader("Download PDF Summary")
                    try:
                        _cap = match046.get("capacity")
                        try:
                            _cap_str = f"{int(round(float(_cap))):,}" if _cap and _cap != "N/A" else ""
                        except Exception:
                            _cap_str = str(_cap) if _cap else ""
                        pdf_buf = build_summary_pdf(
                            inputs=summary,
                            selection=fields,
                            capacity=_cap_str,
                            part_numbers=pn,
                            warnings=[warning046] if warning046 else [],
                            adjustments=adj,
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
    st.info("👈  Fill in the inputs on the left and click **Run Sizing**.")