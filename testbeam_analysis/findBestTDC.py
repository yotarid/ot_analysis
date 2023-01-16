from ROOT import TFile 
import csv, argparse, sys
import matplotlib.pyplot as plt
import numpy as np
import math
import matplotlib.ticker as ticker
from matplotlib.ticker import ScalarFormatter
from scipy import optimize, special
import matplotlib
matplotlib.use('Agg')
import statistics as stat

def parseCSV(file_path):
  print('Parsing CSV file : {}'.format(file_path))
  csv_file = open(file_path, mode='r') 
  return csv.DictReader(csv_file)

def main():
  parser = argparse.ArgumentParser(description="best TDC finder")
  parser.add_argument('-file', help="CSV file to be parsed")
  parser.add_argument('-campaign', help="Beam Test campaign")

  args = parser.parse_args()

  run_list = parseCSV(args.file)
  campaign = args.campaign

  run_number_list, best_tdc_list = [], []
  for run in run_list:
    run_number = run["RunNumber"]
    print(f'Run Number : {run_number}')
    #Get result file
    result_file = TFile(f'/nfs/dust/cms/user/yotarid/Tracker/PSAnalysis/corryvreckan/output/run{run_number}/analyze/analysis_psmodule.root', 'READ')

    # #Get PS-s and PS-p total efficiency profile
    psp_efficiency_vs_tdc = result_file.AnalysisEfficiency.CMSPhase2_30.efficiencyVsTagTProfile_TDC
    pss_efficiency_vs_tdc = result_file.AnalysisEfficiency.CMSPhase2_31.efficiencyVsTagTProfile_TDC
    stub_efficiency_vs_tdc = result_file.AnalysisStubEfficiency.efficiencyVsTagTProfile_TDC

    best_mean_efficiency, best_tdc = -1, -1
    for tdc in range(0,9):
       psp_efficiency = psp_efficiency_vs_tdc.GetBinContent(tdc)
       pss_efficiency = pss_efficiency_vs_tdc.GetBinContent(tdc)
       stub_efficiency = stub_efficiency_vs_tdc.GetBinContent(tdc)

       mean_efficiency = stat.mean([psp_efficiency, pss_efficiency, stub_efficiency])
       if mean_efficiency >= best_mean_efficiency:
         best_mean_efficiency = mean_efficiency
         best_tdc = tdc - 1
    run_number_list.append(run_number)
    best_tdc_list.append(best_tdc)

    print(f'Run Number = {run_number} ; Best TDC = {best_tdc}')
    print(f'')

  best_tdc_plot = plt.plot(run_number_list, best_tdc_list, linestyle='None', marker='d', color='darkred', label="Best TDC")
  #plt.xlim([5214, 5331])
  plt.ylim([-0.5, 8])
  plt.xlabel("Run Number")
  plt.ylabel("Best TDC")
  plt.grid()
  plt.xticks(rotation=90, fontsize=5)

  plt.savefig("./plots/BestTDC_"+campaign+".pdf")

if __name__ == "__main__":
  sys.exit(main())
