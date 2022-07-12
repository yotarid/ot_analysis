from ROOT import TFile 
import csv, argparse, sys
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import ScalarFormatter


def parseCSV(file_path):
  print(f'Parsing CSV file : {file_path}')
  csv_file = open(file_path, mode='r') 
  return csv.DictReader(csv_file)

def main():
  parser = argparse.ArgumentParser(description="threshold scan")
  parser.add_argument('-file', help="CSV file to be parsed")

  args = parser.parse_args()
  run_list = parseCSV(args.file)
  psp_efficiency, pss_efficiency, bias_voltage = [], [], []
  for run in run_list:
    run_number, voltage = run["RunNumber"], run["Voltage"]
    print(f'Run Number : {run_number}, Voltage : {voltage}')
    #Get result file
    result_file = TFile(f'/nfs/dust/cms/user/yotarid/Tracker/PSAnalysis/corryvreckan/output/analyze/run{run_number}/analysis_psmodule_hits.root', 'READ')
    # #Get PS-s and PS-p total efficiency profile
    psp_total_efficiency = result_file.AnalysisEfficiency.CMSPhase2_30.eTotalEfficiency
    pss_total_efficiency = result_file.AnalysisEfficiency.CMSPhase2_31.eTotalEfficiency
    #Get PS-s and PS-p total efficiency
    # psp_threshold.append(int(th)/94)
    bias_voltage.append(voltage)
    psp_efficiency.append(psp_total_efficiency.GetEfficiency(1) * 100)
    pss_efficiency.append(pss_total_efficiency.GetEfficiency(1) * 100)
    # print(f'PS-p efficiency = {psp_efficiency}, PS-s efficiency = {pss_efficiency}')

  psp_plot = plt.plot(bias_voltage, psp_efficiency, linestyle='solid', linewidth=2, marker='o', color='darkred', label='PS-p')
  pss_plot = plt.plot(bias_voltage, pss_efficiency, linestyle='solid', linewidth=2, marker='o', color='navy', label='PS-s')
  plt.title("DESY26_2 Bias scan @Threshold(5k, 5k)(SSA, MPA)")
  plt.xlabel("Voltage [V]")
  plt.ylabel("Efficiency [%]")
  plt.legend(loc="lower right")
  plt.grid()
  # plt.show()
  plt.savefig("./plots/BiasScan_HitEfficiency_DESY26_2.png")

if __name__ == "__main__":
  sys.exit(main())
