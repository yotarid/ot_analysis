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

from matplotlib.ticker import ScalarFormatter

def parseCSV(file_path):
  print('Parsing CSV file : {}'.format(file_path))
  csv_file = open(file_path, mode='r') 
  return csv.DictReader(csv_file)

def main():
  parser = argparse.ArgumentParser(description="resource utilization")
  parser.add_argument('-file', help="CSV file to be parsed")

  args = parser.parse_args()

  resource_table = parseCSV(args.file)

  firmware_list, lookup_tables_list, flipflops_list, block_rams_list = [], [], [], []
  for resources in resource_table:
    firmware, lookup_tables, flipflops, block_rams = str(resources["firmware"]), float(resources["LUT"]), float(resources["FF"]), float(resources["BRAM"])
    firmware_list.append(firmware)
    lookup_tables_list.append(lookup_tables)
    flipflops_list.append(flipflops)
    block_rams_list.append(block_rams)

  fix, ax1 = plt.subplots()
  plt.tight_layout()
  plot_lut = ax1.bar(np.linspace(1,5,3), lookup_tables_list, 0.5, align='center', color='steelblue', alpha=1, label='LUTs', zorder=3)
  plot_ff = ax1.bar(np.linspace(1.5,5.5,3), flipflops_list, 0.5, align='center', color='slategrey', alpha=1, label='FFs', zorder=3)
  plot_ram = ax1.bar(np.linspace(2,6,3), block_rams_list, 0.5, align='center', color='darkslategrey', alpha=1, label='BRAMs', zorder=3)

  ax1.set_ylim([0, 100])
  ax1.set_ylabel("Resource utilization (%)", fontsize=16)
  ax1.set_box_aspect(1)
  plt.xticks(np.linspace(1.5,5.5,3), firmware_list)
  plt.grid(zorder=0, alpha=0.5)

  #plt.legend(loc="upper right", ncol=3, fontsize=16, bbox_to_anchor=(0.975, 1.12))
  legend = ax1.legend(loc='upper left', ncol=1, fontsize=16, bbox_to_anchor=(1., 1.03))
  #plt.legend(loc="upper right", ncol=3, fontsize=12, bbox_to_anchor=(0.1,0.9,0.5,0.1))
  plt.savefig("./plots/resource_utilization.pdf", bbox_inches="tight")
    

if __name__ == "__main__":
  sys.exit(main())
 




