from ROOT import TFile, TH1F, TCanvas, gStyle
import csv, argparse, sys
import numpy as np
import math
from scipy import optimize, special
import matplotlib
matplotlib.rc('font',family='Times New Roman') 
matplotlib.rc('xtick', labelsize=14)
matplotlib.rc('ytick', labelsize=14)
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter, MaxNLocator

def parseCSV(file_path):
  print('Parsing CSV file : {}'.format(file_path))
  csv_file = open(file_path, mode='r') 
  return csv.DictReader(csv_file)

def fit_func(x, p0, p1, p2, p3):
    return 1 - 1/2 * (p0 + p1*special.erf((x-p2)/p3))

def main():
  parser = argparse.ArgumentParser(description="correlation plot")
  parser.add_argument('-file', help="CSV file to be parsed")

  args = parser.parse_args()
  file_list = parseCSV(args.file)

  stub_latency_values, stub_latency_entries = [], []
  mpa_latency_values, mpa_latency_entries_edge, mpa_latency_entries_level = [], [], []
  ssa_latency_values, ssa_latency_entries_edge, ssa_latency_entries_level = [], [], []

  f_edge, f_level, f_stub = TFile(), TFile(), TFile() 
  h_mpa_edge, h_mpa_level, h_ssa_edge, h_ssa_level, h_stub = TH1F(), TH1F(), TH1F(), TH1F(), TH1F()


  board_id, optical_group_id, hybrid_id = 0, 0, 0
  for line in file_list:
    data, mode, folder = line["data"], line["mode"], line["folder"]
    if data == "stub":
      f_stub = TFile.Open(f'results/{folder}/Hybrid.root', 'READ')
      h_stub = f_stub.Get(f'Detector/Board_{board_id}/OpticalGroup_{optical_group_id}/Hybrid_{hybrid_id}/D_B({board_id})_O({optical_group_id})_StubValue_Hybrid({hybrid_id})')
    else:
      if mode == "edge":
        f_edge = TFile.Open(f'results/{folder}/Hybrid.root', 'READ')
        h_mpa_edge = f_edge.Get(f'Detector/Board_{board_id}/OpticalGroup_{optical_group_id}/Hybrid_{hybrid_id}/D_B({board_id})_O({optical_group_id})_LatencyValueS0_Hybrid({hybrid_id})')
        h_ssa_edge = f_edge.Get(f'Detector/Board_{board_id}/OpticalGroup_{optical_group_id}/Hybrid_{hybrid_id}/D_B({board_id})_O({optical_group_id})_LatencyValueS1_Hybrid({hybrid_id})')
      else:
        f_level = TFile.Open(f'results/{folder}/Hybrid.root', 'READ')
        h_mpa_level = f_level.Get(f'Detector/Board_{board_id}/OpticalGroup_{optical_group_id}/Hybrid_{hybrid_id}/D_B({board_id})_O({optical_group_id})_LatencyValueS0_Hybrid({hybrid_id})')
        h_ssa_level = f_level.Get(f'Detector/Board_{board_id}/OpticalGroup_{optical_group_id}/Hybrid_{hybrid_id}/D_B({board_id})_O({optical_group_id})_LatencyValueS1_Hybrid({hybrid_id})')
  
  #stubs 
  for x in range(1, h_stub.GetNbinsX()):
    stub_latency_values.append(h_stub.GetBinLowEdge(x))
    stub_latency_entries.append(h_stub.GetBinContent(x))

  #edge
  for x in range(1, h_mpa_edge.GetNbinsX()):
    mpa_latency_values.append(int(h_mpa_edge.GetBinLowEdge(x)))
    ssa_latency_values.append(int(h_mpa_edge.GetBinLowEdge(x))-1)
    mpa_latency_entries_edge.append(h_mpa_edge.GetBinContent(x))
    ssa_latency_entries_edge.append(h_ssa_edge.GetBinContent(x))

  #level
  for x in range(1, h_mpa_level.GetNbinsX()):
    #mpa_latency_values.append(x)
    mpa_latency_entries_level.append(h_mpa_level.GetBinContent(x))
    ssa_latency_entries_level.append(h_ssa_level.GetBinContent(x))

  fig, ax = plt.subplots()
  axes = fig.gca()
  nbins = int(max(mpa_latency_values) - min(mpa_latency_values))
  #plt.hist(stub_latency_values, weights=stub_latency_entries, histtype='step', color='darkgreen', linewidth=2, label='Stub Latency', zorder=3)
  #plt.hist(mpa_latency_values, weights=mpa_latency_entries_level, bins=nbins, histtype='step', color='darkred', linewidth=2, fill=True, alpha=0.5, label='Edge', zorder=3)
  ax.hist(mpa_latency_values, weights=mpa_latency_entries_edge, bins=nbins, histtype='step', color='darkred', linewidth=2, fill=True, alpha=0.5, label='MPA', zorder=3)
  ax.hist(ssa_latency_values, weights=ssa_latency_entries_edge, bins=nbins, histtype='step', color='navy', linewidth=2, fill=True, alpha=0.5, label='SSA', zorder=3)
  axes.get_xaxis().set_major_locator(MaxNLocator(integer=True))
  ax.set_xlim(117,123)
  ax.grid(zorder=0, alpha=0.5)
  ax.set_xlabel("Latency (BX cycles)", fontsize=14)
  ax.set_ylabel("Entries", fontsize=14)
  ax.legend(loc='upper left', fontsize=14)
  ax.set_box_aspect(1)
  plt.savefig("./plots/latency.pdf", bbox_inches="tight")

  #fig = plt.figure(2)
  #axes = fig.gca()
  #plt.hist(mpa_latency_values, weights=ssa_latency_entries_edge, bins=nbins, histtype='step', color='navy', linewidth=2, fill=True, alpha=0.5, label='Edge', zorder=3)
  #plt.hist(mpa_latency_values, weights=ssa_latency_entries_level, bins=nbins, histtype='step', color='navy', linewidth=2, hatch='/', label='Level', zorder=3)
  #axes.get_xaxis().set_major_locator(MaxNLocator(integer=True))
  #plt.grid(zorder=0, alpha=0.5)
  #plt.xlabel("Latency (BX cycles)", fontsize=12)
  #plt.ylabel("Entries", fontsize=12)
  #plt.legend(loc='upper right', fontsize=12)
  #plt.savefig("./plots/ssa_latency.pdf", bbox_inches="tight")

  
if __name__ == "__main__":
  sys.exit(main())
