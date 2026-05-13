import streamlit as st
import sys
import os

# ── page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="Ultimate Sizing Tool", page_icon="⚙️", layout="wide")

st.title("⚙️ Ultimate Sizing Tool")
st.markdown("Gas regulator sizing tool — fill in the inputs below and click **Run Sizing**.")

# ── inject all the data + logic from the original script ────────────────────
# We exec the file up to (but not including) the INPUT section so we get all
# the data tables and functions, then drive it with Streamlit widgets.

_script_dir = os.path.dirname(os.path.abspath(__file__))
_tool_path   = os.path.join(_script_dir, "Ultimate_Sizing_Tool.py")

with open(_tool_path, "r") as f:
    _source = f.read()

# Split at line 3587 — the print("ULTIMATE SIZING TOOL") line that starts the I/O section
_lines  = _source.splitlines(keepends=True)
_code   = "".join(_lines[:3587])

_globals = {}
exec(compile(_code, _tool_path, "exec"), _globals)

# Make the tool's functions callable directly in this module
for _k, _v in _globals.items():
    if not _k.startswith("__"):
        globals()[_k] = _v

# Keep a reference so run_tool can update the exec namespace
# (functions defined inside _globals look up variables there, not in globals())


# ── helper ───────────────────────────────────────────────────────────────────
def fmt_pn(pn):
    if isinstance(pn, list):
        return "\n".join(f"• {p}" for p in pn)
    return pn

def run_tool(
    inlet_input, outlet_input, flow_rate, min_flow, maop,
    pipesize_input, opp_type, partial, irv_input,
    oversizeby, gastypemult, pload
):
    """Run all regulator selection functions and return (result_dict, warnings)."""

    # ── pressure adjustments (mirror the original script) ───────────────────
    outlet_input496 = 0.25 if 0.125 <= outlet_input < 0.25 else outlet_input
    inlet_input496  = 100  if 100 < inlet_input <= 125  else inlet_input

    if 3.5/28 <= outlet_input < 0.25:
        outlet_input143 = 0.25
    elif 2 < outlet_input <= 6:
        outlet_input143 = 2
    else:
        outlet_input143 = outlet_input

    outlet_input243 = 0.25 if 0.125 <= outlet_input < 0.25 else outlet_input
    outlet_input046 = 5    if 3 <= outlet_input < 5        else outlet_input
    outlet_input121 = 0.18 if 1.5/28 <= outlet_input < 0.18 else outlet_input

    # ── inject globals that the functions read ───────────────────────────────
    # Functions were exec'd into _globals, so that's where they look up names
    _globals["inlet_input"]    = inlet_input
    _globals["outlet_input"]   = outlet_input
    _globals["flow_rate"]      = flow_rate
    _globals["min_flow"]       = min_flow
    _globals["maop"]           = maop
    _globals["pipesize_input"] = pipesize_input
    _globals["opp_type"]       = opp_type
    _globals["partial"]        = partial
    _globals["irv_input"]      = irv_input
    _globals["irv_lim"]        = irv_input - outlet_input if irv_input else 0
    _globals["oversizeby"]     = oversizeby
    _globals["gastypemult"]    = gastypemult
    _globals["pload"]          = pload

    msgs   = []   # warning messages
    result = {}   # what we'll display

    # 496 -------------------------------------------------------------------
    r496, m496, ok496, w496 = run_regulator_selection496(
        inlet_input496, outlet_input496, opp_type)
    if ok496:
        if w496: msgs.append(w496)
        result["match"]  = m496
        result["pn"]     = hsc_pnc496(m496)
        return result, msgs

    # 143 -------------------------------------------------------------------
    r143, m143, ok143, w143 = run_regulator_selection143(
        inlet_input, outlet_input143, opp_type)
    if ok143:
        if w143: msgs.append(w143)
        result["match"] = m143
        result["pn"]    = hsc_pnc143(m143)
        return result, msgs

    # 243 -------------------------------------------------------------------
    r243, m243, ok243, w243 = run_regulator_selection243(
        inlet_input, outlet_input243, opp_type)
    if ok243:
        if w243: msgs.append(w243)
        result["match"] = m243
        result["pn"]    = hsc_pnc243(m243)
        return result, msgs

    # 046 -------------------------------------------------------------------
    r046, m046, ok046, w046 = run_regulator_selection046(
        inlet_input, outlet_input046, opp_type)
    if ok046:
        if w046: msgs.append(w046)
        result["match"] = m046
        result["pn"]    = hsc_pnc046(m046)
        return result, msgs

    # ── new routing: high-eff + no OPP → try 121/122 before 441/461 ────────
    if opp_type == "None" and pload > 0.50:
        r121, r121vp, r122, m121, ok121, w121 = run_regulator_selection121(
            inlet_input, outlet_input121, opp_type)
        if ok121:
            if w121: msgs.append(w121)
            result["match"]    = m121
            result["pn"]       = hsc_pnc121(m121)
            result["note121"]  = True
            result["note121_pipe"] = body_size_min121(ip=inlet_input, reg=m121["reg"])
            return result, msgs

        # 121 didn't work — fall through to 441/461
        m461 = calc_regulator_selection(
            inlet_input, outlet_input, flow_rate, min_flow, False)
        if m461["model"] != "N/A":
            result["match"] = m461
            result["pn"]    = hsc_pnc461(m461)
            return result, msgs

        result["no_match"] = True
        return result, msgs

    # ── standard routing: 441/461 before 121/122 ────────────────────────────
    m461 = calc_regulator_selection(
        inlet_input, outlet_input, flow_rate, min_flow, opp_type != "None")
    if m461["model"] != "N/A":
        if opp_type != "None":
            msgs.append("Sized for worker/monitor setup")
        result["match"] = m461
        result["pn"]    = hsc_pnc461(m461)
        return result, msgs

    # 121/122 ---------------------------------------------------------------
    r121, r121vp, r122, m121, ok121, w121 = run_regulator_selection121(
        inlet_input, outlet_input121, opp_type)
    if ok121:
        if w121: msgs.append(w121)
        result["match"]    = m121
        result["pn"]       = hsc_pnc121(m121)
        result["note121"]  = True
        result["note121_pipe"] = body_size_min121(ip=inlet_input, reg=m121["reg"])
        return result, msgs

    result["no_match"] = True
    return result, msgs


# ── SIDEBAR: all 14 inputs ───────────────────────────────────────────────────
with st.sidebar:
    st.header("📋 Inputs")

    st.subheader("Pressures & Flow")
    inlet_input  = st.number_input("Inlet pressure (psi)",        min_value=0.001, max_value=1000.0, value=5.0,   step=0.5, format="%.3f")
    outlet_input = st.number_input("Outlet pressure (psi)",       min_value=0.001, max_value=250.0,  value=0.25,  step=0.05, format="%.4f",
                                   help="Tip: 7\" wc ≈ 0.25 psi, 11\" wc ≈ 0.393 psi, 14\" wc ≈ 0.5 psi")
    flow_rate    = st.number_input("Max gas load / flow rate (CFH)", min_value=1.0, max_value=5000000.0, value=500.0, step=50.0)
    min_flow_raw = st.number_input("Min gas load / flow rate (CFH — enter 0 to use max flow)", min_value=0.0, max_value=5000000.0, value=0.0, step=50.0)
    min_flow     = flow_rate if min_flow_raw == 0 else min_flow_raw
    maop         = st.number_input("Max inlet pressure / MAOP (psi)", min_value=0.001, max_value=1000.0, value=5.0, step=0.5, format="%.3f")

    st.subheader("Pipe & OPP")
    pipesize_input = st.selectbox("Desired pipe size",
        ["0.375", "0.5", "0.75", "1", "1.25", "1.5", "2", "2.5", "3"],
        index=3,
        format_func=lambda x: f'{x}"')

    opp_choice = st.radio("Overpressure protection required?", ["No", "Yes"])
    partial    = False
    irv_input  = 0.0
    opp_type   = "None"

    if opp_choice == "Yes":
        opp_pref = st.radio("Protection type", ["IRV (Internal Relief Valve)", "Monitor regulator"])
        if "IRV" in opp_pref:
            irv_input = st.number_input("IRV protect downstream pressure to (psi)",
                                        min_value=0.001, max_value=500.0, value=float(outlet_input) + 0.5, step=0.1, format="%.3f")
            opp_type = "IRV"
        else:
            opp_type = "Monitor"
    else:
        partial_choice = st.radio("Select regulator with IRV for partial overpressure protection?", ["No", "Yes"])
        if partial_choice == "Yes":
            partial  = True
            opp_type = "IRV"

    st.subheader("Load Type & Gas")
    higheff = st.radio("Feeding a generator or high-efficiency boiler?", ["No", "Yes"])
    pload   = 0.0
    if higheff == "Yes":
        pload_pct = st.slider("% of total load feeding generator / high-eff boiler", 0, 100, 50)
        pload = pload_pct / 100.0
    oversizeby = 1.2 + (0.8 * pload)

    gastype_input = st.selectbox("Gas type", ["Natural Gas", "Propane", "Other"])
    gastypemult   = 1.0
    if gastype_input == "Propane":
        gastypemult = 0.63
    elif gastype_input == "Other":
        sg = st.number_input("Specific gravity", min_value=0.01, max_value=10.0, value=0.6, step=0.01, format="%.3f")
        gastypemult = min(1.0, (0.6 / sg) ** 0.5)
        st.info("Contact USG for regulator compatibility with gases other than methane or propane.")

    run_btn = st.button("▶  Run Sizing", type="primary", use_container_width=True)


# ── MAIN AREA: validation then results ──────────────────────────────────────
errors = []
if inlet_input > 1000 or inlet_input < 0.25:
    errors.append("Inlet pressure must be between 7\" wc (≈0.25 psi) and 1,000 psi.")
if outlet_input < 1.5/28 or outlet_input > 250:
    errors.append("Outlet pressure must be between 1.5\" wc and 250 psi.")
if outlet_input >= inlet_input:
    errors.append("Outlet pressure must be less than inlet pressure.")
if maop < inlet_input:
    errors.append("MAOP must be ≥ inlet pressure.")
if min_flow > flow_rate:
    errors.append("Minimum flow must be ≤ maximum flow rate.")
if inlet_input > 175 and outlet_input < 3:
    errors.append("Pressure differential too large — consider two pressure cuts.")

if run_btn:
    if errors:
        for e in errors:
            st.error(e)
    else:
        with st.spinner("Sizing regulator…"):
            try:
                result, msgs = run_tool(
                    inlet_input, outlet_input, flow_rate, min_flow, maop,
                    pipesize_input, opp_type, partial, irv_input,
                    oversizeby, gastypemult, pload
                )

                # ── warnings ────────────────────────────────────────────────
                for m in msgs:
                    st.warning(m)

                if result.get("no_match"):
                    st.error("❌  No USG regulators will work for this application.")

                elif "match" in result:
                    match = result["match"]
                    pn    = result["pn"]

                    st.success("✅  Regulator selected!")

                    # ── result card ─────────────────────────────────────────
                    col1, col2 = st.columns(2)

                    with col1:
                        st.subheader("Regulator Selection")
                        fields = [
                            ("Model",              match.get("model")),
                            ("Diaphragm Size",     match.get("diap")),
                            ("Body Size",          match.get("body")),
                            ("Orifice Size",       match.get("orifice")),
                            ("Seat",               match.get("seat")),
                            ("Spring Color",       match.get("color")),
                            ("Spring Range",       match.get("range")),
                        ]
                        for label, val in fields:
                            if val:
                                st.markdown(f"**{label}:** {val}")

                        cap = match.get("capacity")
                        if cap and cap != "N/A":
                            try:
                                st.markdown(f"**Calculated Capacity (CFH):** {int(round(float(cap))):,}")
                            except Exception:
                                st.markdown(f"**Calculated Capacity (CFH):** {cap}")

                    with col2:
                        st.subheader("HSC Part Number(s)")
                        if isinstance(pn, list):
                            for p in pn:
                                st.code(p)
                        else:
                            st.code(pn)

                    if result.get("note121"):
                        pipe = result.get("note121_pipe", "")
                        if pipe:
                            st.info(f"ℹ️  Model 121 regulators have outlet pipe sizing requirements. This regulator was sized for use with **{pipe}** outlet pipe. For capacities with smaller outlet piping, see regulator brochure.")
                        else:
                            st.info("ℹ️  Model 121 regulators have outlet pipe sizing requirements — see brochure.")

                    # ── summary table ────────────────────────────────────────
                    st.divider()
                    st.subheader("Input Summary")
                    summary = {
                        "Inlet Pressure (psi)": inlet_input,
                        "Outlet Pressure (psi)": outlet_input,
                        "Max Flow Rate (CFH)": f"{flow_rate:,.0f}",
                        "Min Flow Rate (CFH)": f"{min_flow:,.0f}",
                        "MAOP (psi)": maop,
                        "Pipe Size": f'{pipesize_input}"',
                        "OPP Type": opp_type,
                        "Gas Type": gastype_input,
                        "Oversize Factor": f"{oversizeby:.2f}×",
                    }
                    import pandas as pd
                    df = pd.DataFrame(summary.items(), columns=["Parameter", "Value"])
                    st.dataframe(df, use_container_width=True, hide_index=True)

            except Exception as ex:
                st.error(f"Error during sizing: {ex}")
                import traceback; st.code(traceback.format_exc())

else:
    # placeholder before first run
    st.info("👈  Fill in the inputs on the left and click **Run Sizing**.")

    # Show a pressure-unit helper
    with st.expander("💡 Pressure conversion helper"):
        st.markdown("""
| Inches w.c. | PSI (approx.) |
|-------------|---------------|
| 1.5\" wc    | 0.054 psi     |
| 3.5\" wc    | 0.125 psi     |
| 7\" wc      | 0.250 psi     |
| 11\" wc     | 0.393 psi     |
| 14\" wc     | 0.500 psi     |
| 27\" wc     | 0.964 psi     |
| 28\" wc     | 1.000 psi     |
""")
