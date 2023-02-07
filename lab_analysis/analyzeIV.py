import csv, argparse, sys
import matplotlib.pyplot as plt
import numpy as np
import math
from matplotlib.ticker import ScalarFormatter
from scipy import optimize, special
import matplotlib
matplotlib.use('Agg')

def parseCSV(file_path):
  print('Parsing CSV file : {}'.format(file_path))
  csv_file = open(file_path, mode='r') 
  return csv.DictReader(csv_file)

def main():
  parser = argparse.ArgumentParser(description="IV Measurement")
  parser.add_argument('-file', help="CSV file to be parsed")

  args = parser.parse_args()

  iv_files = parseCSV(args.file)

  psp_v_list, pss_v_list, module_v_list, psp_i_list, pss_i_list, module_i_list = [], [], [], [], [], []
  for line in iv_files:
    sensor, iv_file = line["sensor"], parseCSV("./results/"+line["file"])
    for iv_line in iv_file:
      voltage, current = -float(iv_line["voltage"]), -float(iv_line["current"])
      #restrict to -300V
      if voltage > 300: continue
      #avoid voltage duplication
      #fill proper container
      if sensor == "psp":
        psp_i_list.append(current)
        psp_v_list.append(voltage)
      elif sensor == "pss":
        pss_i_list.append(current)
        pss_v_list.append(voltage)
      else:
        module_i_list.append(current)
        module_v_list.append(voltage)
    
  plt.plot(psp_v_list, psp_i_list, linestyle='-', marker='o', markersize=3, color="darkred", label="PS-p")    
  plt.plot(pss_v_list, pss_i_list, linestyle='-', marker='o', markersize=3, color="navy", label="PS-s")    
  plt.plot(module_v_list, module_i_list, linestyle='-', marker='o', markersize=3, color="black", label="PS module")    
  plt.xlabel("Voltage (V)")
  plt.ylabel("Current (A)")
  #plt.ticklabel_format(axis='both', style='sci')
  plt.legend(loc="center right")
  plt.grid(zorder=0, alpha=0.5)

  plt.savefig("./plots/iv_measurement.pdf", bbox_inches="tight")
        
if __name__ == "__main__":
  sys.exit(main())

