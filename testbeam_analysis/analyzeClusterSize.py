from ROOT import TFile, TF1Convolution, TGraph, TF1, TCanvas
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

def get_fit_dict(angle_list, cluster_size_list):
  xMin = -60.
  xMax = 60.
  convGaus = TF1("convGaus","1./TMath::Sqrt(2.*TMath::Pi())/[0]*exp(-0.5*x*x/([0]*[0]))", xMin, xMax)
  clustersizeOpt = TF1("clustersizeOpt","[0]+[1]/0.09*abs(tan((x-[2])*TMath::Pi()/180.))",xMin,xMax)
  clustersizeFuncConv = TF1Convolution(clustersizeOpt, convGaus, xMin, xMax, True)

  fit_func = TF1("fit_func", clustersizeFuncConv, xMin,xMax, clustersizeFuncConv.GetNpar())
  fit_func.SetParameter(0,1.)
  fit_func.SetParameter(1,0.28)
  fit_func.SetParameter(2,0.)
  fit_func.SetParameter(3,4.)
  graph = TGraph(len(angle_list), np.array(angle_list), np.array(cluster_size_list))
  graph.Fit(fit_func)
  param_s0 = fit_func.GetParameter(0)
  param_eta = fit_func.GetParameter(1)
  param_theta0 = fit_func.GetParameter(2)
  param_sigma = fit_func.GetParameter(3)
  xfit = np.linspace(-35, 35, 100000)
  yfit = [fit_func(x) for x in np.linspace(-35, 35, 100000)]

  fit_dict = {
      "s0" : param_s0,
      "eta" : param_eta,
      "theta0" : param_theta0,
      "sigma" : param_sigma,
      "xfit" : xfit,
      "yfit" : yfit
  }
  return fit_dict

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

  psp_fit_dict = get_fit_dict(angle_list, psp_mean_cluster_size_list)
  psp_param_s0 = psp_fit_dict["s0"]
  psp_param_eta = psp_fit_dict["eta"]
  psp_param_theta0 = psp_fit_dict["theta0"]
  psp_param_sigma = psp_fit_dict["sigma"]
  psp_xfit = psp_fit_dict["xfit"]
  psp_yfit = psp_fit_dict["yfit"]

  pss_fit_dict = get_fit_dict(angle_list, pss_mean_cluster_size_list)
  pss_param_s0 = pss_fit_dict["s0"]
  pss_param_eta = pss_fit_dict["eta"]
  pss_param_theta0 = pss_fit_dict["theta0"]
  pss_param_sigma = pss_fit_dict["sigma"]
  pss_xfit = pss_fit_dict["xfit"]
  pss_yfit = pss_fit_dict["yfit"]

  psp_plot = plt.plot(angle_list, psp_mean_cluster_size_list, linestyle='None', linewidth=2, marker='o', color='darkred', label='PS-p (threshold = 10 DAC)')  
  psp_fit_plot = plt.plot(psp_xfit, psp_yfit, linestyle='-', linewidth=2.5, color='darkred')

  pss_plot = plt.plot(angle_list, pss_mean_cluster_size_list, linestyle='None', linewidth=2, marker='o', color='navy', label='PS-s (threshold = 25 DAC)')  
  pss_fit_plot = plt.plot(pss_xfit, pss_yfit, linestyle='-', linewidth=2.5, color='navy')

  plt.xticks(np.arange(-40, 40, 10))
  plt.xlim([-40, 40])
  plt.xlabel("Angle (degrees)")
  plt.ylabel("Mean Cluster Size")
  plt.legend(loc="upper center")
  plt.grid()
  plt.savefig("./plots/AngularScan_ClusterSize_"+campaign+".pdf")

if __name__ == "__main__":
  sys.exit(main())

