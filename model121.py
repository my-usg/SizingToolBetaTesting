import streamlit as st
import os
import pandas as pd

# ── page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="Model 121/122 Sizing Tool", page_icon="⚙️", layout="wide")

st.markdown("<style>.beta-badge{display:inline-block;font-size:.6rem;font-weight:600;letter-spacing:.15em;text-transform:uppercase;color:#e85d26;border:1.5px solid #e85d26;border-radius:2px;padding:.1rem .35rem;margin-left:.5rem;vertical-align:middle;position:relative;top:-4px;font-family:sans-serif}</style><h1>⚙️ Model 121/122 Sizing Tool <span class='beta-badge'>Beta</span></h1>", unsafe_allow_html=True)
st.markdown("Fill in the inputs on the left and click **Run Sizing**.")

# ── load script logic ─────────────────────────────────────────────────────────
_tool_path = os.path.join(os.path.dirname(__file__), "121-122 Script.py")

try:
    with open(_tool_path, "r") as f:
        _source = f.read()
except FileNotFoundError as e:
    st.error(f"Could not load sizing script: {e}")
    st.stop()

_lines  = _source.splitlines(keepends=True)
_code   = "".join(_lines[:1004])

_globals = {}
try:
    exec(compile(_code, _tool_path, "exec"), _globals)
except Exception as e:
    st.error(f"Failed to load sizing script: {e}")
    st.stop()

for _k, _v in _globals.items():
    if not _k.startswith("__"):
        globals()[_k] = _v

# VP exclusion list (same as script)
_VP_EXCLUDE = {'R1210813', 'R121081Q', 'R1211230', 'R1211630', 'R121HP13', 'R121HP1Q'}


# ── helper: build dataframe from result dict ──────────────────────────────────
def build_table121(prefix, result, vp):
    rows = []
    for reg, cap in result.items():
        if not reg.startswith(prefix):
            continue
        if vp and reg in _VP_EXCLUDE:
            continue
        body    = _globals["body_type121"](reg)
        cap_str = f"{cap:,.0f}" if isinstance(cap, (int, float)) else str(cap)
        works   = _globals["will_work_vp"](cap, reg, vp)
        rows.append([body, cap_str, works])
    return pd.DataFrame(rows, columns=["Body Size", "Calculated Capacity (CFH)", "Will It Work?"])


# ── SIDEBAR: inputs ───────────────────────────────────────────────────────────
with st.sidebar:
    st.header("📋 Inputs")

    st.subheader("Pressures & Flow")
    inlet_units  = st.selectbox("Inlet pressure units",  ["psi", "bar"])
    inlet_input  = st.number_input("Inlet pressure", min_value=0.0, max_value=100000.0, value=0.0, step=0.1, format="%.1f")

    outlet_units = st.selectbox("Outlet pressure units", ["psi", "in wc", "bar"])
    outlet_input = st.number_input("Outlet pressure", min_value=0.0, max_value=10000.0, value=0.0, step=0.1, format="%.1f")

    flowrate_units = st.selectbox("Flow rate units", ["CFH", "CMH", "BTUH"])
    flow_rate    = st.number_input("Max gas load / flow rate", min_value=0, max_value=500000000, value=0, step=50, format="%d")
    min_flow_raw = st.number_input("Min gas load / flow rate (enter 0 to use max flow)", min_value=0, max_value=500000000, value=0, step=50, format="%d")

    maop = st.number_input("Max inlet pressure / MAOP (psi)", min_value=0, max_value=1000, value=0, step=1, format="%d",
                           help="MAOP is always entered in psi. Enter 0 to use inlet pressure.")

    st.subheader("Design Parameters")
    _pipe_options = ["N/A", '3/8"', '1/2"', '3/4"', '1"', '1-1/4"', '1-1/2"', '2"', '2-1/2"', '3"']
    pipesize_index = st.selectbox("Desired pipe size", range(len(_pipe_options)),
        index=0, format_func=lambda i: _pipe_options[i])
    pipesize_input_raw = _pipe_options[pipesize_index]
    pipesize_input = 0 if pipesize_input_raw == "N/A" else pipesize_input_raw

    opp_choice = st.radio("Overpressure protection required?", ["No", "Yes"])
    opp_type   = "Monitor" if opp_choice == "Yes" else "None"

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
if inlet_input > 0 and (_inlet_psi_check > 60 or _inlet_psi_check < 8/28):
    errors.append("Inlet pressure must be between 8\" wc and 60 psi.")
if outlet_input > 0 and (_outlet_psi_check < 1.5/28 or _outlet_psi_check > 10):
    errors.append("Outlet pressure must be between 1.5\" wc and 10 psi.")
if inlet_input > 0 and outlet_input > 0 and _outlet_psi_check >= _inlet_psi_check:
    errors.append("Outlet pressure must be less than inlet pressure.")
if int(maop) != 0 and maop < _inlet_psi_check:
    errors.append("MAOP must be ≥ inlet pressure.")
if flow_rate == 0:
    errors.append("Please enter a max gas load / flow rate.")
if min_flow_raw > 0 and min_flow_raw > flow_rate:
    errors.append("Minimum flow must be ≤ maximum flow rate.")


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
                min_flow   = flow_cfh if min_flow_raw == 0 else float(min_flow_raw)
                maop_psi   = inlet_psi if maop == 0 else float(maop)

                if flowrate_units == "CMH":
                    flow_cfh   *= 35.3147
                    min_flow   *= 35.3147
                elif flowrate_units == "BTUH":
                    if gastype_input == "Natural Gas":
                        flow_cfh /= 1000; min_flow /= 1000
                    elif gastype_input == "Propane":
                        flow_cfh /= 2516; min_flow /= 2516
                    else:
                        st.error("BTUH conversion only supported for Natural Gas or Propane. Use CFH or CMH.")
                        st.stop()

                # outlet pressure adjustment (mirror script)
                outlet_input121 = 0.18 if 1.5/28 <= outlet_psi < 0.18 else outlet_psi

                # inject globals
                _globals.update({
                    "inlet_input":       inlet_psi,
                    "outlet_input":      outlet_psi,
                    "flow_rate":         flow_cfh,
                    "min_flow":          min_flow,
                    "maop":              maop_psi,
                    "pipesize_input":    pipesize_input,
                    "opp_type":          opp_type,
                    "partial":           False,
                    "irv_input":         0,
                    "irv_lim":           0,
                    "oversizeby":        oversizeby,
                    "oversize_percent":  oversize_percent,
                    "gastypemult":       gastypemult,
                    "pload":             pload,
                })

                # run sizing
                result121, result121_VP, result122, match121, apply121, warning121 = \
                    _globals["run_regulator_selection121"](inlet_psi, outlet_input121, opp_type)


                # ── regulator selection ───────────────────────────────────────
                if match121:
                    if warning121:
                        st.warning(warning121)


                    st.success("✅  Regulator selected!")

                    st.subheader("Regulator Selection")
                    fields = [
                        ("Model",          match121.get("model")),
                        ("Body Size",      match121.get("body")),
                        ("Orifice Size",   match121.get("orifice")),
                        ("Seat",           match121.get("seat")),
                        ("Spring",         f"{match121.get('color','')} {match121.get('range','')}".strip()),
                        ("Monitor Spring", f"{match121.get('mon_color','')} {match121.get('mon_range','')}".strip() if match121.get("mon_color") else None),
                    ]
                    for label, val in fields:
                        if val:
                            st.markdown(f"**{label}:** {val}")

                    cap = match121.get("capacity")
                    if cap and cap != "N/A":
                        try:
                            st.markdown(f"**Calculated Capacity (CFH):** {int(round(float(cap))):,}")
                        except Exception:
                            st.markdown(f"**Calculated Capacity (CFH):** {cap}")

                    # 121 outlet pipe note
                    model_name = match121.get("model", "")
                    if any(m in model_name for m in ["121-8", "121-12", "121-16", "121-HP"]):
                        pipe_req = _globals["body_size_min121"](ip=inlet_psi, reg=match121["reg"])
                        st.info(f"ℹ️  Model 121 regulators have outlet pipe sizing requirements. This regulator was sized for use with **{pipe_req}** outlet pipe. For capacities with smaller outlet piping, see regulator brochure.")

                    st.subheader("HSC Part Number(s)")
                    pn = _globals["hsc_pnc121"](match121)
                    if isinstance(pn, list):
                        for p in pn:
                            st.code(p)
                    else:
                        st.code(pn)

                else:
                    st.error("❌  Model 121/122 will not work for this application.")

                # ── sizing tables ─────────────────────────────────────────────
                st.divider()
                table_label = "**Regulator Sizing Tables with Monitor**" if opp_type == "Monitor" else "**Regulator Sizing Tables**"

                if outlet_psi <= 2 and not isinstance(result122, str):
                    # Standard + VP + 122
                    st.subheader("Regulator Sizing Tables")
                    st.markdown(table_label)

                    st.markdown("**Standard Valves**")
                    for title, prefix in [
                        ("Model 121-8",  "R12108"),
                        ("Model 121-12", "R12112"),
                        ("Model 121-16", "R12116"),
                        ("Model 122-8",  "R12208"),
                        ("Model 122-12", "R12212"),
                    ]:
                        df = build_table121(prefix, result121 if "122" not in title else result122, False)
                        if not df.empty:
                            st.markdown(f"**{title}**")
                            st.dataframe(df, use_container_width=True, hide_index=True)

                    st.markdown("**V-Port Valves**")
                    for title, prefix in [
                        ("Model 121-8",  "R12108"),
                        ("Model 121-12", "R12112"),
                    ]:
                        df = build_table121(prefix, result121_VP, True)
                        if not df.empty:
                            st.markdown(f"**{title}**")
                            st.dataframe(df, use_container_width=True, hide_index=True)

                elif outlet_psi <= 3:
                    # Standard + VP, no 122
                    st.subheader("Regulator Sizing Tables")
                    st.markdown(table_label)

                    st.markdown("**Standard Valves**")
                    for title, prefix in [
                        ("Model 121-8",  "R12108"),
                        ("Model 121-12", "R12112"),
                        ("Model 121-16", "R12116"),
                    ]:
                        df = build_table121(prefix, result121, False)
                        if not df.empty:
                            st.markdown(f"**{title}**")
                            st.dataframe(df, use_container_width=True, hide_index=True)

                    st.markdown("**V-Port Valves**")
                    for title, prefix in [
                        ("Model 121-8",  "R12108"),
                        ("Model 121-12", "R12112"),
                    ]:
                        df = build_table121(prefix, result121_VP, True)
                        if not df.empty:
                            st.markdown(f"**{title}**")
                            st.dataframe(df, use_container_width=True, hide_index=True)

                else:
                    # HP models only
                    st.subheader("Regulator Sizing Tables")
                    st.markdown(table_label)

                    st.markdown("**Standard Valves**")
                    df = build_table121("R121HP", result121, False)
                    if not df.empty:
                        st.markdown("**Model 121-8-HP**")
                        st.dataframe(df, use_container_width=True, hide_index=True)

                    st.markdown("**V-Port Valves**")
                    df = build_table121("R121HP", result121_VP, True)
                    if not df.empty:
                        st.markdown("**Model 121-HP**")
                        st.dataframe(df, use_container_width=True, hide_index=True)

                # ── sizing adjustments ───────────────────────────────────────
                st.divider()
                st.subheader("Sizing Adjustments")
                adj = {"Oversized By": f"{oversize_percent:.0f}%"}
                if match121 and match121.get("opp") == "Monitor":
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
                    f"Max Gas Load ({flowrate_units})":  f"{flow_rate:,}",
                    f"Min Gas Load ({flowrate_units})":  f"{min_flow_raw:,}" if min_flow_raw > 0 else "Same as max",
                    "MAOP (psi)":                        f"{int(maop)}",
                    "Requested Pipe Size":               _pipe_options[pipesize_index],
                    "Overpressure Protection Required":  "Yes" if opp_choice == "Yes" else "No",
                    "% Load Feeding Generator / High-Eff Boiler": f"{pload_pct}%" if higheff == "Yes" else "N/A",
                    "Gas Type":                          gastype_input,
                }

                df_summary = pd.DataFrame(summary.items(), columns=["Parameter", "Value"])
                st.dataframe(df_summary, use_container_width=True, hide_index=True)

            except Exception as ex:
                st.error(f"Error during sizing: {ex}")
                import traceback; st.code(traceback.format_exc())

else:
    st.info("👈  Fill in the inputs on the left and click **Run Sizing**.")