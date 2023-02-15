#from ROOT import TGraph, TH1F, gStyle, TCanvas
import csv, sys, argparse
import numpy as np
import matplotlib
matplotlib.rc('font',family='Times New Roman') 
matplotlib.rc('xtick', labelsize=14)
matplotlib.rc('ytick', labelsize=14)
import matplotlib.pyplot as plt
matplotlib.use('Agg')

module_id = [1, 2, 3, 4, 5]
Tx = [20, 10, 5.5, 25, 4.5]
Ty = [67, 53, 66, 23.5, 3.7]
R = [174, 17, 192, 367, 34.9]

fig, ax1 = plt.subplots()

plt.tight_layout()
plt.grid(alpha=0.5)
ax1.set_xlabel("Module Id", fontsize=14)
ax1.set_ylim(0, 1000)
ax1.set_xlim(0, 6)
ax1.set_ylabel(r"R ($\mu rad$)", fontsize=14)
R_plot, = ax1.plot(module_id, R, linestyle='None', marker='o', markersize=9, color="darkgreen", label="R = rotation")
ax1.plot([0, 6], [800, 800], linestyle='dashed', marker='None', color="darkgreen", alpha=0.5)
plt.text(4.3+0.05, 800+6.5, "Tolerance on R", color="darkgreen", fontsize=12, alpha=0.5)
ax1.set_box_aspect(1)

ax2 = ax1.twinx()
ax2.set_ylabel(r"Tx, Ty ($\mu m$)", fontsize=14)
ax2.set_ylim(0, 200)

Tx_plot, = ax2.plot(module_id, Tx, linestyle='None', marker='s', markersize=9, color="darkred", label=r"Tx = translation $\perp$ to strips")
ax2.plot([0, 6], [50, 50], linestyle='dashed', marker='None', color="darkred", alpha=0.5)
plt.text(4.3+0.05, 50+2, "Tolerance on Tx", color="darkred", fontsize=12, alpha=0.5)

Ty_plot, = ax2.plot(module_id, Ty, linestyle='None', marker='d', markersize=9, color="darkblue", label=r"Ty = translation $\parallel$ to strips")
ax2.plot([0, 6], [100, 100], linestyle='dashed', marker='None', color="darkblue", alpha=0.5)
plt.text(4.3+0.05, 100+2, "Tolerance on Ty", color="darkblue", fontsize=12, alpha=0.5)
ax2.set_box_aspect(1)

plt.legend(handles = [R_plot, Tx_plot, Ty_plot], labels=["R = rotation", r"Tx = translation $\perp$ to strips", r"Ty = translation $\parallel$ to strips"], loc="upper right", fontsize=14, bbox_to_anchor=(0.87, 1.26))
#plt.legend(handles = [R_plot, Tx_plot, Ty_plot], labels=["R = rotation", r"Tx = translation $\perp$ to strips", r"Ty = translation $\parallel$ to strips"], fontsize=14, loc="upper left")
# plt.show()
plt.savefig("./plots/" + "metrology.pdf", bbox_inches="tight")




 




