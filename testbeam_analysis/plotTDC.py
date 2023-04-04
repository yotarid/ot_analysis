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
  parser = argparse.ArgumentParser(description="TDC plot")
  parser.add_argument('-file', help="root file")

  args = parser.parse_args()
  result_file = TFile(args.file, 'READ')

  psp_tdc_eff = result_file.AnalysisEfficiency.CMSPhase2_30.efficiencyVsTagTProfile_TDC
  pss_tdc_eff = result_file.AnalysisEfficiency.CMSPhase2_31.efficiencyVsTagTProfile_TDC
  stub_tdc_eff = result_file.AnalysisStubEfficiency.efficiencyVsTagTProfile_TDC

  tdc, psp_eff, pss_eff, stub_eff = [], [], [], []
  for tdc_bin in range(1, psp_tdc_eff.GetNbinsX()+1):
    tdc.append(int(tdc_bin)-1)
    psp_eff.append(psp_tdc_eff.GetBinContent(tdc_bin))
    pss_eff.append(pss_tdc_eff.GetBinContent(tdc_bin))
    stub_eff.append(stub_tdc_eff.GetBinContent(tdc_bin))

  fig, ax = plt.subplots()
  psp_eff = np.flip(np.roll(psp_eff, 5))
  pss_eff = np.flip(np.roll(pss_eff, 5))
  stub_eff = np.flip(np.roll(stub_eff, 5))

  ax.stairs(psp_eff, color='darkred', label='PS-p')
  plt.scatter(np.linspace(0.5, 7.5, 8), psp_eff, marker='o', c='darkred', s=20, alpha=1)

  ax.stairs(pss_eff, color='navy', label='PS-s')
  plt.scatter(np.linspace(0.5, 7.5, 8), pss_eff, marker='o', c='navy', s=20, alpha=1)

  ax.stairs(stub_eff, color='darkgreen', label='Stubs')
  plt.scatter(np.linspace(0.5, 7.5, 8), stub_eff, marker='o', c='darkgreen', s=20, alpha=1)

  axes = fig.gca()
  axes.get_xaxis().set_major_locator(MaxNLocator(integer=True))
  ax.set_xlim(0,8)
  ax.grid(zorder=0, alpha=0.5)
  ax.set_xlabel("TDC phase", fontsize=16)
  ax.set_ylabel("Efficiency", fontsize=16)
  legend = ax.legend(loc='upper left', ncol=1, fontsize=16, bbox_to_anchor=(1., 1.03))
  ax.set_box_aspect(1)
  plt.savefig("./plots/tdc.pdf", bbox_inches="tight")
       
if __name__ == "__main__":
  sys.exit(main())
 
