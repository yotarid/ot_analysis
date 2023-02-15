import csv, argparse, sys
import numpy as np
import math
from scipy import optimize, special
import matplotlib
matplotlib.rc('font',family='Times New Roman') 
matplotlib.rc('xtick', labelsize=16)
matplotlib.rc('ytick', labelsize=16)
import matplotlib.pyplot as plt
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
    
    
  fig, ax = plt.subplots()

  ax.plot(psp_v_list, psp_i_list, linestyle='-', linewidth=3, marker='o', markersize=3, color="darkred", label="PS-p")    
  ax.plot(pss_v_list, pss_i_list, linestyle='-', linewidth=3, marker='o', markersize=3, color="navy", label="PS-s")    
  ax.plot(module_v_list, module_i_list, linestyle='-', linewidth=3, marker='o', markersize=3, color="black", label="PS module")    
  ax.set_xlabel("Voltage (V)", fontsize=16)
  ax.set_ylabel("Current (A)", fontsize=16)
  ax.set_box_aspect(1)
  #plt.ticklabel_format(axis='both', style='sci')
  plt.legend(loc="center right", fontsize=16, bbox_to_anchor=(1.53, 0.87))
  plt.grid(zorder=0, alpha=0.5)

  plt.savefig("./plots/iv_measurement.pdf", bbox_inches="tight")
        
if __name__ == "__main__":
  sys.exit(main())

