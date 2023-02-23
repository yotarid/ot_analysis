from ROOT import TFile, TH1F
import csv, argparse, sys
import numpy as np
import math
from scipy import optimize, special
import matplotlib
matplotlib.rc('font',family='Times New Roman') 
matplotlib.rc('xtick', labelsize=16)
matplotlib.rc('ytick', labelsize=16)
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter, MaxNLocator

def parseCSV(file_path):
  print('Parsing CSV file : {}'.format(file_path))
  csv_file = open(file_path, mode='r') 
  return csv.DictReader(csv_file)

def main():
  parser = argparse.ArgumentParser(description="correlation plot")
  parser.add_argument('-folder', help="CSV file to be parsed")
  parser.add_argument('-csv', help="CSV file to be parsed")

  args = parser.parse_args()
  csv_file = parseCSV(args.csv)
  folder = args.folder

  f_initial, f_final = TFile(), TFile() 
  h_chi2_initial, h_chi2_final, h_ntracks = TH1F(), TH1F(), TH1F()

  chi2_x, chi2_cnt_initial, chi2_cnt_final, ntracks_x, ntracks_cnt = [], [], [], [], []

  for line in csv_file:
    step, file = line["step"], line["file"]
    if step == "initial":
      f_initial = TFile.Open(f'{folder}/{file}', 'READ')  
      h_chi2_initial = f_initial.Tracking4D.trackChi2ndof
      h_ntracks = f_initial.Tracking4D.tracksPerEvent
    else:
      f_final = TFile.Open(f'{folder}/{file}', 'READ')  
      h_chi2_final = f_final.Tracking4D.trackChi2ndof
   
  for chi2 in range(1, h_chi2_initial.GetNbinsX()):
    chi2_x.append(h_chi2_initial.GetBinLowEdge(chi2))
    chi2_cnt_initial.append(h_chi2_initial.GetBinContent(chi2))
    chi2_cnt_final.append(h_chi2_final.GetBinContent(chi2))

  for ntracks in range(1, h_ntracks.GetNbinsX()):
    ntracks_x.append(h_ntracks.GetBinLowEdge(ntracks))
    ntracks_cnt.append(h_ntracks.GetBinContent(ntracks))


  fig1, ax1 = plt.subplots()
  plt.tight_layout()
  chi2_nbins =  int(max(chi2_x) - min(chi2_x))
  ax1.hist(chi2_x, weights=chi2_cnt_final, bins=chi2_nbins*10, density=True, histtype='step', color='navy', linewidth=1, fill=False, label='Final Tracking', zorder=3)
  ax1.set_xlim(0,10)
  ax1.grid(zorder=0, alpha=0.5)
  ax1.set_xlabel("Track $\mathrm{\chi ^{2}/ndof}$", fontsize=16)
  ax1.set_ylabel("Entries (normalized)", fontsize=16)
  ax1.set_box_aspect(1)
  plt.savefig("./plots/chi2.pdf", bbox_inches="tight")



  fig2, ax2 = plt.subplots()
  plt.tight_layout()
  ntracks_nbins =  int(max(ntracks_x) - min(ntracks_x))
  ax2.hist(ntracks_x, weights=ntracks_cnt, bins=ntracks_nbins, density=True, histtype='step', color='navy', linewidth=1, fill=False, label='Final Tracking', zorder=3)
  ax2.grid(zorder=0, alpha=0.5)
  ax2.set_xlim(0,10)
  ax2.set_xlabel("Tracks", fontsize=16)
  ax2.set_ylabel("Entries (normalized)", fontsize=16)
  ax2.set_box_aspect(1)
  
  plt.savefig("./plots/ntracks.pdf", bbox_inches="tight")

       
if __name__ == "__main__":
  sys.exit(main())


