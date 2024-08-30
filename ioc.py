import asyncio
import getpass

from caproto.server import PVGroup, ioc_arg_parser, pvproperty, run


class TempPVGroup(PVGroup):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    knob_x = pvproperty(name=f"knob_x", value=0.0, dtype=float, read_only=False, doc="")
    knob_y = pvproperty(name=f"knob_y", value=0.0, dtype=float, read_only=False, doc="")

    obs_a = pvproperty(name=f"obs_a", value=0.0, dtype=float, read_only=True, doc="")
    obs_b = pvproperty(name=f"obs_b", value=0.0, dtype=float, read_only=True, doc="")

    @knob_x.putter
    async def knob_x(self, instance, value):
        await self.obs_a.write(value * 2.0)
        return value

    @knob_y.putter
    async def knob_y(self, instance, value):
        await self.obs_b.write(value * (-1))
        return value


if __name__ == "__main__":
    # Command to run this server:
    #   (badger_training) $ python ioc.py --list-pvs

    # obs_a := "knob_x" * 2
    # obs_b := "knob_y" * (-1)

    username = getpass.getuser()

    ioc_options, run_options = ioc_arg_parser(
        default_prefix=f"{username}:", desc="Run a temporary IOC for Badger training"
    )
    ioc = TempPVGroup(**ioc_options)
    run(ioc.pvdb, **run_options)
