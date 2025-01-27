import threading
import time

start_time = time.time() 

def set_persistent():
    print("setting magnet to persistent mode")
    time.sleep(10)
    print("magnet in persistent mode")

def leave_persistent():
    print("leaving persistent mode")
    time.sleep(20)
    print("left persistent mode")

def voltage_sweep() :
    print("sweeping voltage for 60s")
    time.sleep(60)
    print("voltage sweep over")

single_sweep_time = 60.0

# sum(x * int(t) for x, t in zip([3600, 60, 1], time.split(":"))) 

# #map_measurement.write_period = 2

# #goToVoltage(HVch, start = HVch.voltage(), stop = stopHV, fastStep = 0.5, fastWait = 1)

# #sweep ranges for map
# LVsweep  = np.linspace(startLV, stopLV, NLV)

# with map_measurement.run(write_in_background=True) as datasaver:
#     for i, set_B in enumerate(np.linspace(startB, stopB, NB)): #magnetic field iteration
        
#         magnet.B(set_B)

#         goToVoltage(LVch, start = LVch.voltage(), stop = startLV, fastStep = 0.05, fastWait = 1)
        
#         B_sweep          = []
#         LVch_sweep       = []
#         Rxx_sweep        = []
#         Vxx_phase_sweep  = []
#         Rxy_sweep        = []
#         Vxy_phase_sweep  = []
#         Ileak_sweep      = []
#         T_sweep          = []
        
#         for set_LV in LVsweep : #back gate voltage iteration
            
#             LVch.voltage(set_LV)
#             time.sleep(dtLV)
            
#             B_sweep.append(set_B)
#             LVch_sweep.append(set_LV)
#             Rxx_sweep.append(Rxx())
#             Vxx_phase_sweep.append(Vxx_phase())
#             Rxy_sweep.append(Rxy())
#             Vxy_phase_sweep.append(Vxy_phase())
#             Ileak_sweep.append(Ileak())
#             T_sweep.append(T())
            
#         datasaver.add_result((magnet.B, B_sweep),           # 1st independent parameter
#                              (LVch.voltage, LVch_sweep),    # 2nd independent parameter
#                              (Rxx, Rxx_sweep),              # 1st dependent parameter
#                              (Vxx_phase, Vxx_phase_sweep),  # 2nd dependent parameter
#                              (Rxy, Rxy_sweep),              # 3nd dependent parameter
#                              (Vxy_phase, Vxy_phase_sweep),  # 4th dependent parameter
#                              (Ileak, Ileak_sweep),          # 5th dependent parameter
#                              (T, T_sweep))                  # 6th dependent parameter

#     # Convenient to have for plotting and data access
#     dataset = datasaver.dataset


