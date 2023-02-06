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

def main():
  parser = argparse.ArgumentParser(description="Pedestal Equalization")
  parser.add_argument('-file', help="CSV file to be parsed")

  args = parser.parse_args()
  pede_files = parseCSV(args.file)

  f_ssa_pre_trim, f_ssa_post_trim, f_mpa_pre_trim, f_mpa_post_trim = TFile(), TFile(), TFile(), TFile()
  h_ssa_pre_trim, h_ssa_post_trim, h_mpa_pre_trim, h_mpa_post_trim = TH1F(), TH1F(), TH1F(), TH1F()
  board_id, optical_group_id, hybrid_id, ssa_id, mpa_id = 0, 0, 0, 0, 8
  for line in pede_files:
    stage, chip, pede_file_path = line["stage"], line["chip"], line["file"]
    if chip == "ssa":
      if stage == "pre-trim":
        f_ssa_pre_trim = TFile.Open(f'results/{pede_file_path}/Hybrid.root', 'READ')
        h_ssa_pre_trim = f_ssa_pre_trim.Get(f'Detector/Board_{board_id}/OpticalGroup_{optical_group_id}/Hybrid_{hybrid_id}/SSA_{ssa_id}/D_B({board_id})_O({optical_group_id})_H({hybrid_id})_ChannelPedestalDistribution_Chip({ssa_id})')
      else:
        f_ssa_post_trim = TFile.Open(f'results/{pede_file_path}/Hybrid.root', 'READ')
        h_ssa_post_trim = f_ssa_post_trim.Get(f'Detector/Board_{board_id}/OpticalGroup_{optical_group_id}/Hybrid_{hybrid_id}/SSA_{ssa_id}/D_B({board_id})_O({optical_group_id})_H({hybrid_id})_ChannelPedestalDistribution_Chip({ssa_id})')

    else:
      if stage == "pre-trim":
        f_mpa_pre_trim = TFile.Open(f'results/{pede_file_path}/Hybrid.root', 'READ')
        h_mpa_pre_trim = f_mpa_pre_trim.Get(f'Detector/Board_{board_id}/OpticalGroup_{optical_group_id}/Hybrid_{hybrid_id}/MPA_{mpa_id}/D_B({board_id})_O({optical_group_id})_H({hybrid_id})_ChannelPedestalDistribution_Chip({mpa_id})')
      else:
        f_mpa_post_trim = TFile.Open(f'results/{pede_file_path}/Hybrid.root', 'READ')
        h_mpa_post_trim = f_mpa_post_trim.Get(f'Detector/Board_{board_id}/OpticalGroup_{optical_group_id}/Hybrid_{hybrid_id}/MPA_{mpa_id}/D_B({board_id})_O({optical_group_id})_H({hybrid_id})_ChannelPedestalDistribution_Chip({mpa_id})')

  pre_trim_ssa_ch, post_trim_ssa_ch, pre_trim_mpa_ch, post_trim_mpa_ch = h_ssa_pre_trim.GetBinContent(100), h_ssa_post_trim.GetBinContent(100), h_mpa_pre_trim.GetBinContent(100), h_mpa_post_trim.GetBinContent(100),
    
  x_ssa, x_mpa = [], []
  y_ssa_pre_trim, y_ssa_post_trim, y_mpa_pre_trim, y_mpa_post_trim = [], [], [], []
  #for ssa
  for ch_id in range(1, h_ssa_pre_trim.GetNbinsX()):
    x_ssa.append(ch_id) 
    y_ssa_pre_trim.append(h_ssa_pre_trim.GetBinContent(ch_id))
    y_ssa_post_trim.append(h_ssa_post_trim.GetBinContent(ch_id))

  #for mpa
  for ch_id in range(1, h_mpa_pre_trim.GetNbinsX()):
    x_mpa.append(ch_id) 
    y_mpa_pre_trim.append(h_mpa_pre_trim.GetBinContent(ch_id))
    y_mpa_post_trim.append(h_mpa_post_trim.GetBinContent(ch_id))

  plt.figure(1)
  plt.plot(x_ssa, y_ssa_pre_trim, linestyle='None', marker='x', markersize=5, color='darkred', label='pre-equalization')
  plt.plot(x_ssa, y_ssa_post_trim, linestyle='None', marker='*', markersize=5, color='darkgreen', label='post-equalization')
  #plt.ylim(50,100)
  plt.ylim(50,100)
  plt.xlabel('Channel Number')
  plt.ylabel('Amplitude (ThDAC)')
  plt.grid()
  legend = plt.legend(loc='upper right')
  legend.legendHandles[0]._legmarker.set_markersize(6)
  legend.legendHandles[1]._legmarker.set_markersize(6)
  plt.savefig("./plots/pedestal_equalization_ssa.pdf")

  plt.figure(2)
  plt.plot(x_mpa, y_mpa_pre_trim, linestyle='None', marker='x', markersize=4, color='darkred', label='pre-equalization')
  plt.plot(x_mpa, y_mpa_post_trim, linestyle='None', marker='*', markersize=4, color='darkgreen', label='post-equalization')
  #plt.ylim(150,275)
  plt.ylim(150,270)
  plt.xlabel('Channel Number')
  plt.ylabel('Amplitude (ThDAC)')
  plt.grid()
  legend = plt.legend(loc='upper right')
  legend.legendHandles[0]._legmarker.set_markersize(6)
  legend.legendHandles[1]._legmarker.set_markersize(6)
  plt.savefig("./plots/pedestal_equalization_mpa.pdf")
        
if __name__ == "__main__":
  sys.exit(main())

