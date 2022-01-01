#
# This file is part of LiteX-Boards.
#
# Copyright (c) 2019 msloniewski <marcin.sloniewski@gmail.com>
# SPDX-License-Identifier: BSD-2-Clause

from litex.build.generic_platform import *
from litex.build.altera import AlteraPlatform
from litex.build.altera.programmer import USBBlaster

# IOs ----------------------------------------------------------------------------------------------

_io = [
    # Clk / Rst
    ("clk10", 0, Pins("N5"), IOStandard("2.5 V")),
    ("clk25", 0, Pins("M8"), IOStandard("2.5 V")),
    ("clk50", 0, Pins("M9"), IOStandard("2.5 V")),

    # Leds
    ("user_led", 0, Pins("T20"),  IOStandard("1.5 V")),
    ("user_led", 1, Pins("U22"),  IOStandard("1.5 V")),
    ("user_led", 2, Pins("U21"),  IOStandard("1.5 V")),
    ("user_led", 3, Pins("AA21"), IOStandard("1.5 V")),
    ("user_led", 4, Pins("AA22"), IOStandard("1.5 V")),

    # Buttons
    ("user_btn", 0, Pins("L22"), IOStandard("1.5 V")),
    ("user_btn", 1, Pins("M21"), IOStandard("1.5 V")),
    ("user_btn", 2, Pins("M22"), IOStandard("1.5 V")),
    ("user_btn", 3, Pins("N21"), IOStandard("1.5 V")),

    # Switches
    ("user_sw", 0, Pins("H21"), IOStandard("1.5 V")),
    ("user_sw", 1, Pins("H22"), IOStandard("1.5 V")),
    ("user_sw", 2, Pins("J21"), IOStandard("1.5 V")),
    ("user_sw", 3, Pins("J22"), IOStandard("1.5 V")),
    ("user_sw", 4, Pins("G19"), IOStandard("1.5 V")),

    # Serial
    ("serial", 0,
        Subsignal("tx", Pins("W18"), IOStandard("2.5 V")),
        Subsignal("rx", Pins("Y19"), IOStandard("2.5 V"))
    ),
]

# Platform -----------------------------------------------------------------------------------------

class Platform(AlteraPlatform):
    default_clk_name   = "clk50"
    default_clk_period = 1e9/50e6
    create_rbf         = False

    def __init__(self):
        AlteraPlatform.__init__(self, "10M50DAF484C6GES", _io)
        self.add_platform_command("set_global_assignment -name FAMILY \"MAX 10\"")
        self.add_platform_command("set_global_assignment -name ENABLE_CONFIGURATION_PINS OFF")
        self.add_platform_command("set_global_assignment -name INTERNAL_FLASH_UPDATE_MODE \"SINGLE IMAGE WITH ERAM\"")

    def create_programmer(self):
        return USBBlaster(cable_name="USB-BlasterII")

    def do_finalize(self, fragment):
        AlteraPlatform.do_finalize(self, fragment)
        self.add_period_constraint(self.lookup_request("clk10",    loose=True), 1e9/10e6)
        self.add_period_constraint(self.lookup_request("clk50", 0, loose=True), 1e9/50e6)

