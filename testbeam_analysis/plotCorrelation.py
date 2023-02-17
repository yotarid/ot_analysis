from ROOT import TFile 
import csv, argparse, sys
import numpy as np
import math
from scipy import optimize, special
import matplotlib
matplotlib.rc('font',family='Times New Roman') 
matplotlib.rc('xtick', labelsize=12)
matplotlib.rc('ytick', labelsize=12)
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
  
  psp_corr = result_file.Correlations.CMSPhase2_30.correlationX_2Dlocal
  pss_corr = result_file.Correlations.CMSPhase2_31.correlationX_2Dlocal

  telescope_ch, psp_ch, psp_entries, pss_ch, pss_entries = [], [], [], [], []
  for ps_ch in range(1, psp_corr.GetNbinsY()):
    for tele_ch in range(1, psp_corr.GetNbinsY()):
      telescope_ch.append(tele_ch)
      psp_ch.append(ps_ch)
      psp_entries.append(psp_corr.GetBinContent(ps_ch, tele_ch))
      pss_ch.append(ps_ch)
      pss_entries.append(pss_corr.GetBinContent(ps_ch, tele_ch))

  fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
  plt.tight_layout()

  hist1 = ax1.hist2d(psp_ch, telescope_ch, bins=[psp_corr.GetNbinsX(), psp_corr.GetNbinsY()], weights=psp_entries, cmap=plt.cm.jet)
  ax1.set_xlim(620, 850)
  ax1.set_xlabel("PS-p X", fontsize=12)
  ax1.set_ylabel("Telescope X", fontsize=12)
  ax1.set_box_aspect(1)
  fig.colorbar(hist1[3], ax=ax1, location='right', fraction=0.046, pad=0.04)

  hist2 = ax2.hist2d(pss_ch, telescope_ch, bins=[pss_corr.GetNbinsX(), pss_corr.GetNbinsY()], weights=pss_entries, cmap=plt.cm.jet)
  ax2.set_xlim(620, 850)
  ax2.set_xlabel("PS-s X", fontsize=12)
  ax2.set_box_aspect(1)
  fig.colorbar(hist2[3], ax=ax2, location='right', fraction=0.046, pad=0.04)

  plt.savefig("./plots/correlation.pdf", bbox_inches="tight")

if __name__ == "__main__":
  sys.exit(main())
