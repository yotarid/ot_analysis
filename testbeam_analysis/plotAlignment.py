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
  h_psp_initial, h_psp_final = TH1F(), TH1F()
  h_pss_initial, h_pss_final = TH1F(), TH1F()

  res_x, psp_cnt_initial, psp_cnt_final, pss_cnt_initial, pss_cnt_final = [], [], [], [], []

  for line in csv_file:
    step, file = line["step"], line["file"]
    if step == "initial":
      f_initial = TFile.Open(f'{folder}/{file}', 'READ')  
      h_psp_initial = f_initial.AlignmentDUTResidual.CMSPhase2_30.residualsX
      h_pss_initial = f_initial.AlignmentDUTResidual.CMSPhase2_31.residualsX
    else:
      f_final = TFile.Open(f'{folder}/{file}', 'READ')  
      h_psp_final = f_final.AlignmentDUTResidual.CMSPhase2_30.residualsX
      h_pss_final = f_final.AlignmentDUTResidual.CMSPhase2_31.residualsX
   
  for res in range(1, h_psp_final.GetNbinsX()):
    res_x.append(h_psp_final.GetBinLowEdge(res))
    psp_cnt_initial.append(h_psp_initial.GetBinContent(res))
    psp_cnt_final.append(h_psp_final.GetBinContent(res))

    pss_cnt_initial.append(h_pss_initial.GetBinContent(res))
    pss_cnt_final.append(h_pss_final.GetBinContent(res))

  nbins =  int(max(res_x) - min(res_x))

  fig1, ax1 = plt.subplots()
  plt.tight_layout()
  ax1.hist(res_x, weights=psp_cnt_initial, bins=nbins, density=False, histtype='step', color='darkred', linewidth=1, fill=False, label='Initial alignment', zorder=3)
  ax1.hist(res_x, weights=psp_cnt_final, bins=nbins, density=False, histtype='step', color='darkgreen', linewidth=1, fill=False, label='Final alignment', zorder=3)
  ax1.grid(zorder=0, alpha=0.5)
  ax1.set_xlabel("Residuals X ($\mathrm{\mu m}$)", fontsize=16)
  ax1.set_xlim(-200,200)
  ax1.set_ylabel("Entries", fontsize=16)
  ax1.set_box_aspect(1)
  legend = ax1.legend(loc='upper left', ncol=1, fontsize=16, bbox_to_anchor=(1., 1.03))
  plt.savefig("./plots/alignment_psp.pdf", bbox_inches="tight")


  fig2, ax2 = plt.subplots()
  plt.tight_layout()
  ax2.hist(res_x, weights=pss_cnt_initial, bins=nbins, density=False, histtype='step', color='darkred', linewidth=1, fill=False, label='Initial alignment', zorder=3)
  ax2.hist(res_x, weights=pss_cnt_final, bins=nbins, density=False, histtype='step', color='darkgreen', linewidth=1, fill=False, label='Final alignment', zorder=3)
  ax2.grid(zorder=0, alpha=0.5)
  ax2.set_xlabel("Residuals X ($\mathrm{\mu m}$)", fontsize=16)
  ax2.set_xlim(-200,200)
  ax2.set_ylabel("Entries", fontsize=16)
  ax2.set_box_aspect(1)
  legend = ax2.legend(loc='upper left', ncol=1, fontsize=16, bbox_to_anchor=(1., 1.03))
  plt.savefig("./plots/alignment_pss.pdf", bbox_inches="tight")

       
if __name__ == "__main__":
  sys.exit(main())


