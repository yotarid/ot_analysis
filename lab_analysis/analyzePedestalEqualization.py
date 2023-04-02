from ROOT import *
import ROOT
import csv, argparse, sys
import numpy as np
import math
from scipy import optimize, special
import matplotlib
matplotlib.rc('font',family='Times New Roman') 
matplotlib.rc('xtick', labelsize=16)
matplotlib.rc('ytick', labelsize=16)
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
matplotlib.use('Agg')

def parseCSV(file_path):
  print('Parsing CSV file : {}'.format(file_path))
  csv_file = open(file_path, mode='r') 
  return csv.DictReader(csv_file)

def main():
  parser = argparse.ArgumentParser(description="Pedestal Equalization")
  parser.add_argument('-csv', help="CSV file to be parsed")

  args = parser.parse_args()
  csv_file = parseCSV(args.csv)

  f_ssa_pre_trim, f_ssa_post_trim, f_mpa_pre_trim, f_mpa_post_trim = TFile(), TFile(), TFile(), TFile()
  h_ssa_pre_trim, h_ssa_post_trim, h_mpa_pre_trim, h_mpa_post_trim = TH1F(), TH1F(), TH1F(), TH1F()
  board_id, optical_group_id, hybrid_id, ssa_id, mpa_id = 0, 0, 0, 0, 8
  for line in csv_file:
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

  #plt.figure(1)
  fig1, ax1 = plt.subplots()
  plt.tight_layout()

  ax1.plot(x_ssa, y_ssa_pre_trim, linestyle='None', marker='x', markersize=5, color='darkred', alpha=0.5, label='Pre-equalization')
  ax1.plot(x_ssa, y_ssa_post_trim, linestyle='None', marker='*', markersize=5, color='darkgreen', label='Post-equalization')
  ax1.set_ylim(70,90)
  ax1.yaxis.set_ticks(np.arange(70,91,5))
  ax1.set_xlabel('Channel number', fontsize=16)
  ax1.set_ylabel('Pedestal (ThDAC)', fontsize=16)
  ax1.grid(alpha=0.5)
  ax1.set_box_aspect(1)
  legend = ax1.legend(loc='upper left', ncol=1, fontsize=16, handletextpad=0.1, bbox_to_anchor=(1., 1.03))
  legend.legendHandles[0]._legmarker.set_markersize(6)
  legend.legendHandles[1]._legmarker.set_markersize(6)
  plt.savefig("./plots/pedestal_equalization_ssa.pdf", bbox_inches="tight")


  fig2, ax2 = plt.subplots()
  plt.tight_layout()
  ax2.plot(x_mpa, y_mpa_pre_trim, linestyle='None', marker='x', markersize=5, color='darkred', alpha=0.5, label='Pre-equalization')
  ax2.plot(x_mpa, y_mpa_post_trim, linestyle='None', marker='*', markersize=5, color='darkgreen', label='Post-equalization')
  ax2.set_ylim(150,270)
  ax2.yaxis.set_ticks(np.arange(150,271,20))
  ax2.set_xlabel('Channel number', fontsize=16)
  ax2.set_ylabel('Pedestal (ThDAC)', fontsize=16)
  ax2.grid(alpha=0.5)
  ax2.set_box_aspect(1)

  legend = ax2.legend(loc='upper left', ncol=1, fontsize=16, handletextpad=0.1, bbox_to_anchor=(1., 1.03))
  legend.legendHandles[0]._legmarker.set_markersize(6)
  legend.legendHandles[1]._legmarker.set_markersize(6)
  plt.savefig("./plots/pedestal_equalization_mpa.pdf", bbox_inches="tight")
  #plt.savefig("./plots/pedestal_equalization.pdf")

        
if __name__ == "__main__":
  sys.exit(main())

