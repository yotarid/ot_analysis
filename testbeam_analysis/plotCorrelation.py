from ROOT import TFile 
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

def fit_func(x, p0, p1, p2, p3):
    return 1 - 1/2 * (p0 + p1*special.erf((x-p2)/p3))

def main():
  parser = argparse.ArgumentParser(description="correlation plot")
  parser.add_argument('-file', help="root file")
  #parser.add_argument('-file', help="CSV file to be parsed")
  #parser.add_argument('-campaign', help="Beam Test campaign")

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

  plt.figure(1)
  plt.hist2d(psp_ch, telescope_ch, bins=[psp_corr.GetNbinsX(), psp_corr.GetNbinsY()], weights=psp_entries, cmap=plt.cm.jet)
  plt.xlim(620, 850)
  plt.xlabel("PS-p Channel X")
  plt.ylabel("Telescope Channel X")
  #plt.savefig("./plots/psp_correlation.pdf", bbox_inches="tight")
  plt.savefig("./plots/psp_correlation.png", bbox_inches="tight")

  plt.figure(2)
  plt.hist2d(pss_ch, telescope_ch, bins=[pss_corr.GetNbinsX(), pss_corr.GetNbinsY()], weights=pss_entries, cmap=plt.cm.jet)
  plt.xlim(620, 850)
  plt.xlabel("PS-s Channel X")
  plt.ylabel("Telescope Channel X")
  #plt.savefig("./plots/pss_correlation.pdf", bbox_inches="tight")
  plt.savefig("./plots/pss_correlation.png", bbox_inches="tight")

if __name__ == "__main__":
  sys.exit(main())
