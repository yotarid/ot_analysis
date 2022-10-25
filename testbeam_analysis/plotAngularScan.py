from ROOT import TFile 
import csv, argparse, sys
import matplotlib.pyplot as plt
import numpy as np
import math
from matplotlib.ticker import ScalarFormatter
from scipy import optimize, special

def parseCSV(file_path):
  print(f'Parsing CSV file : {file_path}')
  csv_file = open(file_path, mode='r') 
  return csv.DictReader(csv_file)

def fit_func(x, p0, p1, p2, p3):
    return 1 - 1/2 * (p0 + p1*special.erf((x-p2)/p3))

def main():
  parser = argparse.ArgumentParser(description="angular scan")
  parser.add_argument('-file', help="CSV file to be parsed")

  args = parser.parse_args()
  run_list = parseCSV(args.file)
  stub_efficiency_pos, stub_efficiency_neg, stub_efficiency, angles_pos, angles_neg, angles = [], [], [], [], [], []
  for run in run_list:
    run_number, angle = run["RunNumber"], int(run["Angle"])
    print(f'Run Number : {run_number}, Angle : {angle}')
    #Get result file
    result_file = TFile(f'/nfs/dust/cms/user/yotarid/Tracker/PSAnalysis/corryvreckan/output/analyze/run{run_number}/analysis_psmodule_stubs.root', 'READ')
    stub_total_efficiency = result_file.AnalysisStubEfficiency.eTotalEfficiency
    #Get stub efficiency
    angles.append(angle)
    stub_efficiency.append(stub_total_efficiency.GetEfficiency(1))
    if angle >= 0 :
      angles_pos.append(angle)
      stub_efficiency_pos.append(stub_total_efficiency.GetEfficiency(1))
    else:
      angles_neg.append(angle)
      stub_efficiency_neg.append(stub_total_efficiency.GetEfficiency(1))

  #params, cov = optimize.curve_fit(fit_func, np.array(angles), np.array(stub_efficiency), p0=[1, 1, 15, 1], maxfev=8000)
  params_pos, cov_pos = optimize.curve_fit(fit_func, np.array(angles_pos), np.array(stub_efficiency_pos), maxfev=10000)
  params_neg, cov_neg = optimize.curve_fit(fit_func, np.array(angles_neg), np.array(stub_efficiency_neg), maxfev=10000)
  #params_pos[0] = params_neg[0]
  #params_pos[1] = params_neg[1]
  ##params_pos[2] = -params_neg[2]
  #params_pos[3] = -params_neg[3]
  print(params_pos, params_neg)
  stub_plot = plt.plot(angles, np.array(stub_efficiency)*100, linestyle='None', marker='o', markersize=10, color='darkgreen')
  fit_plot_pos = plt.plot(range(0, 30, 1), np.array(fit_func(range(0, 30, 1), *params_pos))*100, linestyle='-', linewidth=2.5, color='darkgreen')
  fit_plot_neg = plt.plot(range(-1, -30, -1), np.array(fit_func(range(-1, -30, -1), *params_neg))*100, linestyle='-', linewidth=2.5, color='darkgreen')
  plt.xticks(np.arange(-40, 40, 10))
  plt.xlim([-35, 35])
  plt.ylim([0, 105])
  #plt.title("DESY26_2 Angular scan @Threshold(5k, 5k)(SSA, MPA)")
  plt.title("Angular scan at 5k e- threshold for both MPA and SSA chips")
  plt.xlabel("Angle (degrees)")
  plt.ylabel("Stub Efficiency (%)")
  plt.grid()
  # plt.show()
  plt.savefig("./plots/AngularScan_StubEfficiency_NoMatch_DESY26_2.png")

if __name__ == "__main__":
  sys.exit(main())
