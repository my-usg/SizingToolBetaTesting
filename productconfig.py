import streamlit as st
from product_selection_script import run_product_configurator

st.set_page_config(page_title="Regulator Part Number Configurator", layout="centered")

st.markdown(
    """
    <style>
    /* Overall base font size */
    html, body, [class*="css"] {
        font-size: 18px;
    }
    /* Widget labels (selectbox, radio, etc.) */
    label, .stSelectbox label, .stRadio label {
        font-size: 1.15rem !important;
        font-weight: 600 !important;
    }
    /* Selected value text inside dropdowns */
    div[data-baseweb="select"] * {
        font-size: 1.1rem !important;
    }
    /* Dropdown menu options */
    ul[role="listbox"] li {
        font-size: 1.1rem !important;
    }
    /* Buttons */
    .stButton button {
        font-size: 1.15rem !important;
        padding: 0.6rem 1.2rem;
    }
    /* Captions / notes */
    .stCaption, [data-testid="stCaptionContainer"] {
        font-size: 1rem !important;
    }
    /* Generated part number code blocks */
    .stCodeBlock, code {
        font-size: 1.3rem !important;
    }
    /* Success / error message boxes */
    .stAlert {
        font-size: 1.1rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Regulator Part Number Configurator")
st.write("Select the options for your regulator below. The part number(s) will be built automatically.")

REGULATOR_TYPES = [
    "496", "143", "243", "046",
    "461-S", "461-57S", "441-57S", "461-X57", "441-S", "441-X57",
    "121", "122",
]

regulator_type = st.selectbox("Regulator Type", REGULATOR_TYPES)
st.divider()

# Defaults - overwritten per branch below
model = body = orifice = spring_color = diap = seat = monitor_color = None
opp = "None"
reg_param = None


def vp_suffix(base, is_vp):
    return f"{base} VP" if is_vp else base


def monitor_block(spring_options, key_prefix):
    """Shared Monitor Needed / Monitor Spring widget pair."""
    opp_choice = st.selectbox("Monitor Needed", ["None", "Monitor"], key=f"{key_prefix}_opp")
    mon_color = None
    if opp_choice == "Monitor":
        mon_color = st.selectbox("Monitor Spring Color", spring_options, key=f"{key_prefix}_monspring")
    return opp_choice, mon_color


# ---------------------------------------------------------------------------
# 496
# ---------------------------------------------------------------------------
if regulator_type == "496":
    reg_param = "496"
    model = st.selectbox("Model", ["496-10", "496-20"])
    if model == "496-20":
        body_options = ['3/8"', '1/2"', '3/4"', '3/4"x1"', '1"']
    else:
        body_options = ['3/4"', '3/4"x1"', '1"']
    body = st.selectbox("Body Size", body_options)
    orifice = st.selectbox("Orifice Size", ['1/8"', '3/16"', '1/4"', '5/16"', '3/8"', '1/2"'])
    spring_color = st.selectbox("Spring Color", ["Silver", "Blue", "Green", "Red", "Black"])

# ---------------------------------------------------------------------------
# 143
# ---------------------------------------------------------------------------
elif regulator_type == "143":
    reg_param = "143"
    model = st.selectbox("Model", ["143-1", "143-2", "143-6", "143-2HP"])
    body = st.selectbox("Body Size", ['3/4"', '1"', '1-1/4"'])

    if model == "143-6":
        orifice_options = ['1/4"', '5/16"', '3/8"', '7/16"']
    else:
        orifice_options = ['1/8"', '3/16"', '1/4"', '5/16"', '3/8"', '1/2"', '5/8"']
    orifice = st.selectbox("Orifice Size", orifice_options)

    if model in ("143-1", "143-2"):
        spring_options = ["Red", "Blue", "Green", "Orange", "Black + White"]
    elif model == "143-2HP":
        spring_options = ["Cadmium", "Black"]
    else:  # 143-6
        spring_options = ["Red", "Blue", "Green", "Orange"]
    spring_color = st.selectbox("Spring Color", spring_options)

# ---------------------------------------------------------------------------
# 243
# ---------------------------------------------------------------------------
elif regulator_type == "243":
    reg_param = "243"
    model = st.selectbox(
        "Model", ["243-12-1", "243-12-2", "243-12-6", "243-8-1", "243-8-2", "243-8-6", "243-8HP"]
    )

    body_options = ['1-1/4" SCD', '1-1/2" SCD', '2" SCD', '2" FLG', '2" FLG 10" FTF']
    if model == "243-12-6":
        body_options = [b for b in body_options if b != '1-1/4" SCD']
    body = st.selectbox("Body Size", body_options)

    wide_bodies = ('2" SCD', '2" FLG', '2" FLG 10" FTF')
    mid_wide_bodies = ('1-1/2" SCD', '2" SCD', '2" FLG', '2" FLG 10" FTF')

    if model in ("243-8-1", "243-8-2"):
        orifice_options = []
        if body in ('1-1/4" SCD', '1-1/2" SCD'):
            orifice_options.append('0.207"')
        orifice_options += ['1/4"', '3/8"', '1/2"', '3/4", 10°']
        if body in wide_bodies:
            orifice_options.append('3/4", 30°')
        if body in mid_wide_bodies:
            orifice_options.append('1", 30°')
        external_control = None
    elif model == "243-12-1":
        external_control = st.selectbox("External Control", ["No", "Yes"])
        orifice_options = ['1/4"', '3/8"', '1/2"', '3/4", 10°']
        if body in wide_bodies:
            orifice_options.append('3/4", 30°')
        if body in mid_wide_bodies:
            orifice_options += ['1", 10°', '1", 30°']
        if external_control == "Yes":
            orifice_options.append('1-1/4", 10°')
        else:
            orifice_options.append('1-1/4", 30°')
    elif model == "243-12-2":
        external_control = None
        orifice_options = ['1/4"', '3/8"', '1/2"', '3/4", 10°']
        if body in wide_bodies:
            orifice_options.append('3/4", 30°')
        if body in mid_wide_bodies:
            orifice_options += ['1", 10°', '1", 30°']
        orifice_options.append('1-1/4", 30°')
    elif model == "243-8HP":
        external_control = None
        orifice_options = ['1/4"', '3/8"', '1/2"', '3/4", 10°']
    else:  # 243-12-6, 243-8-6
        external_control = None
        orifice_options = ['1", 30°', '3/4", 10°', '1/2"']

    orifice = st.selectbox("Orifice Size", orifice_options)

    if model in ("243-12-1", "243-12-2"):
        spring_options = ["Red", "Blue", "Green", "Orange-Black", "Orange", "Black", "Cadmium"]
    elif model in ("243-8-1", "243-8-2"):
        spring_options = ["Red-Black", "Blue-Black", "Green-Black", "Green", "Orange", "Black", "Cadmium"]
    elif model == "243-8HP":
        spring_options = ["Cadmium", "Cadmium + White"]
    elif model == "243-12-6":
        spring_options = ["Red", "Blue", "Green", "Orange-Black", "Orange"]
    else:  # 243-8-6
        spring_options = ["Red-Black", "Blue-Black", "Green-Black", "Green"]
    spring_color = st.selectbox("Spring Color", spring_options)

    if model in ("243-8-1", "243-12-1", "243-8HP"):
        opp, monitor_color = monitor_block(spring_options, "r243")

    # 243-12-1 with External Control = Yes uses the external-control model variant
    if model == "243-12-1" and external_control == "Yes":
        model = "243-12-1 with External Control Line"
        if opp == "Monitor":
            st.caption(
                "Note: the underlying algorithm doesn't have a Monitor branch for the "
                "external-control variant, so only a single (non-monitor) part number "
                "will be generated for this combination."
            )

# ---------------------------------------------------------------------------
# 046
# ---------------------------------------------------------------------------
elif regulator_type == "046":
    reg_param = "046"
    model = st.selectbox("Model", ["046", "046-2"])
    body = st.selectbox("Body Size", ['3/4"', '1"', '1-1/4"'])
    orifice = st.selectbox("Orifice Size", ['1/8"', '5/16"', '1/4"', '3/8"', '1/2"'])

    spring_options = ["Yellow", "Aluminum", "White", "Green", "Tan"]
    if model == "046":
        spring_options.append("Gray")  # Gray only available on 046 (aka 046-1)
    spring_color = st.selectbox("Spring Color", spring_options)
    seat = "Tan"

    if model == "046":
        opp, monitor_color = monitor_block(spring_options, "r046")
    else:
        opp = "None"

# ---------------------------------------------------------------------------
# 461-S
# ---------------------------------------------------------------------------
elif regulator_type == "461-S":
    reg_param = "461"
    model = "461-S"
    body = st.selectbox("Body Size", ['2" Screwed', '2" ANSI 125', '2" ANSI 250', '2" ANSI 300'])

    diap_label = st.selectbox("Diaphragm", ['8" Aluminum', '12" Aluminum', '8.5" Cast Iron', '12" Cast Iron'])
    diap_lookup = {
        '8" Aluminum': '8" Aluminum',
        '12" Aluminum': '12" Alunimum',  # matches a typo'd key in the underlying part-number map
        '8.5" Cast Iron': '8.5" Cast Iron',
        '12" Cast Iron': '12" Cast Iron',
    }
    diap = diap_lookup[diap_label]

    orifice_base = st.selectbox("Orifice Size", ['1" double', '11/16" double', '1" single', '11/16" single'])
    if orifice_base in ('1" double', '11/16" double'):
        seat = st.selectbox("Seat", ["BUNA", "Poly-Tan"])
    else:
        seat = "Poly-Tan"
    if orifice_base in ('1" double', '1" single'):
        is_vp = st.selectbox("V-Port", ["No", "Yes"]) == "Yes"
    else:
        is_vp = False
    orifice = vp_suffix(orifice_base, is_vp)

    if diap_label == '12" Cast Iron':
        spring_options = ["Aluminum", "Green", "Yellow", "Gray", "Blue"]
    elif diap_label == '12" Aluminum':
        spring_options = ["Red", "Blue", "Green", "Orange", "Black", "Cadmium"]
    elif diap_label == '8.5" Cast Iron':
        spring_options = ["Blue", "Red"]
    else:  # 8" Aluminum
        spring_options = ["Orange", "Black", "Cadmium", "Cadmium + White"]
    spring_color = st.selectbox("Spring Color", spring_options)

    opp, monitor_color = monitor_block(spring_options, "r461s")

# ---------------------------------------------------------------------------
# 461-57S
# ---------------------------------------------------------------------------
elif regulator_type == "461-57S":
    reg_param = "461"
    model = "461-57S"
    body = st.selectbox(
        "Body Size", ['2" Screwed', '2" ANSI 125', '2" ANSI 250', '2" ANSI 300', '2" ANSI 600']
    )
    orifice_base = st.selectbox("Orifice Size", ['1" double', '11/16" double', '1" single', '11/16" single'])
    if orifice_base in ('1" double', '11/16" double'):
        seat = st.selectbox("Seat", ["BUNA", "Poly-Tan"])
    else:
        seat = "Poly-Tan"
    if orifice_base in ('1" double', '1" single'):
        is_vp = st.selectbox("V-Port", ["No", "Yes"]) == "Yes"
    else:
        is_vp = False
    orifice = vp_suffix(orifice_base, is_vp)

    spring_options = ["Yellow", "Gray", "Blue", "Red", "Brown", "Black", "Black + White"]
    spring_color = st.selectbox("Spring Color", spring_options)
    opp, monitor_color = monitor_block(spring_options, "r46157s")

# ---------------------------------------------------------------------------
# 461-X57
# ---------------------------------------------------------------------------
elif regulator_type == "461-X57":
    reg_param = "461"
    model = "461-X57"
    body = st.selectbox("Body Size", ['2" ANSI 250', '2" ANSI 300', '2" ANSI 600'])
    orifice_base = st.selectbox("Orifice Size", ['1" double', '11/16" double', '1" single', '11/16" single'])
    seat = "Poly-Tan"
    if orifice_base in ('1" double', '1" single'):
        is_vp = st.selectbox("V-Port", ["No", "Yes"]) == "Yes"
    else:
        is_vp = False
    orifice = vp_suffix(orifice_base, is_vp)

    spring_options = ["Red", "Brown", "Black"]
    spring_color = st.selectbox("Spring Color", spring_options)
    opp, monitor_color = monitor_block(spring_options, "r461x57")

# ---------------------------------------------------------------------------
# 441-S
# ---------------------------------------------------------------------------
elif regulator_type == "441-S":
    reg_param = "441"
    model = "441-S"
    body_size = st.selectbox("Body Size", ['2"', '3"', '4"'])
    rating_options = ["ANSI 125", "ANSI 250"]
    if body_size == '2"':
        rating_options = ["Screwed"] + rating_options
    rating = st.selectbox("Body Pressure Rating", rating_options)
    body = f"{body_size} {rating}"

    diap_options = ['10"', '12"', '14"', '16"']
    if body_size in ('3"', '4"'):
        diap_options.append('18"')
    if body_size == '4"':
        diap_options.append('20"')
    diap = st.selectbox("Diaphragm", diap_options)

    orifice_by_body = {'2"': ['1-1/2"', '1-3/4"'], '3"': ['1-1/2"', '1-3/4"', '2-1/8"'], '4"': ['1-3/4"', '2-1/8"', '3"']}
    orifice_base = st.selectbox("Orifice Size", orifice_by_body[body_size])
    seat = st.selectbox("Seat", ["BUNA", "Poly-Tan"])
    is_vp = st.selectbox("V-Port", ["No", "Yes"]) == "Yes"
    orifice = vp_suffix(orifice_base, is_vp)

    spring_options = ["Aluminum", "Green", "Yellow", "Gray", "Blue", "Red"]
    if diap == '10"':
        spring_options.remove("Aluminum")
    if diap not in ('10"', '12"', '14"'):
        spring_options.remove("Red")
    spring_color = st.selectbox("Spring Color", spring_options)

    opp, monitor_color = monitor_block(spring_options, "r441s")

# ---------------------------------------------------------------------------
# 441-57S
# ---------------------------------------------------------------------------
elif regulator_type == "441-57S":
    reg_param = "441"
    model = "441-57S"
    body_size = st.selectbox("Body Size", ['2"', '3"', '4"', '6"'])
    rating_options = ["ANSI 125", "ANSI 250"]
    if body_size == '2"':
        rating_options = ["Screwed"] + rating_options
    if body_size != '6"':
        rating_options.append("ANSI 300")
    if body_size in ('2"', '3"'):
        rating_options.append("ANSI 600")
    rating = st.selectbox("Body Pressure Rating", rating_options)
    body = f"{body_size} {rating}"

    orifice_by_body = {
        '2"': ['1-1/2"', '1-3/4"'],
        '3"': ['1-1/2"', '1-3/4"', '2-1/8"'],
        '4"': ['1-3/4"', '2-1/8"', '3"'],
        '6"': ['4-1/4"', '3"', '2-1/8"'],
    }
    orifice_base = st.selectbox("Orifice Size", orifice_by_body[body_size])
    seat = st.selectbox("Seat", ["BUNA", "Poly-Tan"])
    is_vp = st.selectbox("V-Port", ["No", "Yes"]) == "Yes"
    orifice = vp_suffix(orifice_base, is_vp)

    spring_options = ["Yellow", "Gray", "Blue", "Red", "Brown", "Black", "Brown + White"]
    spring_color = st.selectbox("Spring Color", spring_options)
    opp, monitor_color = monitor_block(spring_options, "r44157s")

# ---------------------------------------------------------------------------
# 441-X57
# ---------------------------------------------------------------------------
elif regulator_type == "441-X57":
    reg_param = "441"
    model = "441-X57"
    body_size = st.selectbox("Body Size", ['2"', '3"'])
    rating = st.selectbox("Body Pressure Rating", ["ANSI 250", "ANSI 300", "ANSI 600"])
    body = f"{body_size} {rating}"

    orifice_by_body = {'2"': ['1-1/2"', '1-3/4"'], '3"': ['1-1/2"', '1-3/4"', '2-1/8"']}
    orifice_base = st.selectbox("Orifice Size", orifice_by_body[body_size])
    seat = "Poly-Tan"
    is_vp = st.selectbox("V-Port", ["No", "Yes"]) == "Yes"
    orifice = vp_suffix(orifice_base, is_vp)

    spring_options = ["Red", "Brown", "Black"]
    spring_color = st.selectbox("Spring Color", spring_options)
    opp, monitor_color = monitor_block(spring_options, "r441x57")

# ---------------------------------------------------------------------------
# 121
# ---------------------------------------------------------------------------
elif regulator_type == "121":
    reg_param = "121"
    model = st.selectbox("Model", ["121-8", "121-12", "121-16", "121-8HP"])

    if model in ("121-8", "121-8HP"):
        body_options = ['1"', '1-1/4"', '1-1/2"', '2"', '2-1/2"']
    elif model == "121-12":
        body_options = ['1-1/2"', '2"', '2-1/2"', '3"']
    else:  # 121-16
        body_options = ['3"']

    if len(body_options) == 1:
        body = body_options[0]
        st.write(f"Body Size: **{body}** (fixed)")
    else:
        body = st.selectbox("Body Size", body_options)

    vp_eligible_bodies = ('1-1/2"', '2"', '2-1/2"')
    if body in vp_eligible_bodies:
        is_vp = st.selectbox("V-Port", ["No", "Yes"]) == "Yes"
    else:
        is_vp = False
    orifice = "V-Port" if is_vp else "Standard"

    if model == "121-8":
        spring_options = (
            ["Red-Black", "Blue-Black", "Green-Black", "Green", "Orange", "Black"]
            if body in ('1"', '1-1/4"')
            else ["Orange", "Black"]
        )
    elif model == "121-8HP":
        spring_options = ["Cadmium", "Cadmium + White"]
    elif model == "121-12":
        spring_options = (
            ["Black", "Cadmium"] if body == '3"' else ["Red", "Blue", "Green", "Orange", "Black", "Cadmium"]
        )
    else:  # 121-16
        spring_options = ["Red", "Blue", "Green", "Orange", "Yellow"]
    spring_color = st.selectbox("Spring Color", spring_options)

    opp, monitor_color = monitor_block(spring_options, "r121")

# ---------------------------------------------------------------------------
# 122
# ---------------------------------------------------------------------------
elif regulator_type == "122":
    reg_param = "122"
    model = st.selectbox("Model", ["122-8", "122-12"])
    if model == "122-8":
        body_options = ['1"', '1-1/4"']
        spring_options = ["Red-Black", "Blue-Black", "Green-Black", "Green", "Orange"]
    else:
        body_options = ['1-1/2"', '2"', '2-1/2"']
        spring_options = ["Red", "Blue", "Green", "Orange", "Black", "Cadmium"]
    body = st.selectbox("Body Size", body_options)
    spring_color = st.selectbox("Spring Color", spring_options)

    opp, monitor_color = monitor_block(spring_options, "r122")


st.divider()

if st.button("Generate Part Number(s)", type="primary"):
    result = run_product_configurator(
        reg_param, model, body, orifice, spring_color, diap, seat, monitor_color, opp
    )

    if result is None:
        st.error("No part number could be generated for this combination. Please review your selections.")
    elif isinstance(result, list):
        st.success(f"{len(result)} part numbers generated:")
        for i, pn in enumerate(result, start=1):
            label = "Primary" if i == 1 else "Monitor"
            st.code(pn, language=None)
            st.caption(label)
    else:
        st.success("Part number generated:")
        st.code(result, language=None)