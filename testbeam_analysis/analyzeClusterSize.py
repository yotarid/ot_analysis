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

def main():
  parser = argparse.ArgumentParser(description="angular scan")
  parser.add_argument('-file', help="CSV file to be parsed")
  parser.add_argument('-campaign', help="Beam Test campaign")

  args = parser.parse_args()

  run_list = parseCSV(args.file)
  campaign = args.campaign

  psp_mean_cluster_size_list, pss_mean_cluster_size_list, angle_list = [], [], []

  for run in run_list:
    run_number, angle = run["RunNumber"], float(run["Angle"])
    print(f'Run Number : {run_number}, Angle : {angle}')
    #Get result file
    result_file = TFile(f'/nfs/dust/cms/user/yotarid/Tracker/PSAnalysis/corryvreckan/output/run{run_number}/analyze/analysis_psmodule.root', 'READ')

    psp_cluster_size_hist = result_file.AnalysisDUT.CMSPhase2_30.clusterSizeAssociated
    pss_cluster_size_hist = result_file.AnalysisDUT.CMSPhase2_31.clusterSizeAssociated

    psp_mean_cluster_size = psp_cluster_size_hist.GetMean()
    pss_mean_cluster_size = pss_cluster_size_hist.GetMean()

    angle_list.append(angle)
    psp_mean_cluster_size_list.append(psp_mean_cluster_size)
    pss_mean_cluster_size_list.append(pss_mean_cluster_size)

  psp_plot = plt.plot(angle_list, psp_mean_cluster_size_list, linestyle='None', marker='o', color='darkred', label='PS-p')  
  pss_plot = plt.plot(angle_list, pss_mean_cluster_size_list, linestyle='None', marker='o', color='navy', label='PS-s')  

  plt.xticks(np.arange(-40, 40, 5))
  plt.xlim([-40, 40])
  plt.xlabel("Angle (degrees)")
  plt.ylabel("Mean Cluster Size")
  plt.legend(loc="upper center")
  plt.grid()
  plt.savefig("./plots/AngularScan_ClusterSize_"+campaign+".png")

if __name__ == "__main__":
  sys.exit(main())

