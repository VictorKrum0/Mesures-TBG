import threading
import time

start_time = time.time() 

def short_func(num):
    time.sleep(2)
    print("Thread {}, Cube: {}, elapsed {}".format(threading.current_thread().name, num * num * num, time.time()-start_time))


def long_func(num):
    time.sleep(10)
    print("Thread {}, Square: {}, elapsed {}".format(threading.current_thread().name, num * num, time.time()-start_time))


if __name__ =="__main__":
    t1 = threading.Thread(target=short_func, args=(10,), name="t1")
    t2 = threading.Thread(target=long_func, args=(10,), name="t2")

    t1.start()
    t2.start()

    print("\nBoth threads have started. \n")

    t1.join()
    t2.join()

    print("Done!")


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


