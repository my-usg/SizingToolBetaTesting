#143 REGULATOR
from tabulate import tabulate

data143 = {
	0.25: {
        0.5: {'R14334_58': 510, 'R14334_12': 450, 'R14334_38': 340, 'R14334_56': None, 'R14334_14': None, 'R14334_36': None, 'R14334_18': None, 'R14310_58': 520, 'R14310_12': 460, 'R14310_38': 350, 'R14310_56': None, 'R14310_14': None, 'R14310_36': None, 'R14310_18': None, 'R1431Q_58': 520, 'R1431Q_12': 460, 'R1431Q_38': 350, 'R1431Q_56': None, 'R1431Q_14': None, 'R1431Q_36': None, 'R1431Q_18': None},
        1: {'R14334_58': 530, 'R14334_12': 510, 'R14334_38': 500, 'R14334_56': 480, 'R14334_14': None, 'R14334_36': None, 'R14334_18': None, 'R14310_58': 650, 'R14310_12': 600, 'R14310_38': 550, 'R14310_56': 480, 'R14310_14': None, 'R14310_36': None, 'R14310_18': None, 'R1431Q_58': 760, 'R1431Q_12': 680, 'R1431Q_38': 550, 'R1431Q_56': 480, 'R1431Q_14': None, 'R1431Q_36': None, 'R1431Q_18': None},
        2: {'R14334_58': 600, 'R14334_12': 580, 'R14334_38': 570, 'R14334_56': 560, 'R14334_14': 530, 'R14334_36': None, 'R14334_18': None, 'R14310_58': 780, 'R14310_12': 880, 'R14310_38': 840, 'R14310_56': 700, 'R14310_14': 530, 'R14310_36': None, 'R14310_18': None, 'R1431Q_58': 1030, 'R1431Q_12': 1020, 'R1431Q_38': 840, 'R1431Q_56': 700, 'R1431Q_14': 530, 'R1431Q_36': None, 'R1431Q_18': None},
        3: {'R14334_58': 670, 'R14334_12': 650, 'R14334_38': 630, 'R14334_56': 620, 'R14334_14': 600, 'R14334_36': 420, 'R14334_18': None, 'R14310_58': 810, 'R14310_12': 920, 'R14310_38': 1000, 'R14310_56': 870, 'R14310_14': 650, 'R14310_36': 420, 'R14310_18': None, 'R1431Q_58': 1050, 'R1431Q_12': 1200, 'R1431Q_38': 1030, 'R1431Q_56': 870, 'R1431Q_14': 650, 'R1431Q_36': 420, 'R1431Q_18': None},
        5: {'R14334_58': 790, 'R14334_12': 770, 'R14334_38': 730, 'R14334_56': 720, 'R14334_14': 700, 'R14334_36': 560, 'R14334_18': 250, 'R14310_58': 970, 'R14310_12': 950, 'R14310_38': 1160, 'R14310_56': 1120, 'R14310_14': 890, 'R14310_36': 580, 'R14310_18': 250, 'R1431Q_58': 1060, 'R1431Q_12': 1490, 'R1431Q_38': 1350, 'R1431Q_56': 1180, 'R1431Q_14': 890, 'R1431Q_36': 580, 'R1431Q_18': 250},
        7.5: {'R14334_58': 900, 'R14334_12': 900, 'R14334_38': 880, 'R14334_56': 860, 'R14334_14': 840, 'R14334_36': 700, 'R14334_18': 310, 'R14310_58': 1060, 'R14310_12': 1140, 'R14310_38': 1270, 'R14310_56': 1340, 'R14310_14': 1140, 'R14310_36': 700, 'R14310_18': 310, 'R1431Q_58': 1060, 'R1431Q_12': 1140, 'R1431Q_38': 1270, 'R1431Q_56': 1340, 'R1431Q_14': 1140, 'R1431Q_36': 700, 'R1431Q_18': 310},
        10: {'R14334_58': 1020, 'R14334_12': 1020, 'R14334_38': 1000, 'R14334_56': 970, 'R14334_14': 950, 'R14334_36': 830, 'R14334_18': 370, 'R14310_58': 1180, 'R14310_12': 1200, 'R14310_38': 1330, 'R14310_56': 1500, 'R14310_14': 1360, 'R14310_36': 840, 'R14310_18': 370, 'R1431Q_58': 1180, 'R1431Q_12': 1800, 'R1431Q_38': 1710, 'R1431Q_56': 1700, 'R1431Q_14': 1360, 'R1431Q_36': 840, 'R1431Q_18': 370},
        20: {'R14334_58': None, 'R14334_12': 1270, 'R14334_38': 1250, 'R14334_56': 1240, 'R14334_14': 1220, 'R14334_36': 1200, 'R14334_18': 530, 'R14310_58': None, 'R14310_12': 1400, 'R14310_38': 1480, 'R14310_56': 1600, 'R14310_14': 2000, 'R14310_36': 1230, 'R14310_18': 530, 'R1431Q_58': None, 'R1431Q_12': 1900, 'R1431Q_38': 1900, 'R1431Q_56': 1800, 'R1431Q_14': 1600, 'R1431Q_36': 1230, 'R1431Q_18': 630},
        40: {'R14334_58': None, 'R14334_12': None, 'R14334_38': 1450, 'R14334_56': 1340, 'R14334_14': 1330, 'R14334_36': 1570, 'R14334_18': 860, 'R14310_58': None, 'R14310_12': None, 'R14310_38': 1900, 'R14310_56': 1640, 'R14310_14': 2000, 'R14310_36': 1700, 'R14310_18': 860, 'R1431Q_58': None, 'R1431Q_12': None, 'R1431Q_38': 2000, 'R1431Q_56': 1900, 'R1431Q_14': 2200, 'R1431Q_36': 1800, 'R1431Q_18': 860},
        60: {'R14334_58': None, 'R14334_12': None, 'R14334_38': None, 'R14334_56': None, 'R14334_14': 1520, 'R14334_36': 1660, 'R14334_18': 1200, 'R14310_58': None, 'R14310_12': None, 'R14310_38': None, 'R14310_56': None, 'R14310_14': 2000, 'R14310_36': 1900, 'R14310_18': 1200, 'R1431Q_58': None, 'R1431Q_12': None, 'R1431Q_38': None, 'R1431Q_56': None, 'R1431Q_14': 2400, 'R1431Q_36': 2100, 'R1431Q_18': 1200},
        80: {'R14334_58': None, 'R14334_12': None, 'R14334_38': None, 'R14334_56': None, 'R14334_14': None, 'R14334_36': 1710, 'R14334_18': 1500, 'R14310_58': None, 'R14310_12': None, 'R14310_38': None, 'R14310_56': None, 'R14310_14': None, 'R14310_36': 2000, 'R14310_18': 1540, 'R1431Q_58': None, 'R1431Q_12': None, 'R1431Q_38': None, 'R1431Q_56': None, 'R1431Q_14': None, 'R1431Q_36': 2200, 'R1431Q_18': 1550},
        125: {'R14334_58': None, 'R14334_12': None, 'R14334_38': None, 'R14334_56': None, 'R14334_14': None, 'R14334_36': 1900, 'R14334_18': 1800, 'R14310_58': None, 'R14310_12': None, 'R14310_38': None, 'R14310_56': None, 'R14310_14': None, 'R14310_36': 2100, 'R14310_18': 2100, 'R1431Q_58': None, 'R1431Q_12': None, 'R1431Q_38': None, 'R1431Q_56': None, 'R1431Q_14': None, 'R1431Q_36': 2400, 'R1431Q_18': 2250},
    },
    0.5: {
        1: {'R14334_58': 530, 'R14334_12': 510, 'R14334_38': 500, 'R14334_56': 480, 'R14334_14': None, 'R14334_36': None, 'R14334_18': None, 'R14310_58': 650, 'R14310_12': 600, 'R14310_38': 550, 'R14310_56': 480, 'R14310_14': None, 'R14310_36': None, 'R14310_18': None, 'R1431Q_58': 760, 'R1431Q_12': 680, 'R1431Q_38': 550, 'R1431Q_56': 480, 'R1431Q_14': None, 'R1431Q_36': None, 'R1431Q_18': None},
        2: {'R14334_58': 600, 'R14334_12': 580, 'R14334_38': 570, 'R14334_56': 560, 'R14334_14': 530, 'R14334_36': None, 'R14334_18': None, 'R14310_58': 780, 'R14310_12': 880, 'R14310_38': 840, 'R14310_56': 700, 'R14310_14': 530, 'R14310_36': None, 'R14310_18': None, 'R1431Q_58': 1030, 'R1431Q_12': 1020, 'R1431Q_38': 840, 'R1431Q_56': 700, 'R1431Q_14': 530, 'R1431Q_36': None, 'R1431Q_18': None},
        3: {'R14334_58': 670, 'R14334_12': 650, 'R14334_38': 630, 'R14334_56': 620, 'R14334_14': 600, 'R14334_36': 420, 'R14334_18': None, 'R14310_58': 810, 'R14310_12': 920, 'R14310_38': 1000, 'R14310_56': 870, 'R14310_14': 650, 'R14310_36': 420, 'R14310_18': None, 'R1431Q_58': 1050, 'R1431Q_12': 1200, 'R1431Q_38': 1030, 'R1431Q_56': 870, 'R1431Q_14': 650, 'R1431Q_36': 420, 'R1431Q_18': None},
        5: {'R14334_58': 790, 'R14334_12': 770, 'R14334_38': 730, 'R14334_56': 720, 'R14334_14': 700, 'R14334_36': 560, 'R14334_18': 250, 'R14310_58': 970, 'R14310_12': 950, 'R14310_38': 1160, 'R14310_56': 1120, 'R14310_14': 890, 'R14310_36': 580, 'R14310_18': 250, 'R1431Q_58': 1060, 'R1431Q_12': 1490, 'R1431Q_38': 1350, 'R1431Q_56': 1180, 'R1431Q_14': 890, 'R1431Q_36': 580, 'R1431Q_18': 250},
        7.5: {'R14334_58': 900, 'R14334_12': 900, 'R14334_38': 880, 'R14334_56': 860, 'R14334_14': 840, 'R14334_36': 700, 'R14334_18': 310, 'R14310_58': 1060, 'R14310_12': 1140, 'R14310_38': 1270, 'R14310_56': 1340, 'R14310_14': 1140, 'R14310_36': 700, 'R14310_18': 310, 'R1431Q_58': 1060, 'R1431Q_12': 1140, 'R1431Q_38': 1270, 'R1431Q_56': 1340, 'R1431Q_14': 1140, 'R1431Q_36': 700, 'R1431Q_18': 310},
        10: {'R14334_58': 1020, 'R14334_12': 1020, 'R14334_38': 1000, 'R14334_56': 970, 'R14334_14': 950, 'R14334_36': 830, 'R14334_18': 370, 'R14310_58': 1180, 'R14310_12': 1200, 'R14310_38': 1330, 'R14310_56': 1500, 'R14310_14': 1360, 'R14310_36': 840, 'R14310_18': 370, 'R1431Q_58': 1180, 'R1431Q_12': 1800, 'R1431Q_38': 1710, 'R1431Q_56': 1700, 'R1431Q_14': 1360, 'R1431Q_36': 840, 'R1431Q_18': 370},
        20: {'R14334_58': None, 'R14334_12': 1270, 'R14334_38': 1250, 'R14334_56': 1240, 'R14334_14': 1220, 'R14334_36': 1200, 'R14334_18': 530, 'R14310_58': None, 'R14310_12': 1400, 'R14310_38': 1480, 'R14310_56': 1600, 'R14310_14': 2000, 'R14310_36': 1230, 'R14310_18': 530, 'R1431Q_58': None, 'R1431Q_12': 1900, 'R1431Q_38': 1900, 'R1431Q_56': 1800, 'R1431Q_14': 1600, 'R1431Q_36': 1230, 'R1431Q_18': 630},
        40: {'R14334_58': None, 'R14334_12': None, 'R14334_38': 1450, 'R14334_56': 1340, 'R14334_14': 1330, 'R14334_36': 1570, 'R14334_18': 860, 'R14310_58': None, 'R14310_12': None, 'R14310_38': 1900, 'R14310_56': 1640, 'R14310_14': 2000, 'R14310_36': 1700, 'R14310_18': 860, 'R1431Q_58': None, 'R1431Q_12': None, 'R1431Q_38': 2000, 'R1431Q_56': 1900, 'R1431Q_14': 2200, 'R1431Q_36': 1800, 'R1431Q_18': 860},
        60: {'R14334_58': None, 'R14334_12': None, 'R14334_38': None, 'R14334_56': None, 'R14334_14': 1520, 'R14334_36': 1660, 'R14334_18': 1200, 'R14310_58': None, 'R14310_12': None, 'R14310_38': None, 'R14310_56': None, 'R14310_14': 2000, 'R14310_36': 1900, 'R14310_18': 1200, 'R1431Q_58': None, 'R1431Q_12': None, 'R1431Q_38': None, 'R1431Q_56': None, 'R1431Q_14': 2400, 'R1431Q_36': 2100, 'R1431Q_18': 1200},
        80: {'R14334_58': None, 'R14334_12': None, 'R14334_38': None, 'R14334_56': None, 'R14334_14': None, 'R14334_36': 1710, 'R14334_18': 1500, 'R14310_58': None, 'R14310_12': None, 'R14310_38': None, 'R14310_56': None, 'R14310_14': None, 'R14310_36': 2000, 'R14310_18': 1540, 'R1431Q_58': None, 'R1431Q_12': None, 'R1431Q_38': None, 'R1431Q_56': None, 'R1431Q_14': None, 'R1431Q_36': 2200, 'R1431Q_18': 1550},
        125: {'R14334_58': None, 'R14334_12': None, 'R14334_38': None, 'R14334_56': None, 'R14334_14': None, 'R14334_36': 1900, 'R14334_18': 1800, 'R14310_58': None, 'R14310_12': None, 'R14310_38': None, 'R14310_56': None, 'R14310_14': None, 'R14310_36': 2100, 'R14310_18': 2100, 'R1431Q_58': None, 'R1431Q_12': None, 'R1431Q_38': None, 'R1431Q_56': None, 'R1431Q_14': None, 'R1431Q_36': 2400, 'R1431Q_18': 2250},
    },
	2.0: {	
        5: {'R14334_58': None, 'R14334_12': None, 'R14334_38': None, 'R14334_56': None, 'R14334_14': None, 'R14334_36': None, 'R14334_18': None, 'R14310_58': 650, 'R14310_12': 775, 'R14310_38': 650, 'R14310_56': 450, 'R14310_14': 325, 'R14310_36': 225, 'R14310_18': 100, 'R1431Q_58': 1200, 'R1431Q_12': 925, 'R1431Q_38': 650, 'R1431Q_56': 475, 'R1431Q_14': 325, 'R1431Q_36': 250, 'R1431Q_18': 100},
        10: {'R14334_58': None, 'R14334_12': None, 'R14334_38': None, 'R14334_56': None, 'R14334_14': None, 'R14334_36': None, 'R14334_18': None, 'R14310_58': 800, 'R14310_12': 800, 'R14310_38': 1050, 'R14310_56': 875, 'R14310_14': 575, 'R14310_36': 375, 'R14310_18': 175, 'R1431Q_58': 1750, 'R1431Q_12': 1650, 'R1431Q_38': 1150, 'R1431Q_56': 800, 'R1431Q_14': 575, 'R1431Q_36': 350, 'R1431Q_18': 175},
        15: {'R14334_58': None, 'R14334_12': None, 'R14334_38': None, 'R14334_56': None, 'R14334_14': None, 'R14334_36': None, 'R14334_18': None, 'R14310_58': None, 'R14310_12': 800, 'R14310_38': 1525, 'R14310_56': 1225, 'R14310_14': 900, 'R14310_36': 525, 'R14310_18': 225, 'R1431Q_58': None, 'R1431Q_12': 2200, 'R1431Q_38': 1700, 'R1431Q_56': 1100, 'R1431Q_14': 800, 'R1431Q_36': 525, 'R1431Q_18': 225},
        20: {'R14334_58': None, 'R14334_12': None, 'R14334_38': None, 'R14334_56': None, 'R14334_14': None, 'R14334_36': None, 'R14334_18': None, 'R14310_58': None, 'R14310_12': 1000, 'R14310_38': 2000, 'R14310_56': 1600, 'R14310_14': 1100, 'R14310_36': 625, 'R14310_18': 275, 'R1431Q_58': None, 'R1431Q_12': 2550, 'R1431Q_38': 2100, 'R1431Q_56': 1500, 'R1431Q_14': 1075, 'R1431Q_36': 625, 'R1431Q_18': 300},
        30: {'R14334_58': None, 'R14334_12': None, 'R14334_38': None, 'R14334_56': None, 'R14334_14': None, 'R14334_36': None, 'R14334_18': None, 'R14310_58': None, 'R14310_12': None, 'R14310_38': 2150, 'R14310_56': 2150, 'R14310_14': 1400, 'R14310_36': 800, 'R14310_18': 350, 'R1431Q_58': None, 'R1431Q_12': None, 'R1431Q_38': 2400, 'R1431Q_56': 2150, 'R1431Q_14': 1500, 'R1431Q_36': 800, 'R1431Q_18': 350},
        40: {'R14334_58': None, 'R14334_12': None, 'R14334_38': None, 'R14334_56': None, 'R14334_14': None, 'R14334_36': None, 'R14334_18': None, 'R14310_58': None, 'R14310_12': None, 'R14310_38': 2150, 'R14310_56': 2150, 'R14310_14': 1750, 'R14310_36': 1000, 'R14310_18': 450, 'R1431Q_58': None, 'R1431Q_12': None, 'R1431Q_38': 2550, 'R1431Q_56': 2500, 'R1431Q_14': 1850, 'R1431Q_36': 1000, 'R1431Q_18': 475},
        60: {'R14334_58': None, 'R14334_12': None, 'R14334_38': None, 'R14334_56': None, 'R14334_14': None, 'R14334_36': None, 'R14334_18': None, 'R14310_58': None, 'R14310_12': None, 'R14310_38': None, 'R14310_56': None, 'R14310_14': 2200, 'R14310_36': 1375, 'R14310_18': 575, 'R1431Q_58': None, 'R1431Q_12': None, 'R1431Q_38': None, 'R1431Q_56': None, 'R1431Q_14': 2500, 'R1431Q_36': 1375, 'R1431Q_18': 700},
        80: {'R14334_58': None, 'R14334_12': None, 'R14334_38': None, 'R14334_56': None, 'R14334_14': None, 'R14334_36': None, 'R14334_18': None, 'R14310_58': None, 'R14310_12': None, 'R14310_38': None, 'R14310_56': None, 'R14310_14': None, 'R14310_36': 1750, 'R14310_18': 775, 'R1431Q_58': None, 'R1431Q_12': None, 'R1431Q_38': None, 'R1431Q_56': None, 'R1431Q_14': None, 'R1431Q_36': 1725, 'R1431Q_18': 925},
        125: {'R14334_58': None, 'R14334_12': None, 'R14334_38': None, 'R14334_56': None, 'R14334_14': None, 'R14334_36': None, 'R14334_18': None, 'R14310_58': None, 'R14310_12': None, 'R14310_38': None, 'R14310_56': None, 'R14310_14': None, 'R14310_36': 2200, 'R14310_18': 1050, 'R1431Q_58': None, 'R1431Q_12': None, 'R1431Q_38': None, 'R1431Q_56': None, 'R1431Q_14': None, 'R1431Q_36': 2200, 'R1431Q_18': 1200},
    },
}


# Interpolation Function
# ------------------------------------------------------------------------------------------------------

def interpolate_capacity(data, inlet, outlet, monitor_used, vp):
    outlet_vals = sorted(data.keys())

    if outlet < outlet_vals[0] or outlet > outlet_vals[-1]:
        return "Error: inlet pressure is out of range for given outlet pressure"

    outlet_low = max([p for p in outlet_vals if p <= outlet])
    outlet_high = min([p for p in outlet_vals if p >= outlet])

    def inlet_interpolate(section):
        #Interpolate capacities at the target inlet pressure within one outlet section.
        inlet_vals = sorted(section.keys())
        if not inlet_vals or inlet < inlet_vals[0] or inlet > inlet_vals[-1]:
            return None
        inlet_low = max([p for p in inlet_vals if p <= inlet])
        inlet_high = min([p for p in inlet_vals if p >= inlet])
        u = (inlet - inlet_low) / (inlet_high - inlet_low) if inlet_high != inlet_low else 0
        result = {}
        for reg in section[inlet_low]:
            f0 = section[inlet_low][reg]
            f1 = section[inlet_high][reg]
            if f0 is None or f1 is None:
                result[reg] = None
            else:
                result[reg] = (1 - u) * f0 + u * f1
        return result

    cap_low = inlet_interpolate(data[outlet_low])
    cap_high = inlet_interpolate(data[outlet_high])

    if cap_low is None or cap_high is None:
        return "Error: inlet pressure is out of range for given outlet pressure"

    t = (outlet - outlet_low) / (outlet_high - outlet_low) if outlet_high != outlet_low else 0

    capacities = {}
    for reg in cap_low:
        v_low = cap_low[reg]
        v_high = cap_high.get(reg)
        if v_low is None or v_high is None:
            capacities[reg] = "N/A"
            continue
        interpolated = (1 - t) * v_low + t * v_high

        if monitor_used:
            interpolated *= 0.7

        if vp:
            interpolated *= 0.8

        interpolated *= gastypemult

        capacities[reg] = int(round(interpolated))

    return capacities


# Orifice Types & MAOP Function
# ------------------------------------------------------------------------------------------------------

def orifice_type143(reg):
    suf = reg[-2:]
    if suf == "18":
        return '1/8"'
    elif suf == "36":
        return '3/16"'
    elif suf == "14":
        return '1/4"'
    elif suf == "56":
        return '5/16"'
    elif suf == "38":
        return '3/8"'
    elif suf == "12":
        return '1/2"'
    elif suf == '58':
        return '5/8"'

def orifice_max143(reg):
    suf = reg[-2:]
    if suf == "18":
        return 125
    elif suf == "36":
        return 125
    elif suf == "14":
        return 60
    elif suf == "56":
        return 40
    elif suf == "38":
        return 40
    elif suf == "12":
        return 20
    elif suf == '58':
        return 10


# Spring Selections
# ------------------------------------------------------------------------------------------------------

def spring_143(op):
    if op < 6.5/28 and op >= 3.5/28:
        return {
            'color': 'Red',
            'range': '(3.5" - 6.5" wc)',
        }
    elif op < 8.5/28:
        return {
            'color': 'Blue',
            'range': '(5" - 8.5" wc)',
        }
    elif op < 14/28:
        return {
            'color': 'Green',
            'range': '(6" - 14" wc)',
        }
    elif op < 1:
        return {
            'color': 'Orange',
            'range': '(12" - 28" wc)',
        }
    elif op <= 2:
        return {
            'color': 'Black + White',
            'range': '(0.5 - 2 psi)',
        }
    elif op < 3:
        return {
            'color': 'Cadmium',
            'range': '(0.5 - 3 psi)',
        }
    elif op <= 6:
        return {
            'color': 'Black',
            'range': '(2 - 6 psi)',
        }
    

# Will Regulator Work Function & Will IRV Work
# ------------------------------------------------------------------------------------------------------

def will_work(cap, reg, orifice_max):
    if cap == "N/A":
        return "No"
    else:
        if cap >= (flow_rate * oversizeby) and orifice_max >= maop:
            return "Yes"
        else:
            return "No"

def will_irv_work143(reg):
    orif = orifice_type143(reg)

    # Partial IRV
    if partial:
        return "Partial"
    
    if irv_lim >= 1.75:
        if orif == '1/8"':
            max = 125
        elif orif == '3/16"':
            max = 90
        elif orif == '1/4"':
            max = 48
        elif orif == '5/16"':
            max = 30
        elif orif == '3/8"':
            max = 17
        elif orif == '1/2"':
            max = 0
        elif orif == '5/8"':
            max = 0
    elif irv_lim >= 1.25:
        if orif == '1/8"':
            max = 125
        elif orif == '3/16"':
            max = 68
        elif orif == '1/4"':
            max = 36
        elif orif == '5/16"':
            max = 21
        elif orif == '3/8"':
            max = 12.5
        elif orif == '1/2"':
            max = 0
        elif orif == '5/8"':
            max = 0
    elif irv_lim >= 0.75:
        if orif == '1/8"':
            max = 100
        elif orif == '3/16"':
            max = 40
        elif orif == '1/4"':
            max = 20
        elif orif == '5/16"':
            max = 11
        elif orif == '3/8"':
            max = 7
        elif orif == '1/2"':
            max = 0
        elif orif == '5/8"':
            max = 0
    else:
        max = 0

    if inlet_input <= max:
        return "Yes"
    else:
        return "No"


# Regulator Match Functions
# ------------------------------------------------------------------------------------------------------

def gen_match143(result, opp):
    match = None

    if outlet_input > 2:
        model = '143-2HP'
    else:
        model = '143-1' if opp == "None" else '143-2'

    body_labels143 = {
        'R14334': '3/4"',
        'R14310': '1"',
        'R1431Q': '1-1/4"',
    }

    pipe_priority = {
        '3/4"': 'R14334',
        '1"':    'R14310',
        '1-1/4"': 'R1431Q',
    }

    all_prefixes = list(body_labels143.keys())
    prioritized = pipe_priority.get(pipesize_input)
    if prioritized:
        ordered_prefixes = [prioritized] + [p for p in all_prefixes if p != prioritized]
    else:
        ordered_prefixes = all_prefixes

    # largest to smallest orifices
    orifice_order143 = ['58', '12', '38', '56', '14', '36', '18']

    # IRV
    if opp != "None":
        for prefix in ordered_prefixes:
            for orifice in orifice_order143:
                reg = f"{prefix}_{orifice}"
                if reg in result:
                    cap = result[reg]
                    if will_work(cap, reg, orifice_max143(reg)) == "Yes" and will_irv_work143(reg) != "No":
                        match = {
                            'reg' : reg,
                            'model': model,
                            'diap': None,
                            'body': body_labels143[prefix],
                            'orifice': orifice_type143(reg),
                            'seat': None,
                            'color': spring_143(outlet_input)['color'],
                            'range': spring_143(outlet_input)['range'],
                            'capacity': cap,
                            'opp': "IRV",
                            'mon_color': None,
                            'mon_range': None,
                            'mon_diap': None,
                        }
                        return match
    # No OPP
    else:
        for prefix in ordered_prefixes:
            for orifice in orifice_order143:
                reg = f"{prefix}_{orifice}"
                if reg in result:
                    cap = result[reg]
                    if will_work(cap, reg, orifice_max143(reg)) == "Yes":
                        match = {
                            'reg' : reg,
                            'model': model,
                            'diap': None,
                            'body': body_labels143[prefix],
                            'orifice': orifice_type143(reg),
                            'seat': None,
                            'color': spring_143(outlet_input)['color'],
                            'range': spring_143(outlet_input)['range'],
                            'capacity': cap,
                            'opp': "None",
                            'mon_color': None,
                            'mon_range': None,
                            'mon_diap': None,
                        }
                        return match


def run_regulator_selection143(inlet, outlet, opp):
    result = interpolate_capacity(data143, inlet, outlet, False, False)

    warning = None

    if isinstance(result, str):
        warning = result
        result = None
        match = None
        apply = False
        return result, match, apply, warning

    match = gen_match143(result, opp)

    # if opp = IRV and partial = False, fail if outlet > 2 psi (for 143-2HP)

    if opp == "IRV" and outlet_input > 2 and not partial:
        apply = False
        warning = "Cannot size IRV for outlet pressures > 2 psi"
    elif match:
        apply = True
        if opp == "IRV" and not partial:
            warning = "Sized for IRV"
    else:
        apply = False

    return result, match, apply, warning


# Part Number Configurator
# ------------------------------------------------------------------------------------------------------

# Holland Part Number
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


# Output Functions
# ------------------------------------------------------------------------------------------------------

def print_model_table(title, prefix, opp, result):
    
    if opp == "IRV":
        rows = [
            [orifice_type143(reg), f"{cap:,.0f}" if isinstance(cap, (int, float)) else cap, will_work(cap, reg, orifice_max143(reg)), will_irv_work143(reg)]
            for reg, cap in result.items()
            if reg.startswith(prefix)
        ]
        print("\n" + title)
        print(tabulate(rows, headers=["Orifice Size", "Calculated Capacity (CFH)", "Will Reg Work?", "Will IRV Work?"], tablefmt="simple_grid"))
    else:
        rows = [
            [orifice_type143(reg), f"{cap:,.0f}" if isinstance(cap, (int, float)) else cap, will_work(cap, reg, orifice_max143(reg))]
            for reg, cap in result143.items()
            if reg.startswith(prefix)
        ]
        print("\n" + title)
        print(tabulate(rows, headers=["Orifice Size", "Calculated Capacity (CFH)", "Will It Work?"], tablefmt="simple_grid"))

def print_regulator_selection(match):
    print("REGULATOR SELECTION")
    print(f"Model:", match['model'])
    if match['diap'] != None:
        print(f"Diaphragm Size:", match['diap'])
    print(f"Body Size:", match['body'])
    if match['orifice'] != None:
        print(f"Orifice Size:", match['orifice'])
    if match['seat'] != None:
        print(f"Seat:", match['seat'])
    print(f"Spring:", match['color'], match['range'])
    if match['mon_color'] != None:
        print(f"Monitor Spring:", match['mon_color'], match['mon_range'])
    if match['mon_diap'] != None:
        print(f"Monitor Diaphragm Size:", match['mon_diap'])
    capacity = match['capacity']
    cap_str = f"{capacity:,.0f}" if isinstance(capacity, (int, float)) else str(capacity)
    print(f"Calculated Capacity (CFH): {cap_str}")

    print("")
    print("Sizing Adjustments")
    if match['opp'] == "Monitor":
        print("Monitor regulator: 30% Capacity reduction")
    print(f"Oversized by {oversize_percent:.0f}%")
    if gastypemult != 1:
        print(f"Multiplier for other gas: {gastypemult}")


# INPUT
# ------------------------------------------------------------------------------------------------------

print("Model 143 Sizing Tool")

inlet_units = input("Inlet Pressure units (psi, bar): ")
inlet_input = float(input("Enter inlet pressure: "))

outlet_units = input("Outlet Pressure units (in wc, psi, bar): ")
outlet_input = float(input("Enter outlet pressure: "))

flowrate_units = input("Gas Load units (CFH, BTUH, CMH): ")
flow_rate = float(input("Enter gas load/flow rate: "))

maop = float(input("MAOP (psi): "))
maop = inlet_input if maop == 0 else maop

pipesize_input = (input("Enter desired pipe size (enter N/A, 0.75, 1, 1.25, ect.): "))
pipesize_input = 0 if pipesize_input == "N/A" else pipesize_input

# Pressure Units Adjustments
if outlet_units == "in wc":
    outlet_input *= 1/28
elif outlet_units == "bar":
    outlet_input *= 14.5
if inlet_units == "bar":
    inlet_input *= 14.5

opp_input = input("Do you require overpressure protection? (y/n): ").lower()
partial = False
irv_input = 0
if opp_input == "y":
    irv_input = float(input("IRV protect downstream pressure to: "))
    irv_lim = irv_input - outlet_input
    opp_type = "IRV"
else:
    partial_input = input("If applicable, select regulator with IRV for partial overpressure protection? (y/n): ")
    partial = True if partial_input == "y" else False
    opp_type = "IRV" if partial else "None"

higheff_input = input("Is this feeding a generator or high-efficiency boiler? (y/n): ").lower()
if higheff_input == "y":
    pload = float(input("What percent of the total load is feeding a generator or high-efficiency boiler: "))
    if pload < 0 or pload > 100:
        print("")
        print("Error: Percentage must be between 0-100")
        print("")
        exit()
    pload *= 0.01
else:
    pload = 0
oversizeby = 1.2 + (0.8 * pload)
oversize_percent = (oversizeby - 1) * 100

# Other Gasses
# -----------------------------
gastype_input = input("Other gas (n, propane, other): ")
if gastype_input == "other":
    sg = float(input("Enter specific gravity: "))
    gastypemult = (0.6 / sg) ** 0.5
    if gastypemult > 1:
        gastypemult = 1
    print("")
    print("Contact USG for regulator compatibility with gasses other than methane or propane")
elif gastype_input == "propane":
    gastypemult = 0.63
else:
    gastypemult = 1

# Flowrate Unit Adjustments
if flowrate_units == "CMH":
    flow_rate *= 35.3147
elif flowrate_units == "BTUH":
    if gastype_input == "n":
        flow_rate *= 1/1000
    elif gastype_input == "propane":
        flow_rate *= 1/2516
    else:
        print("Enter gas load/flow rate in CFH or CMH when using other gasses")
        exit()


# Validation
# ------------------------------------------------------------------------------------------------------

if inlet_input > 125 or inlet_input < 0.5:
    print("")
    print("Error: Inlet pressure must be between 0.5 - 125 psi")
    print("")
    exit()

if outlet_input < 3.5/28 or outlet_input > 6:
    print("")
    print("Error: Outlet pressure must be between 3.5 in wc and 6 psi")
    print("")
    exit()

if outlet_input >= inlet_input:
    print("")
    print("Error: Outlet pressure must be less than inlet pressure")
    print("")
    exit()

if maop < inlet_input and maop != 0:
    print("")
    print("Error: Maximum inlet pressure/MAOP must be greater than or equal to inlet pressure")
    print("")
    exit()

# Adjust outlet pressures between 3.5" wc and 7" wc to 7" wc
# Adjust outlet pressures between 2 - 6 psi to 2 psi
if 3.5/28 <= outlet_input < 0.25:
    outlet_input143 = 0.25
elif 2 < outlet_input <= 6:
    outlet_input143 = 2
else:
    outlet_input143 = outlet_input



# Run Regulator Selection
# ------------------------------------------------------------------------------------------------------

result143, match143, apply143, warning143 = run_regulator_selection143(inlet_input, outlet_input143, opp_type)


# Print Output
# ------------------------------------------------------------------------------------------------------

# Print regulator selection
if apply143:
    if warning143:
        print("")
        print(warning143)
    print("")
    print_regulator_selection(match143)
    print("")
    
    # HSC Part Number = add_cart
    add_cart = hsc_pnc143(match143)
    print(f"HSC P/N:", ', '.join(add_cart) if isinstance(add_cart, (list, set)) else add_cart)
else:
    if warning143:
        print("")
        print(warning143)
        print("")
        exit()
    else:
        print("")
        print("Model 143 will not work for your application.")
print("")

# Print capacity table

opp_type = "None" if partial else opp_type

print("REGULATOR SIZING TABLES")
print_model_table('Model 143, 3/4" Body','R14334', opp_type, result143)
print_model_table('Model 143, 1" Body','R14310', opp_type, result143)
print_model_table('Model 143, 1-1/4" Body','R1431Q', opp_type, result143)
