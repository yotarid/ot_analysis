from ROOT import TFile 
import csv, argparse, sys
import numpy as np
import math
from scipy import optimize, special
import matplotlib
import matplotlib.pyplot as plt
matplotlib.rc('font',family='Times New Roman') 
matplotlib.rc('xtick', labelsize=16)
matplotlib.rc('ytick', labelsize=16)
matplotlib.use('Agg')
from matplotlib.ticker import ScalarFormatter, MaxNLocator

def parseCSV(file_path):
  print('Parsing CSV file : {}'.format(file_path))
  csv_file = open(file_path, mode='r') 
  return csv.DictReader(csv_file)

def fit_func(x, p0, p1, p2, p3):
    return 1 - 1/2 * (p0 + p1*special.erf((x-p2)/p3))

def calculateError(eff, ntracks):
  return np.sqrt((eff * (1 - eff))/ntracks)

def main():
  parser = argparse.ArgumentParser(description="bias scan")
  parser.add_argument('-csv', help="CSV file to be parsed")
  parser.add_argument('-folder', help="Results folder")
  parser.add_argument('-campaign', help="Beam Test campaign")

  args = parser.parse_args()

  run_list = parseCSV(args.csv)
  folder = args.folder
  campaign = args.campaign
  psp_efficiencies, pss_efficiencies, stub_efficiencies, stub_efficiencies_pos, stub_efficiencies_neg, angles_pos, angles_neg, angles  = [], [], [], [], [], [], [], []
  psp_efficiencies_err, pss_efficiencies_err, stub_efficiencies_err = [], [], [] 

  for run in run_list:
    run_number, angle = run["RunNumber"], float(run["Angle"])
    print(f'Run Number : {run_number}, Angle : {angle}')
    #Get result file
    result_file = TFile(f'{folder}/output/run{run_number}/analyze/analysis_psmodule.root', 'READ')

    # #Get PS-s and PS-p total efficiency profile
    psp_efficiency_vs_tdc = result_file.AnalysisEfficiency.CMSPhase2_30.efficiencyVsTagTProfile_TDC
    pss_efficiency_vs_tdc = result_file.AnalysisEfficiency.CMSPhase2_31.efficiencyVsTagTProfile_TDC
    stub_efficiency_vs_tdc = result_file.AnalysisStubEfficiency.efficiencyVsTagTProfile_TDC

    psp_tdc_efficiencies, pss_tdc_efficiencies, stub_tdc_efficiencies = [], [], []
    psp_tdc_efficiencies_ntrack, pss_tdc_efficiencies_ntrack, stub_tdc_efficiencies_ntrack = [], [], [] 
    for tdc in range(0,9):
       psp_tdc_efficiencies.append(psp_efficiency_vs_tdc.GetBinContent(tdc))
       psp_tdc_efficiencies_ntrack.append(psp_efficiency_vs_tdc.GetBinEntries(tdc))

       pss_tdc_efficiencies.append(pss_efficiency_vs_tdc.GetBinContent(tdc))
       pss_tdc_efficiencies_ntrack.append(pss_efficiency_vs_tdc.GetBinEntries(tdc))

       stub_tdc_efficiencies.append(stub_efficiency_vs_tdc.GetBinContent(tdc))
       stub_tdc_efficiencies_ntrack.append(stub_efficiency_vs_tdc.GetBinEntries(tdc))

    #Get PS-s, PS-p and Stub  efficiencies
    max_psp_efficiency = max(psp_tdc_efficiencies)
    psp_ntrack = psp_tdc_efficiencies_ntrack[psp_tdc_efficiencies.index(max_psp_efficiency)]

    max_pss_efficiency = max(pss_tdc_efficiencies)
    pss_ntrack = pss_tdc_efficiencies_ntrack[pss_tdc_efficiencies.index(max_pss_efficiency)]

    max_stub_efficiency = max(stub_tdc_efficiencies)
    stub_ntrack = stub_tdc_efficiencies_ntrack[stub_tdc_efficiencies.index(max_stub_efficiency)]
    print(f'Angle = {angle} ; PS-p efficiecy = {max_psp_efficiency}')
    print(f'Angle = {angle} ; PS-s efficiecy = {max_pss_efficiency}')
    print(f'Angle = {angle} ; Stub efficiecy = {max_stub_efficiency}')
    print(f'')

    angles.append(angle)
    psp_efficiencies.append(max_psp_efficiency)
    psp_efficiencies_err.append(calculateError(max_psp_efficiency, psp_ntrack))

    pss_efficiencies.append(max_pss_efficiency)
    pss_efficiencies_err.append(calculateError(max_pss_efficiency, pss_ntrack))

    stub_efficiencies.append(max_stub_efficiency)
    stub_efficiencies_err.append(calculateError(max_stub_efficiency, stub_ntrack))

    if angle >= 0 :
      angles_pos.append(angle)
      stub_efficiencies_pos.append(max_stub_efficiency)
    else:
      angles_neg.append(angle)
      stub_efficiencies_neg.append(max_stub_efficiency)

  #params, cov = optimize.curve_fit(fit_func, np.array(angles), np.array(stub_efficiency), p0=[1, 1, 15, 1], maxfev=8000)
  params_pos, cov_pos = optimize.curve_fit(fit_func, np.array(angles_pos), np.array(stub_efficiencies_pos), maxfev=10000)
  params_neg, cov_neg = optimize.curve_fit(fit_func, np.array(angles_neg), np.array(stub_efficiencies_neg), maxfev=10000)
  print(params_pos, params_neg)

  fig, ax = plt.subplots()
  plt.tight_layout()

  psp_plot = ax.errorbar(angles, psp_efficiencies, yerr=psp_efficiencies_err, linestyle='-', linewidth=1, marker='o', markersize=5, color='darkred', label='PS-p')
  pss_plot = ax.errorbar(angles, pss_efficiencies, yerr=pss_efficiencies_err, linestyle='-', linewidth=1, marker='o', markersize=5, color='navy', label='PS-s')
  stub_plot = ax.errorbar(angles, stub_efficiencies, yerr=stub_efficiencies_err, linestyle='None', marker='o', markersize=5, color='darkgreen', label='Stubs')

  fit_plot_pos = plt.plot(np.linspace(-6, 35, 10000), np.array(fit_func(np.linspace(-6, 35, 10000), *params_pos)), linestyle='-', linewidth=1, color='darkgreen')
  fit_plot_neg = plt.plot(np.linspace(-1, -35, 10000), np.array(fit_func(np.linspace(-1, -35, 10000), *params_neg)), linestyle='-', linewidth=1, color='darkgreen')

  #plt.xticks(np.arange(-40, 40, 10))
  #ax.set_xlim([-40, 40])

  ax.set_xlabel('Angle ($^{\circ}$)', fontsize=16)
  ax.set_ylabel("Efficiency (%)", fontsize=16)
  #ax.legend(loc="center left")
  legend = ax.legend(loc='upper right', ncol=3, columnspacing=1.2, fontsize=16, bbox_to_anchor=(1., 1.15))
  ax.grid(alpha=0.5)
  ax.set_box_aspect(1)
  plt.savefig("./plots/angular_scan/angular_scan_efficiency_"+campaign+".pdf", bbox_inches="tight")


if __name__ == "__main__":
  sys.exit(main())
