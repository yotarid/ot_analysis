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

  csv_file = parseCSV(args.csv)
  folder = args.folder
  campaign = args.campaign

  psp_efficiencies, pss_efficiencies, stub_efficiencies, mpa_thresholds, ssa_thresholds = [], [], [], [], []
  psp_efficiencies_err, pss_efficiencies_err, stub_efficiencies_err = [], [], [] 
  psp_mean_cluster_size_list, pss_mean_cluster_size_list = [], []
  psp_resolution_x_list, psp_resolution_y_list = [], []
  pss_resolution_x_list, pss_resolution_y_list = [], []

  #telescope resolution extracted from the resolution simulator
  tele_resolution = 3.54142

  psp_limit = False

  for line in csv_file:
    run_number, th_MPA, th_SSA = line["RunNumber"], int(line["Threshold_MPA"]), int(line["Threshold_SSA"])
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

    #compute PS resolution 
    psp_resolution_x = np.sqrt(psp_rms_residuals_x**2 - tele_resolution**2)
    psp_resolution_y = np.sqrt(psp_rms_residuals_y**2 - tele_resolution**2)
    pss_resolution_x = np.sqrt(pss_rms_residuals_x**2 - tele_resolution**2)
    pss_resolution_y = np.sqrt(pss_rms_residuals_y**2 - tele_resolution**2)

    #get cluster size
    psp_mean_cluster_size = psp_cluster_size_hist.GetMean()
    pss_mean_cluster_size = pss_cluster_size_hist.GetMean()

    #Get PS-s, PS-p and Stub  efficiencies
    max_psp_efficiency = max(psp_tdc_efficiencies)
    psp_ntrack = psp_tdc_efficiencies_ntrack[psp_tdc_efficiencies.index(max_psp_efficiency)]

    max_pss_efficiency = max(pss_tdc_efficiencies)
    pss_ntrack = pss_tdc_efficiencies_ntrack[pss_tdc_efficiencies.index(max_pss_efficiency)]

    max_stub_efficiency = max(stub_tdc_efficiencies)
    stub_ntrack = stub_tdc_efficiencies_ntrack[stub_tdc_efficiencies.index(max_stub_efficiency)]
 
    print(f'MPA Threshold = {th_MPA} ; PS-p efficiecy = {max_psp_efficiency}')
    print(f'SSA Threshold = {th_SSA} ; PS-s efficiecy = {max_pss_efficiency}')
    print(f'SSA Threshold = {th_SSA} ; Stub efficiecy = {max_stub_efficiency}')
    print(f'')

    ssa_thresholds.append(th_SSA)
    pss_efficiencies.append(max_pss_efficiency)
    pss_efficiencies_err.append(calculateError(max_pss_efficiency, pss_ntrack))
    pss_mean_cluster_size_list.append(pss_mean_cluster_size)
    pss_resolution_x_list.append(pss_resolution_x)
    pss_resolution_y_list.append(pss_resolution_y)

    if psp_limit == False:
      mpa_thresholds.append(th_MPA)
      psp_efficiencies.append(max_psp_efficiency)
      psp_efficiencies_err.append(calculateError(max_psp_efficiency, psp_ntrack))
      psp_mean_cluster_size_list.append(psp_mean_cluster_size)
      psp_resolution_x_list.append(psp_resolution_x)
      psp_resolution_y_list.append(psp_resolution_y)

    if th_MPA == 250:
      psp_limit = True

    stub_efficiencies.append(max_stub_efficiency)
    stub_efficiencies_err.append(calculateError(max_stub_efficiency, stub_ntrack))

  #Efficiency
  fig1, ax1 = plt.subplots()
  plt.tight_layout()
  psp_plot = ax1.errorbar(mpa_thresholds, psp_efficiencies, yerr=psp_efficiencies_err, linestyle='solid', linewidth=1, marker='o', markersize=5, capsize=3, color='darkred', label='PS-p')
  pss_plot = ax1.errorbar(ssa_thresholds, pss_efficiencies, yerr=pss_efficiencies_err, linestyle='solid', linewidth=1, marker='o', markersize=5, capsize=3, color='navy', label='PS-s')
  stub_plot = ax1.errorbar(ssa_thresholds, stub_efficiencies, yerr=stub_efficiencies_err, linestyle='solid', linewidth=1, marker='o', markersize=5, capsize=3, color='darkgreen', label='Stubs')
  ax1.set_xlabel('Threshold (ThDAC)', fontsize=16)
  ax1.set_ylabel("Efficiency", fontsize=16)
  legend = ax1.legend(loc='upper left', ncol=1, fontsize=16, bbox_to_anchor=(1., 1.03))
  ax1.grid(alpha=0.5)
  ax1.set_box_aspect(1)
  plt.savefig("./plots/threshold_scan/threshold_scan_efficiency_"+campaign+".pdf", bbox_inches="tight")

  #Cluster size
  fig2, ax2 = plt.subplots()
  plt.tight_layout()
  psp_cluster_size_plot = ax2.errorbar(mpa_thresholds, psp_mean_cluster_size_list, linestyle='-', linewidth=1, marker='o', color='darkred', label='PS-p')
  pss_cluster_size_plot = ax2.errorbar(ssa_thresholds, pss_mean_cluster_size_list, linestyle='-', linewidth=1, marker='o', color='navy', label='PS-s')
  ax2.set_xlabel('Threshold (ThDAC)', fontsize=16)
  ax2.set_ylabel("Average cluster size", fontsize=16)
  legend = ax2.legend(loc='upper left', ncol=1, fontsize=16, bbox_to_anchor=(1., 1.03))
  ax2.grid(alpha=0.5)
  ax2.set_box_aspect(1)
  plt.savefig("./plots/threshold_scan/threshold_scan_cluster_size_"+campaign+".pdf", bbox_inches="tight")

  #Resolution
  fig3, ax3 = plt.subplots()
  plt.tight_layout()
  psp_resolution_plot = ax3.errorbar(mpa_thresholds, psp_resolution_x_list, linestyle='-', linewidth=1, marker='o', color='darkred', label='PS-p')
  pss_resolution_plot = ax3.errorbar(ssa_thresholds, pss_resolution_x_list, linestyle='-', linewidth=1, marker='o', color='navy', label='PS-s')
  ax3.set_xlabel('Threshold (ThDAC)', fontsize=16)
  ax3.set_ylabel("Resolution ($\mathrm{\mu m}$)", fontsize=16)
  legend = ax3.legend(loc='upper left', ncol=1, fontsize=16, bbox_to_anchor=(1., 1.03))
  ax3.grid(alpha=0.5)
  ax3.set_box_aspect(1)
  plt.savefig("./plots/threshold_scan/threshold_scan_resolution_"+campaign+".pdf", bbox_inches="tight")





if __name__ == "__main__":
  sys.exit(main())
