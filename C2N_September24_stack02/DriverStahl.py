# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 14:54:28 2024

@author: Sofiane
"""
import numpy as np
import logging

from typing import Any

from qcodes.instrument import (
    ChannelList,
    InstrumentChannel,
    VisaInstrument
)

import time

logger = logging.getLogger()

class Stahl(VisaInstrument): # DC source containing several channels
    
    def __init__(self, name:str, address:str, **kwargs: Any):
        
        self.start = time.time()
        super().__init__(name, address, terminator="\r", **kwargs)
        self.end   = time.time()
        
        self.identifiers = self.ask("IDN").split()
        self.span = int(self.identifiers[1])       #Reads the maximal DC voltage
        self.nbChannels = int(self.identifiers[2]) #Reads the number of channels
        
        self.add_parameter( #Asks for the identifier
            "identify",
            get_cmd = "IDN",
            get_parser = str)
        
        self.add_parameter( #Asks for temperature
            "temperature",
            get_cmd = f"{self.name} TEMP",
            get_parser = str,
            unit = "C")
        
        self.add_parameter( # 0 means locked 1 means overloaded 
            "isLocked",
            get_cmd = f"{self.name} LOCK",
            get_parser = str)
        
        channels = ChannelList(parent = self, name = "channels", chan_type = StahlChannel)
        
        for channelNumber in range(1, self.nbChannels+1): # The channels are bound Stahl through modules and are effectively independent parameters
            name = f"CH{channelNumber:02d}"
            channel = StahlChannel(parent = self, name = name, channelNumber = channelNumber)
            channels.append(channel)
            self.add_submodule(name = name, submodule = channel)
        # We can communicate with the channels either through self.CH01 or self.channels[0]
            
        self.add_submodule(name = "channels", submodule = channels) # Adds an attribute channel to the Stahl class
            
        self.connect_message()
            
    def connect_message(self) -> None:
        print(f"Connected to: {self.name} with {self.nbChannels} channels and reaching {self.span}V in {self.end-self.start:.2f} s")
        
    def print_readable_snapshot(self) -> None:
        print(f"{self.name}")
        print("--------------------------------------")
        print(f"identify : {self.identify()} \n temperature : {self.temperature()[6:]} \n isLocked : {self.isLocked()}")
        print("--------------------------------------")
        
        for i in range(self.nbChannels):
            name = self.channels[i].name
            print(name  + f"\n {self.channels[i].voltage()}")
        
    def ask_raw(self, cmd: str) -> str:
        """
        Sometimes the instrument returns non-ascii characters in response
        strings manually adjust the encoding to latin-1
        """
        self.visa_log.debug(f"Querying: {cmd}")
        self.visa_handle.write(cmd)
        response = self.visa_handle.read(encoding="latin-1")
        self.visa_log.debug(f"Response: {response}")
        return response
        
        
    
class StahlChannel(InstrumentChannel): # Class controlling voltage in each channel
#InstrumentChannel inherits from InstrumentModule, they are literally the same objects
    
    def __init__(self, parent: VisaInstrument, name:str, channelNumber: int, **kwargs: Any):
        
        super().__init__(parent, name, **kwargs)
        
        self.channelNumber = channelNumber
        self.channelNumberString = f"{channelNumber:02d}"
        
        self.add_parameter(
            "voltageString",
            set_cmd = self._set_voltage, #_set_voltage is a callable, defined below
            get_cmd = self._get_voltage, #_get_voltage is a callable, defined below
            get_parser = str,
            unit = "V")
        
        self.add_parameter(
            "voltage",
            set_cmd = self._set_voltage,
            get_cmd = self._get_voltage,
            get_parser = float,
            unit = "V"
        )
        
    def _set_voltage(self, voltage : float) -> None: #_ before the name for signaling that this method is to be used internally only
        stahlBoundaries = self.parent.span * np.array([-1,1]) 
        inputBoundaries = np.array([0,1])
        
        voltage_normalized = np.interp(voltage, stahlBoundaries, inputBoundaries)
        
        response = self.ask(f"{self.parent.name} CH{self.channelNumberString} {voltage_normalized:1.6f}")

    def _get_voltage(self) -> float:
        answer = self.ask(f"{self.parent.name} Q{self.channelNumberString}")
        vString = answer.split()[0] # To remove the units

        return float(vString.replace(",", "."))
    
    
        
        
        
        
        
        
        
        
        
        