from ROOT import TFile 
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

def fit_func(x, p0, p1, p2, p3):
    return 1 - 1/2 * (p0 + p1*special.erf((x-p2)/p3))

def main():
  parser = argparse.ArgumentParser(description="angular scan")
  parser.add_argument('-file', help="CSV file to be parsed")
  parser.add_argument('-campaign', help="Beam Test campaign")

  args = parser.parse_args()

  run_list = parseCSV(args.file)
  campaign = args.campaign
  psp_efficiencies, pss_efficiencies, stub_efficiencies, stub_efficiencies_pos, stub_efficiencies_neg, angles_pos, angles_neg, angles  = [], [], [], [], [], [], [], []

  for run in run_list:
    run_number, angle = run["RunNumber"], float(run["Angle"])
    print(f'Run Number : {run_number}, Angle : {angle}')
    #Get result file
    result_file = TFile(f'/nfs/dust/cms/user/yotarid/Tracker/PSAnalysis/corryvreckan/output/run{run_number}/analyze/analysis_psmodule.root', 'READ')

    # #Get PS-s and PS-p total efficiency profile
    psp_efficiency_vs_tdc = result_file.AnalysisEfficiency.CMSPhase2_30.efficiencyVsTagTProfile_TDC
    pss_efficiency_vs_tdc = result_file.AnalysisEfficiency.CMSPhase2_31.efficiencyVsTagTProfile_TDC
    stub_efficiency_vs_tdc = result_file.AnalysisStubEfficiency.efficiencyVsTagTProfile_TDC

    psp_tdc_efficiencies, pss_tdc_efficiencies, stub_tdc_efficiencies = [], [], []
    for tdc in range(0,9):
       psp_tdc_efficiencies.append(psp_efficiency_vs_tdc.GetBinContent(tdc))
       pss_tdc_efficiencies.append(pss_efficiency_vs_tdc.GetBinContent(tdc))
       stub_tdc_efficiencies.append(stub_efficiency_vs_tdc.GetBinContent(tdc))
    #Get PS-s, PS-p and Stub  efficiencies
    max_psp_efficiency = max(psp_tdc_efficiencies)
    max_pss_efficiency = max(pss_tdc_efficiencies)
    max_stub_efficiency = max(stub_tdc_efficiencies)
    print(f'Angle = {angle} ; PS-p efficiecy = {max_psp_efficiency}')
    print(f'Angle = {angle} ; PS-s efficiecy = {max_pss_efficiency}')
    print(f'Angle = {angle} ; Stub efficiecy = {max_stub_efficiency}')
    print(f'')

    angles.append(angle)
    psp_efficiencies.append(max_psp_efficiency * 100)
    pss_efficiencies.append(max_pss_efficiency * 100)
    stub_efficiencies.append(max_stub_efficiency * 100)

    if angle >= 0 :
      angles_pos.append(angle)
      stub_efficiencies_pos.append(max_stub_efficiency)
    else:
      angles_neg.append(angle)
      stub_efficiencies_neg.append(max_stub_efficiency)

  #params, cov = optimize.curve_fit(fit_func, np.array(angles), np.array(stub_efficiency), p0=[1, 1, 15, 1], maxfev=8000)
  params_pos, cov_pos = optimize.curve_fit(fit_func, np.array(angles_pos), np.array(stub_efficiencies_pos), maxfev=10000)
  params_neg, cov_neg = optimize.curve_fit(fit_func, np.array(angles_neg), np.array(stub_efficiencies_neg), maxfev=10000)
  #params_pos[0] = params_neg[0]
  #params_pos[1] = params_neg[1]
  ##params_pos[2] = -params_neg[2]
  #params_pos[3] = -params_neg[3]
  print(params_pos, params_neg)
  #print(params_pos)

  psp_plot = plt.plot(angles, psp_efficiencies, linestyle='solid', linewidth=2, marker='o', color='darkred', label='PS-p')
  pss_plot = plt.plot(angles, pss_efficiencies, linestyle='solid', linewidth=2, marker='o', color='navy', label='PS-s')
  #plt.xticks(np.arange(-40, 40, 10))
  #plt.xlim([-40, 40])
  #plt.ylim([0, 105])
  #plt.title("Angular scan at 300V bias voltage, 90 ThDAC MPA, 50 ThDAC SSA")
  #plt.xlabel("Angle (degrees)")
  #plt.ylabel("Hit Efficiency (%)")
  #plt.grid()
  ## plt.show()
  #plt.savefig("./plots/AngularScan_"+campaign+"_HitEfficiency_Dobby.png")

  #plt.clf()

  stub_plot = plt.plot(angles, stub_efficiencies, linestyle='None', marker='o', color='darkgreen', label="Stubs")
  fit_plot_pos = plt.plot(range(-6, 35, 1), np.array(fit_func(range(-6, 35, 1), *params_pos))*100, linestyle='-', linewidth=2.5, color='darkgreen')
  fit_plot_neg = plt.plot(range(-1, -35, -1), np.array(fit_func(range(-1, -35, -1), *params_neg))*100, linestyle='-', linewidth=2.5, color='darkgreen')
  plt.xticks(np.arange(-40, 40, 5))
  plt.xlim([-40, 40])
  plt.ylim([0, 105])
  plt.xlabel("Angle (degrees)")
  plt.ylabel("Efficiency (%)")
  plt.legend(loc="center left")
  plt.grid()
  plt.savefig("./plots/AngularScan_Efficiency_"+campaign+".png")

if __name__ == "__main__":
  sys.exit(main())
