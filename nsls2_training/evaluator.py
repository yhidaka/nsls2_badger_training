from epics import PV

import getpass

username = getpass.getuser()

PVNAMES = dict(
    a=f"{username}:obs_a",
    b=f"{username}:obs_b",
)

PVS = {k: PV(pvname, auto_monitor=False) for k, pvname in PVNAMES.items()}


def get_observable_names():  # Must update for your problem
    return ["a", "b", "derived_objective"]


def a(badger_env_obj):
    return PVS["a"].get()


def b(badger_env_obj):
    return PVS["b"].get()


def derived_objective(badger_env_obj):
    target_a_val = badger_env_obj.target_obs_a
    target_b_val = badger_env_obj.target_obs_b

    obj = (PVS["a"].get() - target_a_val) ** 2
    obj += (PVS["b"].get() - target_b_val) ** 2

    return obj
