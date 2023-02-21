import ROOT
from ROOT import TFile 
import csv, argparse, sys
import numpy as np
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
  psp_efficiencies, pss_efficiencies, stub_efficiencies, bias_voltages = [], [], [], []
  psp_efficiencies_err, pss_efficiencies_err, stub_efficiencies_err = [], [], [] 
  for run in run_list:
    run_number, bias = run["RunNumber"], run["Bias"]
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
    
    print(f'MPA Bias = {bias} ; PS-p efficiecy = {max_psp_efficiency}')
    print(f'SSA Bias = {bias} ; PS-s efficiecy = {max_pss_efficiency}')
    print(f'SSA Bias = {bias} ; Stub efficiecy = {max_stub_efficiency}')
    print(f'')

    bias_voltages.append(int(bias))
    psp_efficiencies.append(max_psp_efficiency)
    psp_efficiencies_err.append(calculateError(max_psp_efficiency, psp_ntrack))

    pss_efficiencies.append(max_pss_efficiency)
    pss_efficiencies_err.append(calculateError(max_pss_efficiency, pss_ntrack))

    stub_efficiencies.append(max_stub_efficiency)
    stub_efficiencies_err.append(calculateError(max_stub_efficiency, stub_ntrack))


  fig, ax = plt.subplots()
  plt.tight_layout()
  psp_plot = ax.errorbar(bias_voltages, psp_efficiencies, yerr=psp_efficiencies_err, linestyle='solid', linewidth=1, marker='o', markersize=5, color='darkred', label='PS-p')
  pss_plot = ax.errorbar(bias_voltages, pss_efficiencies, yerr=pss_efficiencies_err, linestyle='solid', linewidth=1, marker='o', markersize=5, color='navy', label='PS-s')
  stub_plot = ax.errorbar(bias_voltages, stub_efficiencies, yerr=stub_efficiencies_err, linestyle='solid', linewidth=1, marker='o', markersize=5, color='darkgreen', label='Stubs')
  ax.set_xlabel('Voltage (V)', fontsize=16)
  ax.set_ylabel("Efficiency", fontsize=16)
  #ax.legend(loc="center left")
  legend = ax.legend(loc='upper right', ncol=3, columnspacing=1.2, fontsize=16, bbox_to_anchor=(1., 1.15))
  ax.grid(alpha=0.5)
  ax.set_box_aspect(1)
  plt.savefig("./plots/bias_scan/bias_scan_efficiency_"+campaign+".pdf", bbox_inches="tight")

if __name__ == "__main__":
  sys.exit(main())
