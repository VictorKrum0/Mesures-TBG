import numpy as np
import scipy as sc
import pandas as pd
from matplotlib import pyplot as plt
import qcodes as qc 
from qcodes.dataset import initialise_database, initialise_or_create_database_at, load_experiment_by_name, plot_dataset, load_by_run_spec

import seaborn as sns

# Warning : This program causes the data to saturate for visualization purposes.

# Excution parameters -----------------------------------------------------------------
if True :
    initialise_or_create_database_at("Database_copy/Sofiane_Michael_TBG02.db") #open the right database
    #experiment_name = "Landau"
    run_ID = 192
    odd = True # selects either odd (True) or even (False) rows of the landau map

    Landau_plot = False

    row_select_plot = True
    row_select_idxs = [70,71,80,81]

    col_select_plot = False
    col_select_idxs = [50,100,150,200]
# --------------------------------------------------------------------------------------

# Extract the data for the parameters you want to plot, in the np.array format --------
if True :
    dataset = load_by_run_spec(captured_run_id = run_ID) # access the desired item from the open database
    data = dataset.get_parameter_data() # the dictionary with nested dictionaries for each dependent parameter

    Rc = data['Rc']['Rc'].reshape((95,201))
    print(Rc.shape)
    R = data['R']['R'].reshape((95,201))
    print(R.shape)
    B = data['Rc']['IPS120_B'].reshape((95,201))
    print(B.shape)
    Vbg = data['Rc']['HV090_CH02_voltage'].reshape((95,201))
    print(Vbg.shape)
    all_parameters = [Rc, R, B, Vbg]
# --------------------------------------------------------------------------------------

# Transformations on the data -----------------------------------------------------------
dRc = np.diff(Rc, axis=1) # differentiate the array along the voltage direction - must adapt axes
if True :
    M = 1e4
    #R = np.clip(R, 0, M)  # limit values in the array to not exceed M
    M = 100
    dRc = np.clip(dRc, -M, M)  # limit values in the array to not exceed M
    M = 1.4e4
    #Rc = np.clip(Rc, 0, M)  # limit values in the array to not exceed M
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

    for ax in [ax1, ax2] :
        ax.set_ylabel("B (T)")
        ax.set_xlabel("Vbg (V)")

    ax1.set_title("R")
    ax2.set_title("dR")
    ax3.set_title("FFT")

    # plt.colorbar(ax1.pcolormesh(Vbg[offset::2], B[offset::2], np.log(Rc[offset::2]), cmap='RdBu'), cb1)
    # plt.colorbar(ax2.pcolormesh(Vbg[offset::2][:,:-1], B[offset::2][:,:-1], np.sqrt(dRc[offset::2]), cmap='RdBu'), cb2)
    # plt.colorbar(ax3.pcolormesh(Vbg[offset::2], B[offset::2], sc.fft2(Rc[offset::2]), cmap='RdBu'), cb2)

    n = 70
    FFT_mod = sc.fft.fft(Rc[n])

    plt.figure()
    plt.title("Mean of absolute derivatives (Noise level)")
    noise_level_est = np.mean(np.absolute(dRc), axis=1)
    plt.plot(B[:,0], noise_level_est)
    plt.hlines(65,6,7, linestyles="dashed", colors="r")
    good_idxs = [i for i in range(len(B[:,0])) if noise_level_est[i] <= 65]
    bool_good_idxs = [True if i in good_idxs else False for i in range(len(B[:,0]))]

    plt.colorbar(ax1.pcolormesh(Vbg, B, np.log(Rc), cmap='RdBu'), cb1)
    plt.colorbar(ax2.pcolormesh(Vbg[:,:-1], B[:,:-1], dRc, cmap='RdBu'), cb2)
    plt.colorbar(ax3.pcolormesh(Vbg[:,:-1][bool_good_idxs], B[:,:-1][bool_good_idxs], dRc[bool_good_idxs], cmap='RdBu'), cb3)
    plt.legend()
    #plt.colorbar(ax3.pcolormesh(np.linspace(0,1,FFT_x), np.linspace(0,1,FFT_y), FFT_mod, cmap='RdBu'), cb3)

    #plt.figure()
    #sns.heatmap(np.log(FFT_mod))

# --------------------------------------------------------------------------------------

# Plot the data - Row Select -----------------------------------------------------------
k = 1
l = 1
if row_select_plot :
    fig, axes = plt.subplots(1, 2)
    axes[0].grid(True)
    axes[1].grid(True)
    for i, row_idx in enumerate(row_select_idxs) :
        signal = Rc[row_idx]
        axes[0].plot(Vbg[i%2], signal, label = f'B = {B[row_idx, 0]} T') 
        axes[0].set_title("Voltage Sweep at Cst B.")
        axes[0].set_ylabel("Rc ($\Omega$)")
        axes[0].set_xlabel("Vbg (V)")
        signal = dRc[row_idx]
        axes[1].plot(Vbg[i%2][1:], signal, label = f'B = {B[row_idx, 0]} T') 
        axes[1].set_title("Voltage Sweep at Cst B.")
        axes[1].set_ylabel("dRc ($\Omega$)")
        axes[1].set_xlabel("Vbg (V)")
    plt.legend(draggable=True)
# --------------------------------------------------------------------------------------

# Plot the data - Column Select -----------------------------------------------------------
if col_select_plot :
    fig, ax = plt.subplots(1, 1)
    ax.grid(True)
    for i, col_idx in enumerate(col_select_idxs) :
        ax.plot(B[:,col_idx][::2], Rc[:,col_idx][::2], label = f'Vbg = {Vbg[0,col_idx]} V') 
        ax.set_title("Effect of B at cst Vbg")
        ax.set_ylabel("Rc ($\Omega$)")
        ax.set_xlabel("B (T)")
    ax.legend()
# --------------------------------------------------------------------------------------


plt.show()