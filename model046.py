import streamlit as st
import os
import pandas as pd

# ── page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="Model 046 Sizing Tool", page_icon="⚙️", layout="wide")

st.markdown("<style>.beta-badge{display:inline-block;font-size:.6rem;font-weight:600;letter-spacing:.15em;text-transform:uppercase;color:#e85d26;border:1.5px solid #e85d26;border-radius:2px;padding:.1rem .35rem;margin-left:.5rem;vertical-align:middle;position:relative;top:-4px;font-family:sans-serif}</style><h1>⚙️ Model 046 Sizing Tool <span class='beta-badge'>Beta</span></h1>", unsafe_allow_html=True)
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
_code   = "".join(_lines[:691])

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
def build_table(prefix, opp_type, result, irv_input_val, partial_flag):
    rows = []
    for reg, cap in result.items():
        if not reg.startswith(prefix):
            continue
        orifice = _globals["orifice_typeSMALL"](reg)
        cap_str = f"{cap:,.0f}" if isinstance(cap, (int, float)) else str(cap)
        works   = _globals["will_work"](cap, reg, _globals["orifice_max046"](reg))
        if opp_type == "IRV" and not partial_flag:
            irv = _globals["will_irv_work046"](reg, irv_input_val)
            rows.append([orifice, cap_str, works, irv])
        else:
            rows.append([orifice, cap_str, works])

    if opp_type == "IRV" and not partial_flag:
        cols = ["Orifice Size", "Calculated Capacity (CFH)", "Will Reg Work?", "Will IRV Work?"]
    else:
        cols = ["Orifice Size", "Calculated Capacity (CFH)", "Will It Work?"]

    return pd.DataFrame(rows, columns=cols)


# ── SIDEBAR: inputs ───────────────────────────────────────────────────────────
with st.sidebar:
    st.header("📋 Inputs")

    st.subheader("Pressures & Flow")
    inlet_units  = st.selectbox("Inlet pressure units",  ["psi", "bar"])
    inlet_input  = st.number_input("Inlet pressure", min_value=0.0, max_value=100000.0, value=0.0, step=0.1, format="%.1f")

    outlet_units = st.selectbox("Outlet pressure units", ["psi", "in wc", "bar"])
    outlet_input = st.number_input("Outlet pressure", min_value=0.0, max_value=10000.0, value=0.0, step=0.1, format="%.1f")

    flowrate_units = st.selectbox("Flow rate units", ["CFH", "CMH", "BTUH"])
    flow_rate    = st.number_input("Gas load / flow rate", min_value=0, max_value=500000000, value=0, step=50, format="%d")

    maop = st.number_input("Max inlet pressure / MAOP (psi)", min_value=0, max_value=1000, value=0, step=1, format="%d",
                           help="MAOP is always entered in psi. Enter 0 to use inlet pressure.")

    st.subheader("Design Parameters")
    _pipe_options = ["N/A", '3/8"', '1/2"', '3/4"', '1"', '1-1/4"', '1-1/2"', '2"', '2-1/2"', '3"']
    pipesize_index = st.selectbox("Desired pipe size", range(len(_pipe_options)),
        index=0, format_func=lambda i: _pipe_options[i])
    pipesize_input_raw = _pipe_options[pipesize_index]
    pipesize_input = 0 if pipesize_input_raw == "N/A" else pipesize_input_raw

    opp_choice = st.radio("Overpressure protection required?", ["No", "Yes"])
    partial    = False
    irv_input  = 0.0
    opp_type   = "None"
    opp_pref   = ""

    if opp_choice == "Yes":
        opp_pref = st.radio("If applicable should the program prioritize sizing with IRV or default to monitor regulator sizing?",
                            ["IRV (Internal Relief Valve)", "Monitor regulator"])
        if "IRV" in opp_pref:
            irv_input = st.number_input("IRV protect downstream pressure to (psi)",
                                        min_value=0.0, max_value=500.0, value=2.0, step=0.1, format="%.1f")
            opp_type = "IRV"
        else:
            opp_type = "Monitor"
    else:
        partial_choice = st.radio("If applicable, select regulator with IRV for partial overpressure protection?", ["No", "Yes"])
        if partial_choice == "Yes":
            partial  = True
            opp_type = "IRV"

    st.subheader("Load Type & Gas")
    higheff   = st.radio("Feeding a generator or high-efficiency boiler?", ["No", "Yes"])
    pload     = 0.0
    pload_pct = 0
    if higheff == "Yes":
        pload_pct = st.slider("% of total load feeding generator / high-eff boiler", 0, 100, 50)
        pload = pload_pct / 100.0
    oversizeby       = 1.2 + (0.8 * pload)
    oversize_percent = (oversizeby - 1) * 100

    gastype_input = st.selectbox("Gas type", ["Natural Gas", "Propane", "Other"])
    gastypemult   = 1.0
    if gastype_input == "Propane":
        gastypemult = 0.63
    elif gastype_input == "Other":
        sg = st.number_input("Specific gravity", min_value=0.01, max_value=10.0, value=0.6, step=0.01, format="%.2f")
        gastypemult = min(1.0, (0.6 / sg) ** 0.5)
        st.info("Contact USG for regulator compatibility with gases other than methane or propane.")

    run_btn = st.button("▶  Run Sizing", type="primary", use_container_width=True)


# ── validation ────────────────────────────────────────────────────────────────
def to_psi(val, units):
    if units == "in wc": return val * (1/28)
    if units == "bar":   return val * 14.5
    return val

_inlet_psi_check  = inlet_input * 14.5 if inlet_units == "bar" else inlet_input
_outlet_psi_check = to_psi(outlet_input, outlet_units)

errors = []
if inlet_input > 0 and (_inlet_psi_check > 1000 or _inlet_psi_check < 10):
    errors.append("Inlet pressure must be between 10 and 1,000 psi.")
if outlet_input > 0 and (_outlet_psi_check < 3 or _outlet_psi_check > 200):
    errors.append("Outlet pressure must be between 3 and 200 psi.")
if inlet_input > 0 and outlet_input > 0 and _outlet_psi_check >= _inlet_psi_check:
    errors.append("Outlet pressure must be less than inlet pressure.")
if int(maop) != 0 and maop < _inlet_psi_check:
    errors.append("MAOP must be ≥ inlet pressure.")
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
                inlet_psi  = _inlet_psi_check
                outlet_psi = _outlet_psi_check
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
                    "partial":           partial,
                    "irv_input":         irv_input,
                    "irv_lim":           irv_input - outlet_psi if irv_input else 0,
                    "oversizeby":        oversizeby,
                    "oversize_percent":  oversize_percent,
                    "gastypemult":       gastypemult,
                    "pload":             pload,
                })

                # run sizing
                result046, match046, apply046, warning046 = _globals["run_regulator_selection046"](
                    inlet_psi, outlet_input046, opp_type)

                # for IRV: also compute separate irv/monitor results for tables
                if opp_type == "IRV" and not partial:
                    result_irv = _globals["interpolate_capacity"](_globals["data046"], inlet_psi, outlet_input046, False, False)
                    result_mon = _globals["interpolate_capacity"](_globals["data046"], inlet_psi, outlet_input046, True, False)
                else:
                    result_irv = result046
                    result_mon = result046

                # ── warnings ─────────────────────────────────────────────────
                if warning046:
                    st.warning(warning046)

                # ── regulator selection ───────────────────────────────────────
                if apply046:
                    st.success("✅  Regulator selected!")

                    st.subheader("Regulator Selection")
                    fields = [
                        ("Model",        match046.get("model")),
                        ("Body Size",    match046.get("body")),
                        ("Orifice Size", match046.get("orifice")),
                        ("Seat",         match046.get("seat")),
                        ("Spring",       f"{match046.get('color','')} {match046.get('range','')}".strip()),
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
                    if not warning046:
                        st.error("❌  Model 046 will not work for this application.")

                # ── sizing tables ─────────────────────────────────────────────
                st.divider()
                st.subheader("Regulator Sizing Tables")

                if opp_type == "IRV" and not partial:
                    st.markdown("**Regulator Sizing Tables with IRV**")
                    for title, prefix in [
                        ('Model 046-2, 3/4" Body',     'R046234'),
                        ('Model 046-2, 1" Body',        'R046210'),
                        ('Model 046-2, 1-1/4" Body',    'R04621Q'),
                    ]:
                        df = build_table(prefix, "IRV", result_irv, irv_input, partial)
                        if not df.empty:
                            st.markdown(f"**{title}**")
                            st.dataframe(df, use_container_width=True, hide_index=True)

                    st.markdown("**Regulator Sizing Tables with Monitor**")
                    for title, prefix in [
                        ('Model 046, 046-M or 046-2M, 3/4" Body',   'R046134'),
                        ('Model 046, 046-M or 046-2M, 1" Body',      'R046110'),
                        ('Model 046, 046-M or 046-2M, 1-1/4" Body',  'R04611Q'),
                    ]:
                        df = build_table(prefix, "Monitor", result_mon, irv_input, partial)
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
                        df = build_table(prefix, "Monitor", result046, irv_input, partial)
                        if not df.empty:
                            st.markdown(f"**{title}**")
                            st.dataframe(df, use_container_width=True, hide_index=True)

                else:
                    for title, prefix in [
                        ('Model 046, 046-M or 046-2M, 3/4" Body',   'R046134'),
                        ('Model 046, 046-M or 046-2M, 1" Body',      'R046110'),
                        ('Model 046, 046-M or 046-2M, 1-1/4" Body',  'R04611Q'),
                    ]:
                        df = build_table(prefix, opp_type, result046, irv_input, partial)
                        if not df.empty:
                            st.markdown(f"**{title}**")
                            st.dataframe(df, use_container_width=True, hide_index=True)

                # ── sizing adjustments ───────────────────────────────────────
                st.divider()
                st.subheader("Sizing Adjustments")
                adj = {"Oversized By": f"{oversize_percent:.0f}%"}
                if apply046 and match046.get("opp") == "Monitor":
                    adj["Monitor Regulator"] = "30% capacity reduction applied"
                if gastypemult != 1:
                    adj["Gas Type Factor"] = f"{gastypemult:.4f}"
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
                if partial:
                    summary["Select Regulator with IRV"] = "Yes"
                if opp_choice == "Yes":
                    summary["Protection Type"] = "IRV" if "IRV" in opp_pref else "Monitor"
                    if "IRV" in opp_pref:
                        summary["IRV Protect Downstream Pressure To (psi)"] = f"{irv_input:.1f}"
                summary["% Load Feeding Generator / High-Eff Boiler"] = f"{pload_pct}%" if higheff == "Yes" else "N/A"
                summary["Gas Type"]             = gastype_input

                df_summary = pd.DataFrame(summary.items(), columns=["Parameter", "Value"])
                st.dataframe(df_summary, use_container_width=True, hide_index=True)

            except Exception as ex:
                st.error(f"Error during sizing: {ex}")
                import traceback; st.code(traceback.format_exc())

else:
    st.info("👈  Fill in the inputs on the left and click **Run Sizing**.")