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

def parseCSV(file_path):
  print('Parsing CSV file : {}'.format(file_path))
  csv_file = open(file_path, mode='r') 
  return csv.DictReader(csv_file)

def fit_func(x, mu, sigma):
  #return 0.5 * special.erfc((x - mu) / sigma)
  return 0.5 * special.erfc((x - mu) / (sqrt(2.) * sigma))

def main():
  parser = argparse.ArgumentParser(description="Noise")
  parser.add_argument('-file', help="CSV file to be parsed")

  args = parser.parse_args()
  noise_files = parseCSV(args.file)

  f_ssa, f_mpa = TFile(), TFile()
  h_scurve_ssa, h_scurve_mpa = TH2F(), TH2F()
  board_id, optical_group_id = 0,0

  ssa_noise_array = {"pre-assembly":[], "pre-encapsulation":[], "post-encapsulation":[]}
  mpa_noise_array = {"pre-assembly":[], "pre-encapsulation":[], "post-encapsulation":[]}

  for line in noise_files:
    stage, folder = line["stage"], line["folder"]
    f_noise = TFile.Open(f'results/{folder}/Hybrid.root', 'READ')
    if stage == "pre-encapsulation" or stage == "post-encapsulation":
      optical_group_id = 1
    for hybrid_local_id in range(0, 2):
      hybrid_id = 2*optical_group_id + hybrid_local_id
      for chip_id in range(0, 8):
        ssa_id, mpa_id = chip_id, chip_id + 8

        #for ssa
        h_scurve_ssa = f_noise.Get(f'Detector/Board_{board_id}/OpticalGroup_{optical_group_id}/Hybrid_{hybrid_id}/SSA_{ssa_id}/D_B({board_id})_O({optical_group_id})_H({hybrid_id})_SCurve_Chip({ssa_id})')
        if h_scurve_ssa == None:
          continue
        for ch_id in range(1, h_scurve_ssa.GetNbinsX()):
          x_array, y_array = [], []
          for th in range(1, h_scurve_ssa.GetNbinsY()):
            x_array.append(th) 
            y_array.append(h_scurve_ssa.GetBinContent(ch_id, th))
          fit_param, cov = optimize.curve_fit(fit_func, np.array(x_array), np.array(y_array), p0=[77, 6], maxfev=10000)
          ssa_noise_array[stage].append(fit_param[1])

        #for mpa
        if stage == "pre-assembly":
          mpa_id = chip_id + chip_id*hybrid_local_id + 1
          noise_file = parseCSV(f'results/OT_ModuleTest_Dobby_MaPSA/mpa_test_35494_002_PSP_MAINL_chip{mpa_id}.csv')
          for line in noise_file:
            ch, noise = int(line["channel"]), float(line["noise"])
            mpa_noise_array[stage].append(noise/sqrt(2))
        else:  
          h_scurve_mpa = f_noise.Get(f'Detector/Board_{board_id}/OpticalGroup_{optical_group_id}/Hybrid_{hybrid_id}/MPA_{mpa_id}/D_B({board_id})_O({optical_group_id})_H({hybrid_id})_SCurve_Chip({mpa_id})')
          if h_scurve_mpa == None:
            continue
          for ch_id in range(1, h_scurve_mpa.GetNbinsX()):
            x_array, y_array = [], []
            for th in range(1, h_scurve_mpa.GetNbinsY()):
              x_array.append(th) 
              y_array.append(h_scurve_mpa.GetBinContent(ch_id, th))
            fit_param, cov = optimize.curve_fit(fit_func, np.array(x_array), np.array(y_array), p0=[200, 3], maxfev=10000)
            mpa_noise_array[stage].append(fit_param[1])
  
  ssa_thdac, mpa_thdac = 250, 94

  #ssa
  fig1, ax11 = plt.subplots()
  ax12 = ax11.twiny()
  ax12.set_xlabel(r"Channel Noise ($e^{-}$)")
  ax12.set_xlim(0,8*ssa_thdac)

  ax11.hist(ssa_noise_array["pre-assembly"], bins=40, range=(0,10), histtype='step', color='darkgrey', linewidth=2, label='skeleton', zorder=3)
  ax11.hist(ssa_noise_array["pre-encapsulation"], bins=40, range=(0,10), histtype='step', color='steelblue', linewidth=2, label='pre-encapsulation', zorder=3)
  ax11.hist(ssa_noise_array["post-encapsulation"], bins=40, range=(0,10), histtype='step', color='navy', linewidth=2, label='post-encapsulation', zorder=3)
  ax11.set_xlabel('Channel Noise (ThDAC)', fontsize=12)
  ax11.set_ylabel('Entries', fontsize=12)
  ax11.grid(zorder=0, alpha=0.5)
  ax11.set_xlim(0,8)
  ax11.legend(loc='upper right', fontsize=12)
  #plt.savefig("./plots/noise_ssa.pdf", bbox_inches="tight")
  plt.savefig("./plots/noise_ssa.pdf")

  plt.figure(2)
  #mpa
  fig2, ax21 = plt.subplots()
  ax22 = ax21.twiny()
  ax22.set_xlabel(r"Channel Noise ($e^{-}$)")
  ax22.set_xlim(0,5*mpa_thdac)


  ax21.hist(mpa_noise_array["pre-assembly"], bins=40, range=(0,10), histtype='step', color='darkgrey', linewidth=2, label='MaPSA', zorder=3)
  ax21.hist(mpa_noise_array["pre-encapsulation"], bins=40, range=(0,10), histtype='step', color='steelblue', linewidth=2, label='pre-encapsulation', zorder=3)
  ax21.hist(mpa_noise_array["post-encapsulation"], bins=40, range=(0,10), histtype='step', color='navy', linewidth=2, label='post-encapsulation', zorder=3)
  ax21.set_xlabel('Channel Noise (ThDAC)', fontsize=12)
  ax21.set_ylabel('Entries', fontsize=12)
  ax21.grid(zorder=0, alpha=0.5)
  ax21.set_xlim(0,5)
  ax21.legend(loc='upper right', fontsize=12)
  #plt.savefig("./plots/noise_mpa.pdf", bbox_inches="tight")
  plt.savefig("./plots/noise_mpa.pdf")
       
if __name__ == "__main__":
  sys.exit(main())



