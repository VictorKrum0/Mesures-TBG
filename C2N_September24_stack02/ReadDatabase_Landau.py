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
    run_ID = 180
    odd = True # selects either odd (True) or even (False) rows of the landau map

    Landau_plot = True

    row_select_plot = True
    row_select_idxs = [0,1,2,3,4,5]

    col_select_plot = False
    col_select_idxs = [10]
# --------------------------------------------------------------------------------------

# Extract the data for the parameters you want to plot, in the np.array format --------
if True :
    dataset = load_by_run_spec(captured_run_id = run_ID) # access the desired item from the open database
    data = dataset.get_parameter_data() # the dictionary with nested dictionaries for each dependent parameter

    Rc = data['Rc']['Rc'].reshape((401,151))
    print(Rc.shape)
    R = data['R']['R'].reshape((401,151))
    print(R.shape)
    B = data['Rc']['IPS120_B'].reshape((401,151))
    print(B.shape)
    Vbg = data['Rc']['HV090_CH02_voltage'].reshape((401,151))
    print(Vbg.shape)
    all_parameters = [Rc, R, B, Vbg]
# --------------------------------------------------------------------------------------

# Transformations on the data -----------------------------------------------------------
dRc = np.diff(Rc, axis=1) # differentiate the array along the voltage direction - must adapt axes
if False :
    M = 1e5
    R = np.clip(R, 0, M)  # limit values in the array to not exceed M
    M = 1e5 
    dRc = np.clip(dRc, -M, M)  # limit values in the array to not exceed M
    M = 2e4
    Rc = np.clip(Rc, 0, M)  # limit values in the array to not exceed M
offset = 1 if odd else 0
# --------------------------------------------------------------------------------------

# Plot the data - Color mesh for Rc, R, DR ----------------------------------------
if Landau_plot :
    fig = plt.figure(figsize=(18, 5))

    x0 = 0.05 #abs. abcissa of left 
    y0 = 0.1 #abs. height of bottom
    w = 0.235 #figure width
    wcb = 0.01 #cbar width
    h = 0.8 #figure height
    el = 0.01 #space between a figure and its cbar
    er = 0.07 #space between a cbar and the next figure

    # Manually define the position and size of each subplot (left, bottom, width, height) and colorbar
    ax1 = fig.add_axes([x0,                              y0, w,     h])  # First plot
    cb1 = fig.add_axes([x0+w+el,                         y0, wcb,   h])  # First cbar
    ax2 = fig.add_axes([x0+w+el+wcb+er,                  y0, w,     h])  # Second plot
    cb2 = fig.add_axes([x0+w+el+wcb+er+w+el,             y0, wcb,   h])  # Second cbar
    ax3 = fig.add_axes([x0+w+el+wcb+er+w+el+wcb+er,      y0, w,     h])  # Third plot
    cb3 = fig.add_axes([x0+w+el+wcb+er+w+el+wcb+er+w+el, y0, wcb,   h])  # third cbar

    for i in range(1,4) :
        fig.text(x0 + i*(w+el+wcb+er) - er - wcb, y0 + h + 0.01, "$\Omega$", fontsize = 13)

    for ax in [ax1, ax2, ax3] :
        ax.set_ylabel("B (T)")
        ax.set_xlabel("Vbg (V)")

    ax1.set_title("Rc")
    ax2.set_title("R")
    ax3.set_title("dRc")

    plt.colorbar(ax1.pcolormesh(Vbg[offset::2], B[offset::2], Rc[offset::2], cmap='RdBu'), cb1)
    plt.colorbar(ax2.pcolormesh(Vbg[offset::2], B[offset::2], R[offset::2], cmap='RdBu'), cb2)
    plt.colorbar(ax3.pcolormesh(Vbg[offset::2][:,:-1], B[offset::2][:,:-1], dRc[offset::2], cmap='RdBu'), cb3)
# --------------------------------------------------------------------------------------

# Plot the data - Row Select -----------------------------------------------------------
if row_select_plot :
    fig, ax = plt.subplots(1, 1)
    ax.grid(True)
    for i, row_idx in enumerate(row_select_idxs) :
        ax.plot(Vbg[i%2], Rc[row_idx], label = f'B = {B[row_idx, 0]} T') 
        ax.set_title("Voltage Sweep at Cst B.")
        ax.set_ylabel("Rc ($\Omega$)")
        ax.set_xlabel("Vbg (V)")
    ax.legend()
# --------------------------------------------------------------------------------------

# Plot the data - Column Select -----------------------------------------------------------
if col_select_plot :
    fig, ax = plt.subplots(1, 1)
    ax.grid(True)
    for i, col_idx in enumerate(col_select_idxs) :
        ax.plot(1/B[:,col_idx][::2], Rc[:,col_idx][::2], label = f'Vbg = {Vbg[0,col_idx]} V') 
        ax.set_title("Effect of B at cst Vbg")
        ax.set_xlim(xmin=0, xmax=1)
        ax.set_ylabel("Rc ($\Omega$)")
        ax.set_xlabel("B (T)")
    ax.legend()
# --------------------------------------------------------------------------------------

plt.show()