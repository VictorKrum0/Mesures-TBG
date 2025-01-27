import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import qcodes as qc 
from qcodes.dataset import initialise_database, initialise_or_create_database_at, load_experiment_by_name, plot_dataset, load_by_run_spec

# Warning : This program causes the data to saturate for visualization purposes.

# Excution parameters -----------------------------------------------------------------
if True :
    initialise_or_create_database_at("Database/Sofiane_Michael_TBG02.db") #open the right database
    #experiment_name = "Landau"
    run_ID_list = [172,177]
    x_offsets = [55e-3,-51e-3]
# --------------------------------------------------------------------------------------

ind = 0

fig, axes = plt.subplots(1, 2)
axes[0].set_title("With Constriction")
axes[0].set_ylabel("Rc ($\Omega$)")
axes[0].set_xlabel("Vbg (V)")
axes[1].set_title("Without Constriction")
axes[1].set_ylabel("R ($\Omega$)")
axes[1].set_xlabel("Vbg (V)")

for run_ID in run_ID_list : 
    # Extract the data for the parameters you want to plot, in the np.array format --------
    if True :
        dataset = load_by_run_spec(captured_run_id = run_ID) # access the desired item from the open database
        data = dataset.get_parameter_data() # the dictionary with nested dictionaries for each dependent parameter

        Rc = data['Rc']['Rc']
        R = data['R']['R']
        Vbg = data['Rc']['HV090_CH02_voltage']
        all_parameters = [Rc, R, Vbg]
        print(Vbg.shape)
    # --------------------------------------------------------------------------------------

    # Transformations on the data -----------------------------------------------------------
    #dRc = np.diff(Rc, axis=1) # differentiate the array along the voltage direction - must adapt axes
    if False :
        M = 1e5
        R = np.clip(R, 0, M)  # limit values in the array to not exceed M
        M = 1e5 
        dRc = np.clip(dRc, -M, M)  # limit values in the array to not exceed M
        M = 2e4
        Rc = np.clip(Rc, 0, M)  # limit values in the array to not exceed M
    # --------------------------------------------------------------------------------------

    # Plot the data ------------------------------------------------------------------------
    ax = axes[0]
    ax.grid(True)
    ax.plot(Vbg + x_offsets[ind], Rc, label = f'Run ID {run_ID}') 
    ax.legend()

    ax = axes[1]
    ax.grid(True)
    ax.plot(Vbg + x_offsets[ind], R, label = f'Run ID {run_ID}') 
    ax.legend()
    # --------------------------------------------------------------------------------------

    ind += 1

plt.show()