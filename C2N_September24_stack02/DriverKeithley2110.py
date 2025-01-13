# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 17:37:09 2023

@author: Sofiane
"""

from functools import partial
from typing import Any, Callable, Union

from qcodes.instrument import VisaInstrument
from qcodes.validators import Bool, Enum, Ints, MultiType, Numbers

import time



class Keithley2110(VisaInstrument):
    
    def __init__(self, name: str, address: str, reset: bool = False, **kwargs: Any):
        
        self.start = time.time()
        super().__init__(name, address, terminator="\n", **kwargs)
        self.end   = time.time()
        
        self._trigger_sent = False
        
        #The set_cmd are useless until ACvoltage, but I still put them to keep the way to ask it here.
        
        self.add_parameter(
            "amplitude",
            get_cmd = "READ?",
            get_parser=float
            )
        
        self.add_parameter(
            "resistance",
            unit = "ohm",
            get_cmd = "MEAS:RES?",
            set_cmd = "CONF:RES",
            get_parser = float)
        
        self.add_parameter(
            "fresistance",
            unit = "ohm",
            get_cmd = "MEAS:FRES?",
            set_cmd = "CONF:FRES",
            get_parser = float)
        
        self.add_parameter(
            "DCcurrent",
            unit = "ampere",
            get_cmd = "MEAS:CURR:DC?",
            set_cmd = "CONF:CURR:DC",
            get_parser = float)
        
        self.add_parameter(
            "ACcurrent",
            unit = "ampere",
            get_cmd = "MEAS:CURR:AC?",
            set_cmd = "CONF:CURR:AC",
            get_parser = float)
        
        self.add_parameter(
            "DCvoltage",
            unit = "volt",
            get_cmd = "MEAS:VOLT:DC?",
            set_cmd = "CONF:VOLT:DC",
            get_parser = float)
        
        self.add_parameter(
            "ACvoltage",
            unit = "volt",
            get_cmd = "MEAS:VOLT:AC?",
            set_cmd = "CONF:VOLT:AC",
            get_parser = float)
        
        # Unfortunately the strings have to contain quotation marks and a
        # newline character, as this is how the instrument returns it.
        self.add_parameter(
            "mode",
            get_cmd="SENS:FUNC?",
            set_cmd="CONF:{}",
        )

        # Mode specific parameters
        # self.add_parameter(
        #     "nplc",
        #     get_cmd=self.get_mode()+":NPLC?",
        #     get_parser=float,
        #     set_cmd=self. get_mode()+":NPLC {}",
        #     vals=Numbers(min_value=0.01, max_value=10),
        # )

        # TODO: validator, this one is more difficult since different modes
        # require different validation ranges
        self.add_parameter(
            "range",
            get_cmd=self.get_mode()+":RANG?", 
            get_parser=float,
            set_cmd=self.get_mode()+":RANG {}",
            vals=Numbers(),
        )

        self.add_parameter(
            "auto_range_enabled",
            get_cmd=self.get_mode()+":RANG:AUTO?",
            set_cmd=self.get_mode()+":RANG:AUTO {}",
            set_parser = str
        )

        # self.add_parameter(
        #     "digits",
        #     get_cmd=partial(self._get_mode_param, "DIG", int),
        #     set_cmd=partial(self._set_mode_param, "DIG"),
        #     vals=Ints(min_value=4, max_value=7),
        # )

        self.add_parameter(
            "averaging_type",
            get_cmd= "AVER:TCON?",
            set_cmd= "AVER:TCON {}",
            vals=Enum("moving", "repeat"),
        )

        self.add_parameter(
            "averaging_count",
            get_cmd= "AVER:COUN?",
            set_cmd= "AVER:COUN {}",
            vals=Ints(min_value=1, max_value=100),
        )

        self.add_parameter(
            "averaging_enabled",
            get_cmd="AVER:STAT?",
            set_cmd="AVER:STAT {}",
            set_parser = str,
        )

        # Global parameters
        # self.add_parameter(
        #     "display_enabled",
        #     get_cmd="DISP:ENAB?",
        #     set_cmd="DISP:ENAB {}",
        #     set_parser = str,
        # )

        # self.add_parameter(
        #     "trigger_continuous",
        #     get_cmd="INIT:CONT?",
        #     set_cmd="INIT:CONT {}",
        #     set_parser=str
        # )

        self.add_parameter(
            "trigger_count",
            get_cmd="TRIG:COUN?",
            set_cmd="TRIG:COUN {}",
            vals=MultiType(
                Ints(min_value=1, max_value=9999),
                Enum("inf", "default", "minimum", "maximum"),
            ),
        )

        self.add_parameter(
            "trigger_delay",
            get_cmd="TRIG:DEL?",
            get_parser=float,
            set_cmd="TRIG:DEL {}",
            unit="s",
            vals=Numbers(min_value=0, max_value=999999.999),
        )

        self.add_parameter(
            "trigger_source",
            get_cmd="TRIG:SOUR?",
            set_cmd="TRIG:SOUR {}",
            val_mapping={
                "immediate": "IMM",
                "timer": "TIM",
                "manual": "MAN",
                "bus": "BUS",
                "external": "EXT",
            },
        )

        # self.add_parameter(
        #     "trigger_timer",
        #     get_cmd="TRIG:TIM?",
        #     get_parser=float,
        #     set_cmd="TRIG:TIM {}",
        #     unit="s",
        #     vals=Numbers(min_value=0.001, max_value=999999.999),
        # )

        self.add_function("reset", call_cmd="*RST")

        if reset:
            self.reset()

        # Set the data format to have only ascii data without units and channels
        self.write("FORM:DATA ASCII")
        self.write("FORM:ELEM READ")

        self.connect_message()
        
    
    def trigger(self) -> None:
        if not self.trigger_continuous():
            self.write("INIT")
            self._trigger_sent = True


    def get_mode(self):
        mode = self.ask("SENS:FUNC?")
        return mode[1:-1] # [1:-1] to remove the outer quotes sent by the Keithley
    
    def connect_message(self) -> None:
        idn = self.IDN()
        print(f"Connected to: {idn['vendor']} {idn['model']} (serial:{idn['serial']}, {idn['firmware']}) in {self.end-self.start:.2f} s")