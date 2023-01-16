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


  plt.bar(np.linspace(1,5,3), lookup_tables_list, 0.5, align='center', color='navy', label='LUTs')
  plt.bar(np.linspace(1.5,5.5,3), flipflops_list, 0.5, align='center', color='darkred', label='FFs')
  plt.bar(np.linspace(2,6,3), block_rams_list, 0.5, align='center', color='darkgreen', label='BRAMs')

  plt.ylim([0, 100])
  plt.ylabel("Resource Utilization (%)")
  plt.xticks(np.linspace(1.5,5.5,3), firmware_list)
  plt.grid()

  plt.legend(loc="upper right")
  plt.savefig("./plots/Resource_Utilization.pdf")
    

if __name__ == "__main__":
  sys.exit(main())
 




