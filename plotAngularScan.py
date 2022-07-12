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
  parser = argparse.ArgumentParser(description="angular scan")
  parser.add_argument('-file', help="CSV file to be parsed")

  args = parser.parse_args()
  run_list = parseCSV(args.file)
  stub_efficiency, angles = [], []
  for run in run_list:
    run_number, angle = run["RunNumber"], run["Angle"]
    print(f'Run Number : {run_number}, Angle : {angle}')
    #Get result file
    result_file = TFile(f'/nfs/dust/cms/user/yotarid/Tracker/PSAnalysis/corryvreckan/output/analyze/run{run_number}/analysis_psmodule_stubs.root', 'READ')
    stub_total_efficiency = result_file.AnalysisStubEfficiency.eTotalEfficiency
    #Get stub efficiency
    angles.append(int(angle))
    stub_efficiency.append(stub_total_efficiency.GetEfficiency(1) * 100)

  stub_plot = plt.plot(angles, stub_efficiency, linestyle='solid', linewidth=2, marker='o', color='green')
  plt.xticks(np.arange(0, 30, 5))
  plt.title("DESY26_2 Angular scan @Threshold(5k, 5k)(SSA, MPA)")
  plt.xlabel("Angle [deg]")
  plt.ylabel("Stub Efficiency [%]")
  plt.grid()
  # plt.show()
  plt.savefig("./plots/AngularScan_StubEfficiency_DESY26_2.png")

if __name__ == "__main__":
  sys.exit(main())
