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
  parser = argparse.ArgumentParser(description="bias scan")
  parser.add_argument('-file', help="CSV file to be parsed")
  parser.add_argument('-campaign', help="Beam Test campaign")

  args = parser.parse_args()

  run_list = parseCSV(args.file)
  campaign = args.campaign
  psp_efficiencies, pss_efficiencies, stub_efficiencies, bias_voltages = [], [], [], []
  for run in run_list:
    run_number, bias = run["RunNumber"], run["Bias"]
    #Get result file
    result_file = TFile('/nfs/dust/cms/user/yotarid/Tracker/PSAnalysis/corryvreckan/output/run{}/analyze/analysis_psmodule.root'.format(run_number), 'READ')
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
    print(f'MPA Bias = {bias} ; PS-p efficiecy = {max_psp_efficiency}')
    print(f'SSA Bias = {bias} ; PS-s efficiecy = {max_pss_efficiency}')
    print(f'SSA Bias = {bias} ; Stub efficiecy = {max_stub_efficiency}')
    print(f'')

    bias_voltages.append(int(bias))
    psp_efficiencies.append(max_psp_efficiency * 100)
    pss_efficiencies.append(max_pss_efficiency * 100)
    stub_efficiencies.append(max_stub_efficiency * 100)

  psp_plot = plt.plot(bias_voltages, psp_efficiencies, linestyle='solid', linewidth=2, marker='o', color='darkred', label='PS-p')
  pss_plot = plt.plot(bias_voltages, pss_efficiencies, linestyle='solid', linewidth=2, marker='o', color='navy', label='PS-s')
  stub_plot = plt.plot(bias_voltages, stub_efficiencies, linestyle='solid', linewidth=2, marker='o', color='darkgreen', label='Stubs')
  plt.xlabel('Voltage (V)')
  plt.ylabel("Efficiency (%)")
  plt.legend(loc="center left")
  plt.grid()
  plt.savefig("./plots/BiasScan_Efficiency_"+campaign+".png")

if __name__ == "__main__":
  sys.exit(main())
