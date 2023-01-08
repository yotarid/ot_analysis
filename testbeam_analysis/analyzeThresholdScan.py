import ROOT
from ROOT import TFile 
import csv, argparse, sys
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import ScalarFormatter
import matplotlib
matplotlib.use('Agg')


def parseCSV(file_path):
  print('Parsing CSV file : {}'.format(file_path))
  csv_file = open(file_path, mode='r') 
  return csv.DictReader(csv_file)

def main():
  parser = argparse.ArgumentParser(description="threshold scan")
  parser.add_argument('-file', help="CSV file to be parsed")
  parser.add_argument('-campaign', help="Beam Test campaign")
  parser.add_argument('-ThDAC', help="Plots in unit of electrons", action="store_true")

  args = parser.parse_args()

  run_list = parseCSV(args.file)
  campaign = args.campaign
  psp_efficiencies, pss_efficiencies, stub_efficiencies, mpa_thresholds, ssa_thresholds = [], [], [], [], []
  for run in run_list:
    run_number, th_MPA, th_SSA = run["RunNumber"], run["Threshold_MPA"], run["Threshold_SSA"]
    #Get result file
    result_file = TFile('/nfs/dust/cms/user/yotarid/Tracker/PSAnalysis/corryvreckan/output/run{}/analyze/analysis_psmodule.root'.format(run_number), 'READ')
    # #Get PS-s and PS-p total efficiency profile
    psp_efficiency_vs_tdc = result_file.AnalysisEfficiency.CMSPhase2_30.efficiencyVsTagTProfile_TDC
    pss_efficiency_vs_tdc = result_file.AnalysisEfficiency.CMSPhase2_31.efficiencyVsTagTProfile_TDC
    stub_efficiency_vs_tdc = result_file.AnalysisStubEfficiency.efficiencyVsTagTProfile_TDC

    psp_tdc_efficiencies, pss_tdc_efficiencies, stub_tdc_efficiencies = [], [], []
    for tdc in range(0,8):
       psp_tdc_efficiencies.append(psp_efficiency_vs_tdc.GetBinContent(tdc))
       pss_tdc_efficiencies.append(pss_efficiency_vs_tdc.GetBinContent(tdc))
       stub_tdc_efficiencies.append(stub_efficiency_vs_tdc.GetBinContent(tdc))
    #Get PS-s, PS-p and Stub  efficiencies
    max_psp_efficiency = max(psp_tdc_efficiencies)
    max_pss_efficiency = max(pss_tdc_efficiencies)
    max_stub_efficiency = max(stub_tdc_efficiencies)
    print(f'MPA Threshold = {th_MPA} ; PS-p efficiecy = {max_psp_efficiency}')
    print(f'SSA Threshold = {th_SSA} ; PS-s efficiecy = {max_pss_efficiency}')
    print(f'SSA Threshold = {th_SSA} ; Stub efficiecy = {max_stub_efficiency}')
    print(f'')

    mpa_thresholds.append(int(th_MPA))
    psp_efficiencies.append(max_psp_efficiency * 100)
    ssa_thresholds.append(int(th_SSA))
    pss_efficiencies.append(max_pss_efficiency * 100)
    stub_efficiencies.append(max_stub_efficiency * 100)

  psp_plot = plt.plot(mpa_thresholds, psp_efficiencies, linestyle='solid', linewidth=2, marker='o', color='darkred', label='PS-p')
  pss_plot = plt.plot(ssa_thresholds, pss_efficiencies, linestyle='solid', linewidth=2, marker='o', color='navy', label='PS-s')
  stub_plot = plt.plot(ssa_thresholds, stub_efficiencies, linestyle='solid', linewidth=2, marker='o', color='darkgreen', label='Stubs')
  #plt.title("DESY26_2 Threshold scan @Bias(300V)")
  #plt.title("Threshold scan at 300V bias voltage")
  plt.xlabel('Threshold (DAC)')
  #plt.ylim((0, 105))
  plt.ylabel("Efficiency (%)")
  plt.legend(loc="center left")
  plt.grid()
  # plt.show()
  plt.savefig("./plots/ThresholdScan_"+campaign+"_Efficiency_Dobby.png")




if __name__ == "__main__":
  sys.exit(main())
