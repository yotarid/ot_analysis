from ROOT import TFile 
import csv, argparse, sys
import matplotlib.pyplot as plt
import numpy as np
import math
from matplotlib.ticker import ScalarFormatter
from scipy import optimize, special, integrate, signal
import matplotlib
matplotlib.use('Agg')

def parseCSV(file_path):
  print('Parsing CSV file : {}'.format(file_path))
  csv_file = open(file_path, mode='r') 
  return csv.DictReader(csv_file)

def gaus_func(t, theta, sigma):
  return (1/np.sqrt(2*np.pi * sigma**2)) * np.exp(-(t - theta)**2 / (2 * sigma**2))

def size_func(t, s0, alpha, theta0):
  return s0 + alpha * np.absolute(np.tan(t - theta0)) 

def integrand(t, s0, alpha, theta0, theta, sigma):
  return size_func(t, s0, alpha, theta0) * gaus_func(t, theta, sigma)

def integral(s0, alpha, theta0, theta, sigma):
  return integrate.quad(integrand, np.NINF, np.Inf, args=(s0, alpha, theta0, theta, sigma), limit=1000000)[0]

def fit_func(theta, s0, alpha, theta0, sigma):
  return [integral(s0, alpha, theta0, t, sigma) for t in theta]

#def gaus_func(x, p0):
#  return (1/np.sqrt(2*np.pi)) * np.exp(-0.5 * x**2 / p0**2)
#
#def size_func(x, p0, p1, p2):
#  return p0 + p1 * np.absolute(np.tan(x - p2) * np.pi/180) 
#
#def fit_func(x, s0, alpha, theta0, sigma):
#  return np.convolve(size_func(x, s0, alpha, theta0), gaus_func(x, sigma), mode='full')[0:len(x)]

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

  psp_params, psp_cov = optimize.curve_fit(fit_func, np.array(angle_list), np.array(psp_mean_cluster_size_list))  
  pss_params, pss_cov = optimize.curve_fit(fit_func, np.array(angle_list), np.array(pss_mean_cluster_size_list))  
  print(psp_params, pss_params)

  psp_plot = plt.plot(angle_list, psp_mean_cluster_size_list, linestyle='None', linewidth=2, marker='o', color='darkred', label='PS-p (threshold = 10 DAC)')  
  psp_fit_plot = plt.plot(np.linspace(-35, 35, 10000), np.array(fit_func(np.linspace(-35, 35, 10000), *psp_params))*100, linestyle='-', linewidth=2.5, color='darkred')

  pss_plot = plt.plot(angle_list, pss_mean_cluster_size_list, linestyle='None', linewidth=2, marker='o', color='navy', label='PS-s (threshold = 25 DAC)')  
  pss_fit_plot = plt.plot(np.linspace(-35, 35, 10000), np.array(fit_func(np.linspace(-35, 35, 10000), *pss_params))*100, linestyle='-', linewidth=2.5, color='navy')

  plt.xticks(np.arange(-40, 40, 10))
  plt.xlim([-40, 40])
  plt.xlabel("Angle (degrees)")
  plt.ylabel("Mean Cluster Size")
  plt.legend(loc="upper center")
  plt.grid()
  plt.savefig("./plots/AngularScan_ClusterSize_"+campaign+".pdf")

if __name__ == "__main__":
  sys.exit(main())

