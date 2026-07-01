# Product Selection Tools


# 496 HSC Part Number Builder
# ---------------------------------------------------------------------------
def hsc_pnc496(match):
    body_map = {
        '3/8"': '3/8',
        '1/2"': '1/2',
        '3/4"': '3/4',
        '1"': '1',
    }
    orifice_map = {
        '1/8"': '10',
        '3/16"': '11',
        '1/4"': '12',
        '5/16"': '13',
        '3/8"': '14',
        '1/2"': '15',
    }
    spring_map = {
        'Silver': '00',
        'Blue': '11',
        'Green': '12',
        'Red': '10',
        'Black': '14',
    }

    model = match['model']
    body = body_map.get(match['body'])
    orifice = orifice_map.get(match['orifice'])
    spring = spring_map.get(match['color'])

    return f"R.{model}.{body}.{orifice}.{spring}"


# 143 HSC Part Number Builder
# ---------------------------------------------------------------------------
def hsc_pnc143(match):
    body_map = {
        '3/4"': '3/4',
        '1"': '1',
        '1-1/4"': '1-1/4',
    }
    orifice_map = {
        '1/8"': '10',
        '3/16"': '11',
        '1/4"': '12',
        '5/16"': '13',
        '3/8"': '14',
        '1/2"': '15',
        '5/8"': '16',
        '7/16"': '17',
    }
    spring_map = {
        'Red': '10',
        'Blue': '11',
        'Green': '12',
        'Orange': '13',
        'Black + White': '20',
        'Cadmium': '15',
        'Black': '14',
    }

    model = match['model']
    body = body_map.get(match['body'])
    orifice = orifice_map.get(match['orifice'])
    spring = spring_map.get(match['color'])

    return f"R.{model}.{body}.{orifice}.{spring}"


# 243 HSC Part Number Builder
# ---------------------------------------------------------------------------
def hsc_pnc243(match):
    body_map = {
        '1-1/4" SCD': '1-1/4SCD',
        '1-1/2" SCD': '1-1/2SCD',
        '2" SCD': '2SCD',
        '2" FLG': '2FLG',
        '2" FLG 10" FTF': '2FLG10',
    }
    orifice_map = {
        '0.207"': '207',
        '1/4"': '12',
        '3/8"': '14',
        '1/2"': '15',
        '3/4", 10°': '18',
        '3/4", 30°': '19',
        '1", 10°': '20',
        '1", 30°': '20',
        '1-1/4", 10°': '21',
        '1-1/4", 30°': '21',
    }
    spring_map = {
        'Red-Black': '01',
        'Blue-Black': '02',
        'Green-Black': '03',
        'Red': '10',
        'Blue': '11',
        'Green': '12',
        'Orange-Black': '13A',
        'Orange': '13',
        'Black': '14',
        'Cadmium': '15',
        'Cadmium + White': '21',
    }

    model = match['model']
    body = body_map.get(match['body'])
    orifice = orifice_map.get(match['orifice'])
    spring = spring_map.get(match['color'])
    opp = match['opp']
    monitor_spring = spring_map.get(match['mon_color'])

    if model == '243-12-2':
        return f"R.243-12-2.STD.{body}.12-2.INT.{orifice}.STD.{spring}.ALU"
    
    elif model == '243-12-1' and opp == "Monitor":
        return [
            f"R.243-12-1M.STD.{body}.12-1.EXT.{orifice}.STD.{monitor_spring}.ALU",
            f"R.243-12-1.STD.{body}.12-1.INT.{orifice}.STD.{spring}.ALU",
        ]
    
    elif model == '243-12-1':
        return f"R.243-12-1.STD.{body}.12-1.INT.{orifice}.STD.{spring}.ALU"
    
    elif model == '243-12-1M with External Control Line' and opp == "Monitor":
        return [
                f"R.243-12-1M.STD.{body}.12-1.EXT.{orifice}.STD.{monitor_spring}.ALU",
                f"R.243-12-1M.STD.{body}.12-1.EXT.{orifice}.STD.{spring}.ALU",
            ]
    
    elif model == '243-12-1 with External Control Line':
        return f"R.243-12-1M.STD.{body}.12-1.EXT.{orifice}.STD.{spring}.ALU"

    elif model == '243-8-2':
        return f"R.243-8-2.{body}.INT.{orifice}.STD.{spring}.ALU"
        
    elif model == '243-8-1' and opp == "Monitor":
        return [
            f"R.243-8-1M.{body}.EXT.{orifice}.STD.{monitor_spring}.ALU",
            f"R.243-8-1.{body}.INT.{orifice}.STD.{spring}.ALU",
        ]
    
    elif model == '243-8-1':
        return f"R.243-8-1.{body}.INT.{orifice}.STD.{spring}.ALU"

    # 243-8HP
    elif model == '243-8HP' and opp == "Monitor":
        return [
            f"R.243.HP-M.{body}.8-HP.EXT.{orifice}.STD.{monitor_spring}.ALU",
            f"R.243.HP.{body}.8-HP.INT.{orifice}.STD.{spring}.ALU",
        ]
    
    else:
        return f"R.243.HP.{body}.8-HP.INT.{orifice}.STD.{spring}.ALU"


# 046 HSC Part Number Builder
# ---------------------------------------------------------------------------
def hsc_pnc046(match):
    body_map = {
        '3/4"': '3/4',
        '1"': '1',
        '1-1/4"': '1-1/4',
    }
    orifice_map = {
        '1/8"': "10",
        '3/16"': "11",
        '1/4"': "12",
        '5/16"': "13",
        '3/8"': "14",
        '1/2"': "15",
    }
    spring_map = {
        'Yellow': '23',
        'Aluminum': '24',
        'White': '25',
        'Green': '28',
        'Tan': '26',
        'Gray': '27',
    }

    model = match['model']
    body = body_map.get(match['body'])
    orifice = orifice_map.get(match['orifice'])
    seat = 'TAN' # NetSuite only uses TAN orifice on most models
    spring = spring_map.get(match['color'])
    monitor_spring = spring_map.get(match['mon_color'])

    if model == '046-2':
        return f"R.046-2.IRV.{body}.IRV.{orifice}.{seat}.{spring}.ALU"
    elif model == '046' and match['opp'] != "Monitor":
        return f"R.046-1.STD.{body}.{orifice}.{seat}.{spring}.ALU"
    # Under 125 psi setpoint - use 046-2M for monitor
    elif monitor_spring != '27':
        return [
            f"R.046-2M.MON.{body}.IRV.{orifice}.{seat}.{monitor_spring}.ALU",
            f"R.046-1.STD.{body}.{orifice}.{seat}.{spring}.ALU",
        ]
    # over 125 psi setpoint - use 046-M for monitor
    else:
        return [
            f"R.046-M.MON.{body}.{orifice}.{seat}.{monitor_spring}.ALU",
            f"R.046-1.STD.{body}.{orifice}.{seat}.{spring}.ALU",
        ]


# 121-122 HSC Part Number Builder
# ---------------------------------------------------------------------------
def hsc_pnc121(match):
    #121
    body_map121 = {
        '1"': '1SCD',
        '1-1/4"': '11/4SCD',
        '1-1/2"': '11/2SCD',
        '2"': '2SCD',
        '2-1/2"': '21/2SCD',
        '3"': '3SCD',
    }    
    #122
    body_map122 = {
        '1"': '1SCD',
        '1-1/4"': '1-1/4SCD',
        '1-1/2"': '1-1/2SCD',
        '2"': '2SCD',
        '2-1/2"': '2-1/2SCD',
        '3"': '3SCD',
    }
    spring_map = {
        'Blue-Black with Black-Red counter': '37',
        'Red-Black': '1',
        'Blue-Black': '2',
        'Green-Black': '3',
        'Green': '12',
        'Orange': '13',
        'Black': '14',
        'Red with counter': '39',
        'Red': '10',
        'Blue': '11',
        'Cadmium': '15',
        'Yellow': '23',
        'Cadmium + White': '21',
        'Blue-black with Black counter': '33',
        'Red with Red-Black counter': '35',
    }

    if match['orifice'] == "V-Port":
        vp = 'VPORT'
    else:
        vp = 'STD'

    model = match['model']
    if model == '122-12' or model == '122-8':
        body = body_map122.get(match['body'])
    else:
        body = body_map121.get(match['body'])
    spring = spring_map.get(match['color'])
    monitor_spring = spring_map.get(match['mon_color'])

    if model == '121-16':
        diap = '16'
    elif model == '122-12' or model == '121-12':
        diap = '12'
    elif model == '121-8-HP':
        diap = '8-HP'
    else:
        diap = '8'

    if model == '122-8' or model == '122-12':
        # 122
        if match['opp'] == "Monitor":
            return [
                f"R.{model}.STD.{body}.{diap}.EXTCON.STD.STD.{monitor_spring}.ALU",
                f"R.{model}.STD.{body}.{diap}.INTCON.STD.STD.{spring}.ALU",
            ]
        else:
            return f"R.{model}.STD.{body}.{diap}.EXTCON.STD.STD.{spring}.ALU"
    else:
        # 121
        if match['opp'] == "Monitor":
            return [
                f"R.{model}.STD.{body}.{diap}.EXTCON.STD.STD.{vp}.{monitor_spring}.ALU",
                f"R.{model}.STD.{body}.{diap}.EXTCON.STD.STD.{vp}.{spring}.ALU",
            ]
        else:
            return f"R.{model}.STD.{body}.{diap}.EXTCON.STD.STD.{vp}.{spring}.ALU"
        

# 441-461 HSC Part Number Builder
# ---------------------------------------------------------------------------
def hsc_pnc461(match):
    body_map = {
        '2" Screwed': '2SCD',
        '2" ANSI 125': '2FLG125',
        '2" ANSI 250': '2FLG250',
        '2" ANSI 300': '2FLG300',
        '2" ANSI 600': '2FLG600',
        '3" ANSI 125': '3FLG125',
        '3" ANSI 250': '3FLG250',
        '3" ANSI 300': '3FLG300',
        '3" ANSI 600': '3FLG600',
        '4" ANSI 125': '4FLG125',
        '4" ANSI 250': '4FLG250',
        '4" ANSI 300': '4FLG300',
        '6" ANSI 125': '6FLG125',
        '6" ANSI 250': '6FLG250',
    }
    diap_map = {
        '10"': '10',
        '12"': '12',
        '14"': '14',
        '16"': '16',
        '18"': '18',
        '20"': '20',
        '12" Cast Iron': '461S-12',
        '12" Alunimum': '461-12-S',
        '8" Aluminum': '461-8-S',
        '8.5" Cast Iron': '461S-8',
    }
    orifice_map = {
        '11/16" single': '22S',
        '11/16" double': '22D',
        '1" single': '20S',
        '1" double': '20D',
        '1-1/2"': '23',
        '1-3/4"': '24',
        '2-1/8"': '25',
        '3"': '26',
        '4-1/4"': '27',
        '1" single VP': '20VPS',
        '1" double VP': '20VPD',
        '1-1/2" VP': '23VP',
        '1-3/4" VP': '24VP',
        '2-1/8" VP': '25VP',
        '3" VP': '26VP',
        '4-1/4" VP': '27VP',
    }
    spring_map = {
        'Aluminum': '24',
        'Green': '12',
        'Yellow': '23',
        'Gray': '27',
        'Blue': '11',
        'Red': '10',
        'Orange': '13',
        'Black': '14',
        'Cadmium': '15',
        'Cadmium + White': '21',
        'Brown': '22',
        'Brown + White': '31',
    }

    model = match['model']
    body = body_map.get(match['body'])
    diap = diap_map.get(match['diap'])
    diap = 'EXTCON' if diap == None else diap
    orifice = orifice_map.get(match['orifice'])
    seat = match['seat']
    seat = 'PT' if seat == "Poly-Tan" else seat
    spring = spring_map.get(match['color'])
    mon_spring = spring_map.get(match['mon_color'])
    opp = match['opp']
    end = 'S' if body[-3:] in ('300', '600') else 'I'

    # 461 -------------------
    if model == '461-X57':
        seat = 'B' if seat == "BUNA" else seat
        if opp == "Monitor":
            return [
                f"R.{model}.{body}.{diap}.{orifice}.{seat}.{spring}.ST",
                f"R.{model}.{body}.{diap}.{orifice}.{seat}.{mon_spring}.ST",
            ]
        else:
            return f"R.{model}.{body}.{diap}.{orifice}.{seat}.{spring}.ST"
    
    elif model == '461-57S' or model == '461-S':
        seat = 'B' if seat == "BUNA" else seat
        model = diap if diap == '461S-12' or diap == '461-12-S' or diap == '461-8-S' or diap == '461S-8' else model
        if opp == "Monitor":
            return [
                f"R.{model}.{body}.{orifice}.{seat}.{spring}",
                f"R.{model}.{body}.{orifice}.{seat}.{mon_spring}",
            ]
        else:
            return f"R.{model}.{body}.{orifice}.{seat}.{spring}"

    # 441 -------------------
    elif model == '441-57S' and body[0] in ('4', '6'):
        seat = 'B' if seat == "BUNA" else seat
        if opp == "Monitor":
            return [
                f"R.{model}.{body}.{orifice}.{seat}.{spring}.{end}",
                f"R.{model}.{body}.{orifice}.{seat}.{mon_spring}.{end}",
            ]
        else:
            return f"R.{model}.{body}.{orifice}.{seat}.{spring}.{end}"

    elif model == '441-S' and diap == '12' and body == '2FLG125':
        if opp == "Monitor":
            return [
                f"R.{model}.{body}.{diap}.{orifice}.{seat}.{spring}",
                f"R.{model}.{body}.{diap}.{orifice}.{seat}.{mon_spring}",
            ]
        else:
            return f"R.{model}.{body}.{diap}.{orifice}.{seat}.{spring}"

    else:
        if model == '441-57S':
            body = '2FLG' if body == '2FLG125' else '3FLG' if body == '3FLG125' else '2SCRD' if body == '2SCD' else body
        if opp == "Monitor":
            return [
                f"R.{model}.{body}.{diap}.{orifice}.{seat}.{spring}.{end}",
                f"R.{model}.{body}.{diap}.{orifice}.{seat}.{mon_spring}.{end}",
            ]
        else:
            return f"R.{model}.{body}.{diap}.{orifice}.{seat}.{spring}.{end}"


# Run Product Selection Function
# ---------------------------------------------------------------------------

def run_product_configurator(regulator_type, model, body, orifice, spring_color, diap, seat, monitor_spring_color, opp):

    match = None
    output = None

    match = {
        'model' : model,
        'body' : body,
        'diap' : diap,
        'orifice' : orifice,
        'seat' : seat,
        'color' : spring_color,
        'opp' : opp,
        'mon_color' : monitor_spring_color,
    }

    if regulator_type == '496':
        output = hsc_pnc496(match)
    if regulator_type == '143':
        output = hsc_pnc143(match)
    if regulator_type == '243':
        output = hsc_pnc243(match)
    if regulator_type == '046':
        output = hsc_pnc046(match)
    if regulator_type == '121' or regulator_type == '122':
        output = hsc_pnc121(match)
    if regulator_type == '441' or regulator_type == '461':
        output = hsc_pnc461(match)

    return output


# Required Inputs
# ---------------------------------------------------------------------------

# regulator type ('496', '143', '046', '243', '121', '122', '441', '461')
# model
# body
# diap
# orifice
# seat
# spring color
# opp
# monitor spring color

# they may be None depending on the regulator type