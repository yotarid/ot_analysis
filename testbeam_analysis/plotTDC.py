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
  parser.add_argument('-file', help="root file")

  args = parser.parse_args()
  result_file = TFile(args.file, 'READ')

  psp_tdc_eff = result_file.AnalysisEfficiency.CMSPhase2_30.efficiencyVsTagTProfile_TDC
  pss_tdc_eff = result_file.AnalysisEfficiency.CMSPhase2_31.efficiencyVsTagTProfile_TDC
  stub_tdc_eff = result_file.AnalysisStubEfficiency.efficiencyVsTagTProfile_TDC

  tdc, psp_eff, pss_eff, stub_eff = [], [], [], []
  for tdc_bin in range(1, psp_tdc_eff.GetNbinsX()+1):
    tdc.append(int(tdc_bin)-1)
    psp_eff.append(psp_tdc_eff.GetBinContent(tdc_bin)*100)
    pss_eff.append(pss_tdc_eff.GetBinContent(tdc_bin)*100)
    stub_eff.append(stub_tdc_eff.GetBinContent(tdc_bin)*100)

  fig, ax = plt.subplots()
  axes = fig.gca()
  psp_eff = np.flip(np.roll(psp_eff, 5))
  pss_eff = np.flip(np.roll(pss_eff, 5))
  stub_eff = np.flip(np.roll(stub_eff, 5))
  #nbins = int(max(tdc) - min(tdc)) 
  n,bins,patches = ax.hist(tdc, weights=psp_eff, bins=8, histtype='step', color='darkred', linewidth='1', fill=False, label='PS-p', zorder=3)
  plt.scatter(bins[:-1]+ 0.5*(bins[1:] - bins[:-1]), n, marker='o', c='darkred', s=20, alpha=1)

  n,bins,patches = ax.hist(tdc, weights=pss_eff, bins=8, histtype='step', color='navy', linewidth='1', fill=False, label='PS-s', zorder=3)
  plt.scatter(bins[:-1]+ 0.5*(bins[1:] - bins[:-1]), n, marker='o', c='navy', s=20, alpha=1)

  n,bins,patches = ax.hist(tdc, weights=stub_eff, bins=8, histtype='step', color='darkgreen', linewidth='1', fill=False, label='Stub', zorder=3)
  plt.scatter(bins[:-1]+ 0.5*(bins[1:] - bins[:-1]), n, marker='o', c='darkgreen', s=20, alpha=1)

  axes.get_xaxis().set_major_locator(MaxNLocator(integer=True))
  ax.set_xlim(0,7)
  ax.grid(zorder=0, alpha=0.5)
  ax.set_xlabel("TDC phase", fontsize=16)
  ax.set_ylabel("Efficiency (%)", fontsize=16)
  legend = plt.legend(loc='upper right', ncol=3, columnspacing=1.2, fontsize=15, bbox_to_anchor=(1.01, 1.15))
  ax.set_box_aspect(1)
  plt.savefig("./plots/tdc.pdf", bbox_inches="tight")
       
if __name__ == "__main__":
  sys.exit(main())
 
