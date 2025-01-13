import sys
sys.path.append('C:/Users/labo-admin/Desktop/Python_SGM/dilu06_packages_Package')
# from ReadMotor_z import *
import qcodes_contrib_drivers.drivers.Tektronix.Keithley_2700 as Keithley
from Fancy_Plotter_v6  import *
import time
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from matplotlib.widgets import Button
from datetime import datetime, timedelta
from matplotlib.dates import DateFormatter
from IPython.display import clear_output
from matplotlib.widgets import CheckButtons
from ipywidgets import Checkbox,Layout
from zhinst.qcodes import ZISession 
from zhinst.qcodes import MFLI
import qcodes as qc

#A COMPLETER AVEC ADRESSES KEITHLEY + MFLI

VISA_Dmm1='GPIB0::14::INSTR' 
MFLI_Adress='dev4451'




##############################################################
dmm1=Keithley.Keithley_2700('Keytley_2700B',address=VISA_Dmm1)
dmm1.add_parameter('VoltDC',unit='Ohm',get_cmd='MEAS:VOLT:DC? ',get_parser=float)



session = ZISession("localhost")
mfli=MFLI(serial=MFLI_Adress,host='localhost')
mfli.connect_message()
Aux_out=qc.ScaledParameter(mfli.auxouts[3].offset, gain=1, name='Aux_out', label='Auxout', unit='V')

# Function to measure data
def measure(interval=200):
    # Function to measure data / Before replacing by the real measurement tool,
    # in the meantime we can just generate random data
    Extension=4.8
    V_in=Aux_out()
    data = (Extension)*((dmm1.VoltDC()-(0.04*V_in))/(0.7*V_in+1e-10))*1000  # Replace this line with your actual measurement code
    
    return data


plot_measured_data(filepath='./Zmotor/', saving = False,measure_data=measure,Axis_Y='Extension \ [\mu m]')
