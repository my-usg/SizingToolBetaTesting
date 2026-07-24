import streamlit as st
import os
import pandas as pd

# ── page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="Model 441/461 Sizing Tool", page_icon="⚙️", layout="wide")

st.markdown("<style>.beta-badge{display:inline-block;font-size:.6rem;font-weight:600;letter-spacing:.15em;text-transform:uppercase;color:#e85d26;border:1.5px solid #e85d26;border-radius:2px;padding:.1rem .35rem;margin-left:.5rem;vertical-align:middle;position:relative;top:-4px;font-family:sans-serif}</style><h1>⚙️ Model 441/461 Sizing Tool <span class='beta-badge'>Beta</span></h1>", unsafe_allow_html=True)
st.markdown("Fill in the inputs on the left and click **Run Sizing**.")

# ── load script logic ─────────────────────────────────────────────────────────
_tool_path = os.path.join(os.path.dirname(__file__), "441-461 Script.py")

try:
    with open(_tool_path, "r") as f:
        _source = f.read()
except FileNotFoundError as e:
    st.error(f"Could not load sizing script: {e}")
    st.stop()

_lines  = _source.splitlines(keepends=True)
_code   = "".join(_lines[:935])

_globals = {}
try:
    exec(compile(_code, _tool_path, "exec"), _globals)
except Exception as e:
    st.error(f"Failed to load sizing script: {e}")
    st.stop()

for _k, _v in _globals.items():
    if not _k.startswith("__"):
        globals()[_k] = _v


# ── helper: build dataframe from table list ───────────────────────────────────
def table_to_df(table):
    rows = [
        [
            row["model"],
            row["body"],
            row["orifice"],
            f"{row['qmax']:,.0f}",
            f"{row['qmin']:,.0f}",
            row["yn"],
        ]
        for row in table
    ]
    return pd.DataFrame(rows, columns=["Applicable Models", "Body", "Orifice", "Qmax (CFH)", "Qmin (CFH)", "Y/N"])


# ── SIDEBAR: inputs ───────────────────────────────────────────────────────────
with st.sidebar:
    st.header("📋 Inputs")

    st.subheader("Pressures & Flow")
    inlet_units  = st.selectbox("Inlet pressure units",  ["psi", "bar"])
    inlet_input  = st.number_input("Inlet pressure", min_value=0.0, max_value=100000.0, value=0.0, step=0.1, format="%.1f")

    outlet_units = st.selectbox("Outlet pressure units", ["psi", "in wc", "bar"])
    outlet_input = st.number_input("Outlet pressure", min_value=0.0, max_value=10000.0, value=0.0, step=0.1, format="%.1f")

    flowrate_units = st.selectbox("Gas load / flow rate units", ["CFH", "CMH", "BTUH"])
    flow_rate    = st.number_input("Max gas load / flow rate", min_value=0, max_value=500000000, value=0, step=50, format="%d")
    min_flow_raw = st.number_input("Min gas load / flow rate (enter 0 to use max flow)", min_value=0, max_value=500000000, value=0, step=50, format="%d")

    maop = st.number_input("MAOP (psi)", min_value=0, max_value=1000, value=0, step=1, format="%d",
                           help="MAOP is always entered in psi. Enter 0 to use inlet pressure.")

    st.subheader("Design Parameters")

    opp_choice = st.radio("Overpressure protection required?", ["No", "Yes"])
    opp_type   = "Monitor" if opp_choice == "Yes" else "None"

    st.subheader("Load Type & Gas")
    higheff   = st.radio("Feeding a generator or high-efficiency boiler?", ["No", "Yes"])
    pload     = 0.0
    pload_pct = 0
    if higheff == "Yes":
        pload_pct = st.slider("% of total load feeding generator / high-eff boiler", 0, 100, 50)
        pload = pload_pct / 100.0
    oversizeby = 1.25 + (0.75 * pload)

    st.subheader("Gas")
    gastype_input = st.selectbox("Gas type", ["Natural Gas", "Propane", "Other"])
    gastypemult   = 1.0
    if gastype_input == "Propane":
        gastypemult = 0.63
    elif gastype_input == "Other":
        sg = st.number_input("Specific gravity", min_value=0.01, max_value=10.0, value=0.6, step=0.01, format="%.2f")
        gastypemult = min(1.0, (0.6 / sg) ** 0.5)
        st.info("Contact USG for regulator compatibility with gases other than methane or propane.")

    # Altitude
    elevation = st.selectbox("Altitude above 3,000 feet or atmospheric pressure below 13 psi", ["Yes", "No"])
    if elevation == "Yes":
        Patm  = st.number_input("Atmospheric Pressure (psi)",   min_value=8.80, max_value=14.73, value=0.0,   step=0.01,  format="%.1f")
    else:
        Patm = 14.4

    run_btn = st.button("▶  Run Sizing", type="primary", use_container_width=True)


# ── validation ────────────────────────────────────────────────────────────────
def to_psi(val, units):
    if units == "in wc": return val * (1/28)
    if units == "bar":   return val * 14.5
    return val

_inlet_psi_check  = inlet_input * 14.5 if inlet_units == "bar" else inlet_input
_outlet_psi_check = to_psi(outlet_input, outlet_units)

errors = []
if inlet_input > 0 and (_inlet_psi_check > 1000 or _inlet_psi_check < 0.25):
    errors.append("Inlet pressure must be between 7\" wc and 1,000 psi.")
if outlet_input > 0 and (_outlet_psi_check < 2/28 or _outlet_psi_check > 250):
    errors.append("Outlet pressure must be between 2\" wc and 250 psi.")
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
                    flow_cfh *= 35.3147
                    min_flow *= 35.3147
                elif flowrate_units == "BTUH":
                    if gastype_input == "Natural Gas":
                        flow_cfh /= 1000; min_flow /= 1000
                    elif gastype_input == "Propane":
                        flow_cfh /= 2516; min_flow /= 2516
                    else:
                        st.error("BTUH conversion only supported for Natural Gas or Propane. Use CFH or CMH.")
                        st.stop()

                oversize_percent = 20.0

                # inject globals
                _globals.update({
                    "inlet_input":       inlet_psi,
                    "outlet_input":      outlet_psi,
                    "flow_rate":         flow_cfh,
                    "min_flow":          min_flow,
                    "maop":              maop_psi,
                    "opp_type":          opp_type,
                    "oversizeby":        1.2,
                    "oversize_percent":  oversize_percent,
                    "gastypemult":       gastypemult,
                    "pload":             pload,
                    "Patm":              Patm,
                })

                # run sizing
                std      = _globals["build_standard_table"](inlet_psi, outlet_psi, flow_cfh, min_flow, opp_type)
                vp       = _globals["build_vport_table"](inlet_psi, outlet_psi, flow_cfh, min_flow, opp_type)
                match461, ok461, warning461 = _globals["run_regulator_selection461"](inlet_psi, outlet_psi, flow_cfh, min_flow, opp_type)

                # ── regulator selection ───────────────────────────────────────

                if not ok461:
                    st.error("❌  Model 441/461 will not work for this application.")
                else:
                    if warning461:
                        st.warning(warning461)

                    st.success("✅  Regulator selected!")

                    st.subheader("Regulator Selection")
                    fields = [
                        ("Model",              match461.get("model")),
                        ("Diaphragm",          match461.get("diap")),
                        ("Body Size",          match461.get("body")),
                        ("Orifice Size",       match461.get("orifice")),
                        ("Seat",               match461.get("seat")),
                        ("Spring",             f"{match461.get('color','')} {match461.get('range','')}".strip()),
                        ("Monitor Spring",     f"{match461.get('mon_color','')} {match461.get('mon_range','')}".strip() if match461.get("mon_color") not in (None, "N/A") else None),
                    ]
                    for label, val in fields:
                        if val:
                            st.markdown(f"**{label}:** {val}")

                    cap = match461.get("capacity")
                    if cap and cap != "N/A":
                        try:
                            st.markdown(f"**Calculated Capacity (CFH):** {int(round(float(cap))):,}")
                        except Exception:
                            st.markdown(f"**Calculated Capacity (CFH):** {cap}")

                    st.subheader("HSC Part Number(s)")
                    pn = _globals["hsc_pnc461"](match461)
                    if isinstance(pn, list):
                        for p in pn:
                            st.code(p)
                    else:
                        st.code(pn)

                # ── sizing tables ─────────────────────────────────────────────
                st.divider()
                st.subheader("Regulator Sizing Tables")

                if opp_type != "None":
                    st.caption("Capacity reduction due to monitor shown.")

                st.markdown("**Standard Valves**")
                df_std = table_to_df(std)
                st.dataframe(df_std, use_container_width=True, hide_index=True)

                st.markdown("**V-Port Valves**")
                df_vp = table_to_df(vp)
                st.dataframe(df_vp, use_container_width=True, hide_index=True)

                # ── sizing adjustments ───────────────────────────────────────
                st.divider()
                st.subheader("Sizing Adjustments")
                adj = {"Oversized By": f"{oversize_percent:.0f}%"}
                if ok461 and match461.get("opp") == "Monitor":
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
                    "Overpressure Protection Required":  "Yes" if opp_choice == "Yes" else "No",
                    "Gas Type":                          gastype_input,
                }

                df_summary = pd.DataFrame(summary.items(), columns=["Parameter", "Value"])
                st.dataframe(df_summary, use_container_width=True, hide_index=True)

            except Exception as ex:
                st.error(f"Error during sizing: {ex}")
                import traceback; st.code(traceback.format_exc())

else:
    st.info("👈  Fill in the inputs on the left and click **Run Sizing**.")