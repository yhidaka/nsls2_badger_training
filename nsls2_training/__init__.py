import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import evaluator
import knobs

from badger import environment


class Environment(environment.Environment):
    name = "nsls2_training"

    # parameters
    target_obs_a: float = 1.5
    target_obs_b: float = 2.3

    # ----------- Only modify above -----------

    variables = {k: [] for k in knobs.get_names()}
    observables = evaluator.get_observable_names()

    def __init__(self, **data):
        super().__init__(**data)

        self._pv_limits = knobs.get_abs_limits()

    def get_bounds(self, var_names):
        return {name: self._pv_limits[name] for name in var_names}

    def get_variables(self, var_names):
        return {knob_name: knobs.get_pv(knob_name).get() for knob_name in var_names}

    def set_variables(self, var_dict):
        for knob_name, val in var_dict.items():
            knobs.get_pv(knob_name).put(val, wait=False)

    def get_observables(self, obs_names):
        return {name: self._get_obs(name) for name in obs_names}

    def _get_obs(self, obs_name):
        return getattr(evaluator, obs_name)(self)
