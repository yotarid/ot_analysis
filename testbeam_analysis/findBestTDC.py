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
  parser.add_argument('-csv', help="CSV file to be parsed")
  parser.add_argument('-folder', help="result folder")
  parser.add_argument('-campaign', help="Beam Test campaign")

  args = parser.parse_args()

  csv_file = parseCSV(args.csv)
  folder = args.folder
  campaign = args.campaign

  tdc_dict = []

  run_number_list = []
  for run in csv_file:
    run_number = run["RunNumber"]
    print(f'Run Number : {run_number}')
    #Get result file
    result_file = TFile(f'{folder}/output/run{run_number}/analyze/analysis_psmodule.root', 'READ')

    # #Get PS-s and PS-p total efficiency profile
    psp_efficiency_vs_tdc = result_file.AnalysisEfficiency.CMSPhase2_30.efficiencyVsTagTProfile_TDC
    pss_efficiency_vs_tdc = result_file.AnalysisEfficiency.CMSPhase2_31.efficiencyVsTagTProfile_TDC
    stub_efficiency_vs_tdc = result_file.AnalysisStubEfficiency.efficiencyVsTagTProfile_TDC

    tdc_list, best_tdc_list, psp_eff_list, pss_eff_list, stub_eff_list = [], [], [], [], []
    for tdc in range(0,9):
       psp_eff_list.append(psp_efficiency_vs_tdc.GetBinContent(tdc))
       pss_eff_list.append(pss_efficiency_vs_tdc.GetBinContent(tdc))
       stub_eff_list.append(stub_efficiency_vs_tdc.GetBinContent(tdc))
       tdc_list.append(tdc - 1)

    psp_eff_max = max(psp_eff_list)
    pss_eff_max = max(pss_eff_list)
    stub_eff_max = max(stub_eff_list)

    best_psp_tdc = tdc_list[psp_eff_list.index(psp_eff_max)]
    best_pss_tdc = tdc_list[pss_eff_list.index(pss_eff_max)]
    best_stub_tdc = tdc_list[stub_eff_list.index(stub_eff_max)]
    for idx, tdc in enumerate(tdc_list):
      if (psp_eff_max - psp_eff_list[idx]) <= 0.05 and (pss_eff_max - pss_eff_list[idx]) <= 0.05:
        best_tdc_list.append(tdc)
    
    tdc_dict.append({'run_number': run_number, 'max_psp_eff_tdc': best_psp_tdc, 'max_pss_eff_tdc': best_pss_tdc, 'max_stub_eff_tdc': best_stub_tdc, 'best_tdc_list': best_tdc_list})

    print(f'Run Number = {run_number} ; max_psp_tdc = {best_psp_tdc} ; max_pss_tdc = {best_pss_tdc} ; max_stub_tdc = {best_stub_tdc}; best_tdc_list  = {best_tdc_list}')
    print(f'')

  fields = ['run_number', 'max_psp_eff_tdc', 'max_pss_eff_tdc', 'max_stub_eff_tdc', 'best_tdc_list'] 

  with open('best_tdc.csv', 'w', newline='') as file: 
    writer = csv.DictWriter(file, fieldnames = fields)

    writer.writeheader() 

    writer.writerows(tdc_dict)

  #best_tdc_plot = plt.plot(run_number_list, best_tdc_list, linestyle='None', marker='d', color='darkred', label="Best TDC")
  ##plt.xlim([5214, 5331])
  #plt.ylim([-0.5, 8])
  #plt.xlabel("Run Number")
  #plt.ylabel("Best TDC")
  #plt.grid()
  #plt.xticks(rotation=90, fontsize=5)

  #plt.savefig("./plots/BestTDC_"+campaign+".pdf")

if __name__ == "__main__":
  sys.exit(main())
