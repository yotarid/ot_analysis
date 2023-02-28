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
  parser.add_argument('-csv', help="CSV file to be parsed")

  args = parser.parse_args()

  csv_file = parseCSV(args.csv)

  #psp_v_list, pss_v_list, module_v_list, psp_i_list, pss_i_list, module_i_list = [], [], [], [], [], []
  v_dict, i_dict = {}, {}
  sensors = []
  for line in csv_file:
    sensor, iv_file = line["sensor"], parseCSV("./results/"+line["file"])
    sensors.append(sensor)
    i_temp, v_temp = [], []
    for iv_line in iv_file:
      v, i = -float(iv_line["voltage"]), -float(iv_line["current"])
      #restrict to -300V
      if v > 300: continue
      v_temp.append(v)
      i_temp.append(i)
    v_dict[sensor] = v_temp      
    i_dict[sensor] = i_temp      
    
  fig1, ax1 = plt.subplots()

  ax1.plot(v_dict["PS_40_05_DSY-00003"], i_dict["PS_40_05_DSY-00003"], linestyle='-', linewidth=1, marker='o', markersize=3,  label="PS_40_05_DSY-00003")    
  ax1.plot(v_dict["PS_40_05_DSY-00004"], i_dict["PS_40_05_DSY-00004"], linestyle='-', linewidth=1, marker='o', markersize=3,  label="PS_40_05_DSY-00004")    
  ax1.plot(v_dict["PS_40_05_DSY-00005"], i_dict["PS_40_05_DSY-00005"], linestyle='-', linewidth=1, marker='o', markersize=3,  label="PS_40_05_DSY-00005")    

  ax1.set_xlabel("Voltage (V)", fontsize=16)
  ax1.set_ylabel("Current (A)", fontsize=16)
  ax1.set_box_aspect(1)
  #plt.ticklabel_format(axis='both', style='sci')
  legend = ax1.legend(loc='upper left', ncol=1, fontsize=16, bbox_to_anchor=(1., 1.03))
  plt.grid(zorder=0, alpha=0.5)
  plt.savefig("./plots/iv_measurement_modules.pdf", bbox_inches="tight")


  fig2, ax2 = plt.subplots()

  ax2.plot(v_dict["PS_40_05_DSY-00005 PS-p"], i_dict["PS_40_05_DSY-00005 PS-p"], linestyle='-', linewidth=1, marker='o', markersize=3, label="PS-p")    
  ax2.plot(v_dict["PS_40_05_DSY-00005 PS-s"], i_dict["PS_40_05_DSY-00005 PS-s"], linestyle='-', linewidth=1, marker='o', markersize=3, label="PS-s")    
  ax2.plot(v_dict["PS_40_05_DSY-00005 No VTRx+"], i_dict["PS_40_05_DSY-00005 No VTRx+"], linestyle='-', linewidth=1, marker='o', markersize=3, label="Module w/o VTRx+")    
  ax2.plot(v_dict["PS_40_05_DSY-00005"], i_dict["PS_40_05_DSY-00005"], linestyle='-', linewidth=1, marker='o', markersize=3, label="Module w/ VTRx+")    

  ax2.set_xlabel("Voltage (V)", fontsize=16)
  ax2.set_ylabel("Current (A)", fontsize=16)
  ax2.set_box_aspect(1)
  legend = ax2.legend(loc='upper left', ncol=1, fontsize=16, bbox_to_anchor=(1., 1.03))
  plt.grid(zorder=0, alpha=0.5)
  plt.savefig("./plots/iv_measurement_assembly.pdf", bbox_inches="tight")



  fig1, ax1 = plt.subplots()
        
if __name__ == "__main__":
  sys.exit(main())

