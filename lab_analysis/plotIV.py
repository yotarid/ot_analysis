
import matplotlib.pyplot as plt
import csv, sys, argparse
import numpy as np

rampUpVoltage = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200,
                   210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310, 320, 330, 340, 350, 360, 370, 380, 390, 400]

DESY26_2_I_withVTRx = [3.24, 3.35, 3.40, 3.43, 3.46, 3.48, 3.50, 3.52, 3.54, 3.56, 3.58, 3.60, 3.62, 3.64, 3.66, 3.68, 3.70, 
                                            3.70, 3.70, 3.72, 3.72, 3.72, 3.74, 3.75, 3.76, 3.77, 3.78, 3.79, 3.79, 3.80, 3.80, 3.81, 3.81, 3.82, 3.83, 3.83, 3.84, 3.84, 3.85, 3.86, 3.87]
  
DESY26_2_I_withoutVTRx = [0.34, 0.43, 0.46, 0.49, 0.51, 0.53, 0.55, 0.57, 0.59, 0.61, 0.63, 0.65, 0.66, 0.68, 0.69, 0.70, 0.72, 
                                               0.73, 0.74, 0.75, 0.76, 0.77, 0.77, 0.78, 0.78, 0.79, 0.80, 0.80, 0.80, 0.80, 0.81, 0.81, 0.82, 0.82, 0.82, 0.83, 0.83, 0.84, 0.84, 0.85, 0.85]

DESY40_3_I_withVTRx = [3.68, 3.90, 4.01, 4.07, 4.11, 4.16, 4.20, 4.26, 4.33, 4.36, 4.41, 4.47, 4.52, 4.56, 4.62, 4.67, 4.72, 4.76, 4.80, 4.82, 4.84, 4.90, 4.90, 4.91, 4.93, 4.95, 4.96, 4.96, 4.96, 4.99, 5.00, 5.01, 5.01, 5.02, 5.03, 5.06, 5.06, 5.06, 5.06, 5.06, 5.06]

plt.plot(rampUpVoltage, DESY26_2_I_withVTRx, linestyle='-', marker='o', markersize=5, color='navy', label='DESY26_2 (VTRx+ plugged)')
plt.plot(rampUpVoltage, DESY26_2_I_withoutVTRx, linestyle='-', marker='o', markersize=5, color='tomato', label='DESY26_2 (VTRx+ unplugged)')
plt.plot(rampUpVoltage, DESY40_3_I_withVTRx, linestyle='-', marker='o', markersize=5, color='darkgreen', label='DESY40_3 (VTRx+ plugged)')

plt.xlabel("Voltage [V]")
plt.xlim(-5, 410)
plt.ylabel("Current [uA]")
plt.title("I-V measurement")
plt.legend(loc="upper left", fontsize=10)
plt.grid()
# plt.show()
plt.savefig("./plots/" + "DESY_IV_measurement.png")
 
