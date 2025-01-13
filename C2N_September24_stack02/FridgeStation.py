# This code creates a station for the Montana setup

import qcodes as qc 
import zhinst
from zhinst.qcodes import ZISession
from DriverStahl import Stahl, StahlChannel
from DriverKeithley2110 import Keithley2110
from IPS120 import OxfordInstruments_IPS120
import numpy as np
from qcodes import Station
from qcodes.parameters import Parameter
from typing import Any
import time


class Fridge(Station):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs) # The Fridge class inherits from the Station class
        
    def add_dmm(self, address = 'USB0::0x05E6::0x2110::8009584::INSTR'): # Digital MultiMeter
        '''
        There are also other drivers on : 
        https://github.com/QCoDeS/Qcodes_contrib_drivers/tree/main/qcodes_contrib_drivers/drivers/Tektronix
        They are developped by the commununity, and not by QCoDeS developpers. Still, it heavily relies on it.
        '''
        dmm = Keithley2110(name = 'Keithley2110', address = address) # Creates an instantiation "dmm" from the class keithley2000
        self.add_component(dmm, update_snapshot = False) # We add the Keithley to the station of instruments
        return dmm
    
    def add_mfli(self, serial = ['DEV?'], dataserver_address = "local?"):
        # dataserver address can be found in the LabOne Config tab
        mfli_list = []
        
        session = ZISession(dataserver_address) # Connection to the data server
        for i in range(len(serial)): # We connect the MFLI with the serials provided in the serial list
            session.connect_device(serial[i])
            mfli = session.devices[serial[i]]
            mfli.connect_message()
            mfli_list.append(mfli)
            self.add_component(mfli)
            
            if i == 0:
                daq_mfli = zhinst.core.ziDAQServer(dataserver_address, 8004, 6)
                
        return mfli_list, daq_mfli
    
    def add_Stahl(self, name = "HV062", address = "COM14"):
        
        dc = Stahl(name = name, address = address)
        self.add_component(dc, update_snapshot = False) #Disable update_snapshot that would ask *IDN to HV, that would not understand
        return dc
    
    def add_magnet(self, name = "IPS120", address = "GPIB2::30::INSTR"):
        
        magnet = OxfordInstruments_IPS120(name = name, address = address, use_gpib = True)
        magnet.connect_message()
        self.add_component(magnet, update_snapshot = False)
        return magnet
        
    
    def default_initialisation(self, dmm_dict = {"address":"address?"}, mfli_dict = {"serial":["serial?"],"dataserver":"localhost?"}, HV_dict = {"name":"name?","address":"COM?"}, LV_dict = {"name":"name?","address":"COM?"}, magnet_dict = {"name":"name?","address":"address?"}): # Initialises all the instruments
        self.station = qc.Station() 
        instrumentList = []
        
        if dmm_dict["address"] != "address?": # If an argument has been passed
            dmm = self.add_dmm(address = dmm_dict["address"]) # Sends a connection message by default
            instrumentList.append(dmm)
            
        if mfli_dict["serial"] != ["serial?"]:
            mfli_list, daq_mfli = self.add_mfli(serial = mfli_dict["serial"], dataserver_address=mfli_dict["dataserver"])
            instrumentList.append(mfli_list)
            instrumentList.append(daq_mfli)
            
        if HV_dict["name"] != "name?":
            HV = self.add_Stahl(name = HV_dict["name"], address = HV_dict["address"])
            instrumentList.append(HV)
            
        if LV_dict["name"] != "name?":
            LV = self.add_Stahl(name = LV_dict["name"], address = LV_dict["address"])
            instrumentList.append(LV)
            
        if magnet_dict["name"] != "name?":
            magnet = self.add_magnet(name = magnet_dict["name"], address = magnet_dict["address"])
            instrumentList.append(magnet)
            
        return instrumentList
    
    
class mfli_module(Parameter):
     
    def __init__(self, mfli, demodulator, name = "module"):
        super().__init__(
            name = name, # The local name of the parameter. If this parameter is part of an Instrument or Station, this is how it will be referenced from that parent, ie instrument.name or instrument.parameters[name]
            instrument = mfli, # The instrument this parameter belongs to, if any.
            label = name,
            unit = "") # Normally used as the axis label when this parameter is graphed, along with unit
        
        self.demodulator = demodulator
        self.mfli = mfli
    
    def get_raw(self):
        x = self.mfli.demods[self.demodulator].sample()["x"][0]
        y = self.mfli.demods[self.demodulator].sample()["y"][0]
        R = np.sqrt( x**2 + y**2 )
        return R
    
class mfli_phase(Parameter):
    
    def __init__(self,  mfli, demodulator, name = "phase"):
        super().__init__(
            name, # The local name of the parameter. If this parameter is part of an Instrument or Station, this is how it will be referenced from that parent, ie instrument.name or instrument.parameters[name]
            instrument = mfli, # The instrument this parameter belongs to, if any.
            label = "Phase",
            unit = "$\degree$") # Normally used as the axis label when this parameter is graphed, along with unit
        
        self.demodulator = demodulator
        self.mfli = mfli
    
    def get_raw(self):
        x = self.mfli.demods[self.demodulator].sample()["x"][0]
        y = self.mfli.demods[self.demodulator].sample()["y"][0]
        phase = np.arctan2(y, x) * 360/(2*np.pi)
        return phase
    
    
        
def module_and_phase(mfli, demod):
    x = mfli.demods[demod].sample()["x"][0]
    y = mfli.demods[demod].sample()["y"][0]
    R = np.sqrt( x**2 + y**2 )
    phi = np.arctan2(y, x) * 360/(2*np.pi)
    return (R, phi)


def goToVoltage(bgChannel:StahlChannel, start:float, stop:float, fastStep:float = 0.1, fastWait:float = 1.0) -> None:
    fastStep = abs(fastStep)
    if stop > start:
        for V in np.arange(start, stop+fastStep, fastStep):
            bgChannel.voltage(V)
            time.sleep(fastWait)
    elif stop < start:
        for V in np.arange(start, stop-fastStep, -fastStep):
            bgChannel.voltage(V)
            time.sleep(fastWait) 
    time.sleep(1) # Just leave some time to properly reach the final value

    bgChannel.voltage(stop) # Bug correction

    print(f"Successfully reached {bgChannel.voltage()} V")
    
def goToGround(bgChannel:StahlChannel, start:float, fastStep:float = 0.1, fastWait:float = 1.0) -> None:
    goToVoltage(bgChannel, start, 0, fastStep, fastWait)
    
def my_str(f): #A function to ensure that there are no points in the final database names
    return str(f).replace('.', ',')