import getpass

username = getpass.getuser()

PVNAMES = dict(
    x=f"{username}:knob_x",
    y=f"{username}:knob_y",
)

ABS_LIMITS = {}  # Absolute limits

for k in ["x", "y"]:
    ABS_LIMITS[k] = [-20.0, +20.0]

# ----------- Only modify above -----------

import numpy as np
from epics import PV

PVS = {k: PV(pvname, auto_monitor=False) for k, pvname in PVNAMES.items()}


def get_names():
    return list(PVS)


def get_pv(knob_name):
    return PVS[knob_name]


def get_abs_limits():
    lower = np.array([ABS_LIMITS[name][0] for name in PVS.keys()])
    upper = np.array([ABS_LIMITS[name][1] for name in PVS.keys()])

    assert len(lower) == len(upper) == len(PVS)

    abs_limits = {
        name: [float(L), float(U)] for name, L, U in zip(list(PVS), lower, upper)
    }

    return abs_limits
