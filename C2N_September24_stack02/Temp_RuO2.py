import sys
sys.path.append('C:/Users/labo-admin/Desktop/Python_SGM//dilu06_packages_Package')
from ReadMotor_z import *
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
from SGM_LLN_Package import *



####################
session = ZISession("localhost")
mfli=MFLI(serial='dev3213',host='localhost')
mfli.connect_message()

###################

demod0_R = LI_mparam_demod_amp(mfli, demod_n = 0)
demod1_R = LI_mparam_demod_amp(mfli, demod_n = 1)


R1=qc.ScaledParameter(demod0_R,gain=1, name='R_1', label='V_1', unit='V')
R2=qc.ScaledParameter(demod1_R,gain=1, name='R_2', label='I_1', unit='A')


f_1=qc.ScaledParameter(mfli.oscs[0].freq, gain=1, name='f_demod1', label='f_demod1', unit='Hz')

select_f_1 = qc.ScaledParameter(mfli.demods[0].oscselect, gain=1, name='f_sel_1', label='select_f_1')

Input_signal_1 = qc.ScaledParameter(mfli.demods[0].adcselect, gain=1, name = 'signal_type_1')
Input_signal_2 = qc.ScaledParameter(mfli.demods[1].adcselect, gain=1, name = 'signal_type_2')

enable_1 = qc.ScaledParameter(mfli.demods[0].enable, gain=1, name = 'enable_1')
enable_2 = qc.ScaledParameter(mfli.demods[1].enable, gain=1, name = 'enable_2')

diff_1 = qc.ScaledParameter(mfli.sigins[0].diff, gain=1, name = 'diff')

#############

f_1(7)

Input_signal_1(0)
Input_signal_2(1)

select_f_1(0)
select_f_1(0)

enable_1(1)
enable_2(1)

diff_1(1)

#############
def measure():
    # R = R1()/R2()
    V = mfli.sigouts[0].amplitudes[0].value()/np.sqrt(2)
    I = V / 100e6 #10 mV sur 100MOhms
    R = R1() / I
    ln_T = -2.6553952011*np.log(-8.1866484759+0.98155249557*np.log(R))
    T = np.exp(ln_T)
    return T * 1e3

plot_measured_data( filepath='./RuO2/', saving = False,measure_data=measure,Axis_Y='T_{RuO2} \ [mK]')
