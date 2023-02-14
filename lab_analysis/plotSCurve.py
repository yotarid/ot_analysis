from ROOT import *
import ROOT
import csv, argparse, sys
import matplotlib.pyplot as plt
import numpy as np
import math
from matplotlib.ticker import ScalarFormatter
from scipy import optimize, special
import matplotlib
matplotlib.use('Agg')

NHYBRID = 2
NCHIP = 8
NSSACH = 120
NMPACH = 920

def parseCSV(file_path):
  print('Parsing CSV file : {}'.format(file_path))
  csv_file = open(file_path, mode='r') 
  return csv.DictReader(csv_file)

def fit_func(x, mu, sigma):
  return 0.5 * special.erfc((x - mu) / (sqrt(2.) * sigma))

def main():
  parser = argparse.ArgumentParser(description="SCurve")
  parser.add_argument('-file', help="CSV file to be parsed")

  args = parser.parse_args()
  noise_files = parseCSV(args.file)

  f_ssa, f_mpa = TFile(), TFile()
  h_ssa, h_mpa = TH2F(), TH2F()
  board_id, optical_group_id, hybrid_id, ssa_id, mpa_id = 0, 0, 0, 0, 8
  for line in noise_files:
    chip, folder = line["chip"], line["folder"]
    if chip == "ssa":
      f_ssa = TFile.Open(f'results/{folder}/Hybrid.root', 'READ')
      h_ssa = f_ssa.Get(f'Detector/Board_{board_id}/OpticalGroup_{optical_group_id}/Hybrid_{hybrid_id}/SSA_{ssa_id}/D_B({board_id})_O({optical_group_id})_H({hybrid_id})_SCurve_Chip({ssa_id})')
    else:
      f_mpa = TFile.Open(f'results/{folder}/Hybrid.root', 'READ')
      h_mpa = f_mpa.Get(f'Detector/Board_{board_id}/OpticalGroup_{optical_group_id}/Hybrid_{hybrid_id}/MPA_{mpa_id}/D_B({board_id})_O({optical_group_id})_H({hybrid_id})_SCurve_Chip({mpa_id})')

  #for ssa
  plt.figure(1)
  for ch_id in range(1, h_ssa.GetNbinsX()):
  #for ch_id in range(100, 101):
    x_ssa, y_ssa = [], []
    for th in range(1, h_ssa.GetNbinsY()):
      if th < 55: continue
      x_ssa.append(th) 
      y_ssa.append(h_ssa.GetBinContent(ch_id, th))
    fit_param, cov = optimize.curve_fit(fit_func, np.array(x_ssa), np.array(y_ssa), p0=[77, 6], maxfev=10000)
    fit_plot = plt.plot(np.linspace(min(x_ssa), max(x_ssa), 10000), [fit_func(x, *fit_param)*100 for x in np.linspace(min(x_ssa), max(x_ssa), 10000)], linestyle='-', linewidth=1)
    plt.plot(x_ssa, np.array(y_ssa)*100, linestyle='None', marker='o', markersize=1)

  plt.xlim(50,110)
  plt.ylim(0,105)
  plt.xlabel('Threshold (ThDAC)', fontsize=12)
  plt.ylabel('Efficiency (%)', fontsize=12)
  plt.grid()
  plt.savefig("./plots/scurve_ssa.pdf", bbox_inches="tight")

  #for mpa
  plt.figure(2)
  for ch_id in range(1, h_mpa.GetNbinsX()):
  #for ch_id in range(1, 2):
    x_mpa, y_mpa = [], []
    for th in range(1, h_mpa.GetNbinsY()):
      if th < 160: continue
      x_mpa.append(th) 
      y_mpa.append(h_mpa.GetBinContent(ch_id, th))
    fit_param, cov = optimize.curve_fit(fit_func, np.array(x_mpa), np.array(y_mpa), p0=[200, 3], maxfev=10000)
    #fit_plot = plt.plot(np.linspace(min(x_mpa), max(x_mpa), 10000), [fit_func(x, *fit_param) for x in np.linspace(min(x_mpa), max(x_mpa), 10000)], linestyle='-', linewidth=1, color='navy')
    fit_plot = plt.plot(np.linspace(min(x_mpa), max(x_mpa), 10000), [fit_func(x, *fit_param)*100 for x in np.linspace(min(x_mpa), max(x_mpa), 10000)], linestyle='-', linewidth=1)
    #plt.plot(x_mpa, y_mpa, linestyle='None', marker='o', markersize=1, color='navy')
    plt.plot(x_mpa, np.array(y_mpa)*100, linestyle='None', marker='o', markersize=1)

  plt.xlim(175,240)
  plt.ylim(0,105)
  plt.xlabel('Threshold (ThDAC)', fontsize=12)
  plt.ylabel('Efficiency (%)', fontsize=12)
  plt.grid()
  plt.savefig("./plots/scurve_mpa.pdf", bbox_inches="tight")

       
if __name__ == "__main__":
  sys.exit(main())

