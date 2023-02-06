import matplotlib.pyplot as plt
import csv, sys, argparse
import numpy as np
import matplotlib
matplotlib.use('Agg')

module_id = [1, 2, 3, 4, 5]
Tx = [20, 10, 5.5, 25, 4.5]
Ty = [67, 53, 66, 23.5, 3.7]
R = [174, 17, 192, 367, 34.9]

fig, ax1 = plt.subplots()

ax1.set_xlabel("Module Id")
ax1.set_ylim(0, 1200)
ax1.set_xlim(0, 6)
ax1.set_ylabel(r"R ($\mu rad$)")
R_plot, = ax1.plot(module_id, R, linestyle='None', marker='o', markersize=7, color="darkgreen", label="R = rotation")
ax1.plot([0, 6], [800, 800], linestyle='dashed', marker='None', color="darkgreen")
plt.text(0+0.05, 800+6, "Tolerance on R", color="darkgreen")

ax2 = ax1.twinx()
ax2.set_ylabel(r"Tx, Ty ($\mu m$)")
ax2.set_ylim(0, 200)

Tx_plot, = ax2.plot(module_id, Tx, linestyle='None', marker='s', markersize=7, color="darkred", label=r"Tx = translation $\perp$ to strips")
ax2.plot([0, 6], [50, 50], linestyle='dashed', marker='None', color="darkred")
plt.text(0+0.05, 50+2, "Tolerance on Tx", color="darkred")

Ty_plot, = ax2.plot(module_id, Ty, linestyle='None', marker='d', markersize=7, color="darkblue", label=r"Ty = translation $\parallel$ to strips")
ax2.plot([0, 6], [100, 100], linestyle='dashed', marker='None', color="darkblue")
plt.text(0+0.05, 100+2, "Tolerance on Ty", color="darkblue")

plt.legend(handles = [R_plot, Tx_plot, Ty_plot], labels=["R = rotation", r"Tx = translation $\perp$ to strips", r"Ty = translation $\parallel$ to strips"], loc="upper right", fontsize=10)
plt.grid()
plt.tight_layout()
# plt.show()
plt.savefig("./plots/" + "metrology.pdf")
 




