from ROOT import TFile, TF1Convolution, TGraph, TF1, TCanvas
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
from matplotlib.lines import Line2D

def parseCSV(file_path):
  print('Parsing CSV file : {}'.format(file_path))
  csv_file = open(file_path, mode='r') 
  return csv.DictReader(csv_file)

def fit_func(x, p0, p1, p2, p3):
    return 1 - 1/2 * (p0 + p1*special.erf((x-p2)/p3))

def calculateError(eff, ntracks):
  return np.sqrt((eff * (1 - eff))/ntracks)

def calculatePt(angle):
  angle_rad = angle*np.pi/180
  return 0.57 * 0.2484475 / np.sin(angle_rad)
#return abs(angle)

def get_fit_dict(angles, cluster_size_list):
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
  graph = TGraph(len(angles), np.array(angles), np.array(cluster_size_list))
  graph.Fit(fit_func)
  param_s0 = fit_func.GetParameter(0)
  param_eta = fit_func.GetParameter(1)
  param_theta0 = fit_func.GetParameter(2)
  param_sigma = fit_func.GetParameter(3)
  xfit = np.linspace(-25, 25, 100000)
  yfit = [fit_func(x) for x in xfit]

  fit_dict = {
      "s0" : param_s0,
      "eta" : param_eta,
      "theta0" : param_theta0,
      "sigma" : param_sigma,
      "xfit" : xfit,
      "yfit" : yfit
  }
  #print(fit_dict)
  return fit_dict



def main():
  parser = argparse.ArgumentParser(description="bias scan")
  parser.add_argument('-csv', help="CSV file to be parsed")
  parser.add_argument('-folder', help="Results folder")
  parser.add_argument('-campaign', help="Beam Test campaign")

  args = parser.parse_args()

  run_list = parseCSV(args.csv)
  folder = args.folder
  campaign = args.campaign
  psp_efficiencies, pss_efficiencies, stub_efficiencies, stub_efficiencies_pos, stub_efficiencies_neg = [], [], [], [], []
  angles_pos, angles_neg, angles  =  [], [], []
  pt_momentum  =  []
  psp_efficiencies_err, pss_efficiencies_err, stub_efficiencies_err, stub_efficiencies_pos_err, stub_efficiencies_neg_err = [], [], [], [], [] 
  psp_mean_cluster_size_list, psp_mean_cluster_size_err_list, pss_mean_cluster_size_list, pss_mean_cluster_size_err_list= [], [], [], []
  psp_resolution_x_list, psp_resolution_err_x_list, psp_resolution_y_list = [], [], []
  pss_resolution_x_list, pss_resolution_err_x_list, pss_resolution_y_list = [], [], []

  #telescope resolution extracted from the resolution simulator
  tele_resolution = 9.15577

  for run in run_list:
    run_number, angle = run["RunNumber"], float(run["Angle"])
    angle = angle - 0.45
    print(f'Run Number : {run_number}, Angle : {angle}')
    #Get result file
    result_file = TFile(f'{folder}/output/run{run_number}/analyze/analysis_psmodule_test.root', 'READ')

    # #Get PS-s and PS-p total efficiency profile
    psp_efficiency_vs_tdc = result_file.AnalysisEfficiency.CMSPhase2_30.efficiencyVsTagTProfile_TDC
    pss_efficiency_vs_tdc = result_file.AnalysisEfficiency.CMSPhase2_31.efficiencyVsTagTProfile_TDC
    stub_efficiency_vs_tdc = result_file.AnalysisStubEfficiency.efficiencyVsTagTProfile_TDC

    psp_cluster_size_hist = result_file.AnalysisDUT.CMSPhase2_30.clusterSizeAssociated
    pss_cluster_size_hist = result_file.AnalysisDUT.CMSPhase2_31.clusterSizeAssociated

    psp_residuals_x_hist = result_file.AnalysisDUT.CMSPhase2_30.global_residuals.residualsX
    psp_residuals_y_hist = result_file.AnalysisDUT.CMSPhase2_30.global_residuals.residualsY
    pss_residuals_x_hist = result_file.AnalysisDUT.CMSPhase2_31.global_residuals.residualsX
    pss_residuals_y_hist = result_file.AnalysisDUT.CMSPhase2_31.global_residuals.residualsY

    psp_tdc_efficiencies, pss_tdc_efficiencies, stub_tdc_efficiencies = [], [], []
    psp_tdc_efficiencies_ntrack, pss_tdc_efficiencies_ntrack, stub_tdc_efficiencies_ntrack = [], [], [] 
    for tdc in range(0,9):
       psp_tdc_efficiencies.append(psp_efficiency_vs_tdc.GetBinContent(tdc))
       psp_tdc_efficiencies_ntrack.append(psp_efficiency_vs_tdc.GetBinEntries(tdc))

       pss_tdc_efficiencies.append(pss_efficiency_vs_tdc.GetBinContent(tdc))
       pss_tdc_efficiencies_ntrack.append(pss_efficiency_vs_tdc.GetBinEntries(tdc))

       stub_tdc_efficiencies.append(stub_efficiency_vs_tdc.GetBinContent(tdc))
       stub_tdc_efficiencies_ntrack.append(stub_efficiency_vs_tdc.GetBinEntries(tdc))

    #get PS residuals RMS
    psp_rms_residuals_x = psp_residuals_x_hist.GetRMS()
    psp_rms_residuals_y = psp_residuals_y_hist.GetRMS()
    pss_rms_residuals_x = pss_residuals_x_hist.GetRMS()
    pss_rms_residuals_y = pss_residuals_y_hist.GetRMS()

    #get PS residuals RMS
    psp_rms_err_residuals_x = psp_residuals_x_hist.GetRMSError()
    psp_rms_err_residuals_y = psp_residuals_y_hist.GetRMSError()
    pss_rms_err_residuals_x = pss_residuals_x_hist.GetRMSError()
    pss_rms_err_residuals_y = pss_residuals_y_hist.GetRMSError()

    #compute PS resolution 
    psp_resolution_x = np.sqrt(psp_rms_residuals_x**2 - tele_resolution**2)
    psp_resolution_y = np.sqrt(psp_rms_residuals_y**2 - tele_resolution**2)
    pss_resolution_x = np.sqrt(pss_rms_residuals_x**2 - tele_resolution**2)
    pss_resolution_y = np.sqrt(pss_rms_residuals_y**2 - tele_resolution**2)

    psp_resolution_x_list.append(psp_resolution_x)
    psp_resolution_err_x_list.append(psp_rms_err_residuals_x)
    psp_resolution_y_list.append(psp_resolution_y)
    pss_resolution_x_list.append(pss_resolution_x)
    pss_resolution_err_x_list.append(pss_rms_err_residuals_x)
    pss_resolution_y_list.append(pss_resolution_y)

    #Get cluster size
    psp_mean_cluster_size = psp_cluster_size_hist.GetMean()
    pss_mean_cluster_size = pss_cluster_size_hist.GetMean()
    psp_mean_cluster_size_err = psp_cluster_size_hist.GetMeanError()
    pss_mean_cluster_size_err = pss_cluster_size_hist.GetMeanError()

    psp_mean_cluster_size_list.append(psp_mean_cluster_size)
    pss_mean_cluster_size_list.append(pss_mean_cluster_size)
    psp_mean_cluster_size_err_list.append(psp_mean_cluster_size_err)
    pss_mean_cluster_size_err_list.append(pss_mean_cluster_size_err)

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
    print(f'Angle = {angle} ; Telescope resolution = {tele_resolution}')
    print(f'Angle = {angle} ; PS-p measured resolution = {psp_rms_residuals_x}')
    print(f'Angle = {angle} ; PS-s measured resolution = {pss_rms_residuals_x}')
    print(f'Angle = {angle} ; PS-p resolution = {psp_resolution_x} +/- {psp_rms_err_residuals_x}')
    print(f'Angle = {angle} ; PS-s resolution = {pss_resolution_x} +/- {pss_rms_err_residuals_x}')
    print(f'')

    angles.append(angle)
    psp_efficiencies.append(max_psp_efficiency)
    psp_efficiencies_err.append(calculateError(max_psp_efficiency, psp_ntrack))

    pss_efficiencies.append(max_pss_efficiency)
    pss_efficiencies_err.append(calculateError(max_pss_efficiency, pss_ntrack))

    stub_efficiencies.append(max_stub_efficiency)
    stub_efficiencies_err.append(calculateError(max_stub_efficiency, stub_ntrack))

    if angle >= 0 :
      pt_momentum.append(calculatePt(angle))
      angles_pos.append(angle)
      stub_efficiencies_pos.append(max_stub_efficiency)
      stub_efficiencies_pos_err.append(calculateError(max_stub_efficiency, stub_ntrack))
    else:
      angles_neg.append(angle)
      stub_efficiencies_neg.append(max_stub_efficiency)
      stub_efficiencies_neg_err.append(calculateError(max_stub_efficiency, stub_ntrack))


  #################################################################################
  ######################### Stub Effeciency Analysis ############################
  #################################################################################
  #params, cov = optimize.curve_fit(fit_func, np.array(angles), np.array(stub_efficiency), p0=[1, 1, 15, 1], maxfev=8000)
  params_pos, cov_pos = optimize.curve_fit(fit_func, np.array(angles_pos), np.array(stub_efficiencies_pos), maxfev=10000)
  params_neg, cov_neg = optimize.curve_fit(fit_func, np.array(angles_neg), np.array(stub_efficiencies_neg), maxfev=10000)
  print(params_pos, params_neg)
  

  fig1, ax1 = plt.subplots()
  plt.tight_layout()

  ax1.errorbar(angles, psp_efficiencies, yerr=psp_efficiencies_err, linestyle='-', linewidth=1, marker='o', markersize=5, capsize=3, color='darkred', label='PS-p')
  ax1.errorbar(angles, pss_efficiencies, yerr=pss_efficiencies_err, linestyle='-', linewidth=1, marker='o', markersize=5, capsize=3, color='navy', label='PS-s')
  ax1.errorbar(angles, stub_efficiencies, yerr=stub_efficiencies_err, linestyle='None', linewidth=1, marker='o', markersize=5, capsize=3, color='darkgreen', label='Stubs')
  ax1.errorbar(np.linspace(0, 26, 10000), np.array(fit_func(np.linspace(0, 26, 10000), *params_pos)), linestyle='--', linewidth=1, capsize=3, color='darkgreen', label='Stubs fit')
  ax1.errorbar(np.linspace(0, -26, 10000), np.array(fit_func(np.linspace(0, -26, 10000), *params_neg)), linestyle='--', linewidth=1, capsize=3, color='darkgreen')


  ax1.set_xlabel('Angle ($^{\circ}$)', fontsize=16)
  #ax1.set_xlim(-25,25)
  #ax1.xaxis.set_ticks(np.arange(-25, 25, 10))
  #ax1.xaxis.set_ticks(np.arange(-40, 41, 10))
  ax1.set_ylabel("Efficiency", fontsize=16)

  legend = ax1.legend(loc='upper left', ncol=1, fontsize=16, bbox_to_anchor=(1., 1.03))
  #legend = ax1.legend(loc='upper right', ncol=1, columnspacing=1.2, fontsize=16, bbox_to_anchor=(1.42, 1.03))

  ax1.grid(alpha=0.5)
  ax1.set_box_aspect(1)
  plt.savefig("./plots/angular_scan/angular_scan_efficiency_"+campaign+".pdf", bbox_inches="tight")

  #################################################################################
  ######################### pT Discrimination Analysis ############################
  #################################################################################
  params_pt, cov_pt = optimize.curve_fit(fit_func, np.array(pt_momentum), np.array(stub_efficiencies_pos), maxfev=10000)
  print(params_pos, params_neg, params_pt)

  fig2, ax2 = plt.subplots()
  plt.tight_layout()
  ax2.errorbar(pt_momentum, stub_efficiencies_pos, yerr=stub_efficiencies_pos_err, linestyle='None', marker='o', markersize=5, capsize=3, color='darkgreen', label='Stubs')
  ax2.errorbar(np.linspace(0, int(max(pt_momentum))+1, 10000), np.array(fit_func(np.linspace(0, int(max(pt_momentum))+1, 10000), *params_pt)), linestyle='--', linewidth=1, color='darkgreen', label='Stubs fit')
  ax2.set_xlabel('Transverse momentum (GeV)', fontsize=16)
  ax2.xaxis.set_ticks(np.arange(0, 6.1, 1))
  ax2.set_ylabel("Stub efficiency", fontsize=16)
  #ax.legend(loc="center left")
  legend = ax2.legend(loc='upper left', ncol=1, fontsize=16, bbox_to_anchor=(1., 1.03))
  ax2.grid(alpha=0.5)
  ax2.set_box_aspect(1)
  plt.savefig("./plots/angular_scan/angular_scan_pT_efficiency_"+campaign+".pdf", bbox_inches="tight")


  #################################################################################
  ######################### Cluster Size Analysis ############################
  #################################################################################
  psp_fit_dict = get_fit_dict(angles, psp_mean_cluster_size_list)
  psp_param_s0 = psp_fit_dict["s0"]
  psp_param_eta = psp_fit_dict["eta"]
  psp_param_theta0 = psp_fit_dict["theta0"]
  psp_param_sigma = psp_fit_dict["sigma"]
  psp_xfit = psp_fit_dict["xfit"]
  psp_yfit = psp_fit_dict["yfit"]

  pss_fit_dict = get_fit_dict(angles, pss_mean_cluster_size_list)
  pss_param_s0 = pss_fit_dict["s0"]
  pss_param_eta = pss_fit_dict["eta"]
  pss_param_theta0 = pss_fit_dict["theta0"]
  pss_param_sigma = pss_fit_dict["sigma"]
  pss_xfit = pss_fit_dict["xfit"]
  pss_yfit = pss_fit_dict["yfit"]

  fig3, ax3 = plt.subplots()
  plt.tight_layout()
  psp_plot = ax3.errorbar(angles, psp_mean_cluster_size_list, yerr=psp_mean_cluster_size_err_list, linestyle='None', linewidth=1, marker='o', markersize=5, capsize=3, color='darkred', label='PS-p')  
  psp_fit_plot = ax3.errorbar(psp_xfit, psp_yfit, linestyle='--', linewidth=1, color='darkred', label='PS-p fit')

  pss_plot = ax3.errorbar(angles, pss_mean_cluster_size_list, yerr=pss_mean_cluster_size_err_list, linestyle='None', linewidth=1, marker='o', markersize=5, capsize=3, color='navy', label='PS-s')  
  pss_fit_plot = ax3.errorbar(pss_xfit, pss_yfit, linestyle='--', linewidth=1, color='navy', label='PS-s fit')

  ax3.set_xlabel('Angle ($^{\circ}$)', fontsize=16)
  #ax3.xaxis.set_ticks(np.arange(-25, 25, 10))
  ax3.yaxis.set_ticks(np.arange(1, 2, 0.2))
  ax3.set_ylabel("Average cluster size", fontsize=16)
  #ax.legend(loc="center left")
  legend = ax3.legend(loc='upper left', ncol=1, fontsize=16, bbox_to_anchor=(1., 1.03))
  ax3.grid(alpha=0.5)
  ax3.set_box_aspect(1)
  plt.savefig("./plots/angular_scan/angular_scan_cluster_size_"+campaign+".pdf", bbox_inches="tight")

  #################################################################################
  ######################### Resolution Analysis ############################
  #################################################################################
  #Resolution
  fig4, ax4 = plt.subplots()
  plt.tight_layout()
  psp_resolution_plot = ax4.errorbar(angles, psp_resolution_x_list, yerr=psp_resolution_err_x_list, linestyle='-', linewidth=1, marker='o', markersize=5, capsize=3, color='darkred', label='PS-p')
  pss_resolution_plot = ax4.errorbar(angles, pss_resolution_x_list, yerr=pss_resolution_err_x_list, linestyle='-', linewidth=1, marker='o', markersize=5, capsize=3, color='navy', label='PS-s')
  ax4.set_xlabel('Angle ($^{\circ}$)', fontsize=16)
  ax4.set_ylabel("Resolution ($\mathrm{\mu m}$)", fontsize=16)
  legend = ax4.legend(loc='upper left', ncol=1, fontsize=16, bbox_to_anchor=(1., 1.03))
  ax4.grid(alpha=0.5)
  ax4.set_box_aspect(1)
  plt.savefig("./plots/angular_scan/angular_scan_resolution_"+campaign+".pdf", bbox_inches="tight")

if __name__ == "__main__":
  sys.exit(main())
