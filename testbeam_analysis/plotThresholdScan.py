import ROOT
from ROOT import TFile 
import csv, argparse, sys
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import ScalarFormatter


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

  
  unit = "(e-)"
  ThDACtoEl_ssa, ThDACtoEl_mpa = 1, 1
  pss_baseline, psp_baseline = 4798.72, 4284.26
  #pss_baseline, psp_baseline = 0, 0
  if args.ThDAC :
    unit = "(Th_DAC)"
    ThDACtoEl_ssa, ThDACtoEl_mpa = 250, 94
    pss_baseline, psp_baseline = pss_baseline/ThDACtoEl_ssa, psp_baseline/ThDACtoEl_mpa
  run_list = parseCSV(args.file)
  campaign = args.campaign
  psp_efficiency, pss_efficiency, stub_efficiency, psp_threshold, pss_threshold = [], [], [], [], []
  for run in run_list:
    run_number, th = run["RunNumber"], run["Threshold"]
    #Get result file
    hit_result_file = TFile('/nfs/dust/cms/user/yotarid/Tracker/PSAnalysis/corryvreckan/output/analyze/run{}/analysis_psmodule_hits.root'.format(run_number), 'READ')
    #stub_result_file = TFile('/nfs/dust/cms/user/yotarid/Tracker/PSAnalysis/corryvreckan/output/analyze/run{}/analysis_psmodule_stubs.root'.format(run_number), 'READ')
    # #Get PS-s and PS-p total efficiency profile
    psp_total_efficiency = hit_result_file.AnalysisEfficiency.CMSPhase2_30.eTotalEfficiency_inPixelROI
    pss_total_efficiency = hit_result_file.AnalysisEfficiency.CMSPhase2_31.eTotalEfficiency_inPixelROI
    #stub_total_efficiency = stub_result_file.AnalysisStubEfficiency.eTotalEfficiency
    #Get PS-s and PS-p total efficiency
    psp_threshold.append((float(th) - psp_baseline)/ThDACtoEl_mpa)
    psp_efficiency.append(psp_total_efficiency.GetEfficiency(1) * 100)
    pss_threshold.append((float(th) - pss_baseline)/ThDACtoEl_ssa)
    pss_efficiency.append(pss_total_efficiency.GetEfficiency(1) * 100)
    #stub_efficiency.append(stub_total_efficiency.GetEfficiency(1) * 100)

  psp_plot = plt.plot(psp_threshold, psp_efficiency, linestyle='solid', linewidth=2, marker='o', color='darkred', label='PS-p')
  pss_plot = plt.plot(pss_threshold, pss_efficiency, linestyle='solid', linewidth=2, marker='o', color='navy', label='PS-s')
  #stub_plot = plt.plot(psp_threshold, stub_efficiency, linestyle='solid', linewidth=2, marker='o', color='darkgreen', label='Stubs')
  #plt.title("DESY26_2 Threshold scan @Bias(300V)")
  plt.title("Threshold scan at 300V bias voltage")
  plt.xlabel('Threshold {}'.format(unit))
  #plt.ylim((0, 105))
  plt.ylabel("Efficiency (%)")
  plt.legend(loc="upper right")
  plt.grid()
  # plt.show()
  plt.savefig("./plots/ThresholdScan_"+campaign+"_Efficiency_DESY26_2.png")




if __name__ == "__main__":
  sys.exit(main())
