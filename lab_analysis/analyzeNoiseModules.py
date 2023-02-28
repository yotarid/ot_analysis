from ROOT import *
import ROOT
import csv, argparse, sys
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy import optimize, special
import matplotlib
matplotlib.rc('font',family='Times New Roman') 
matplotlib.rc('xtick', labelsize=16)
matplotlib.rc('ytick', labelsize=16)
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import ScalarFormatter
matplotlib.use('Agg')

def parseCSV(file_path):
  print('Parsing CSV file : {}'.format(file_path))
  csv_file = open(file_path, mode='r') 
  return csv.DictReader(csv_file)

def fit_func(x, mu, sigma):
  return 0.5 * special.erfc((x - mu) / (sqrt(2.) * sigma))

def main():
  parser = argparse.ArgumentParser(description="Noise")
  parser.add_argument('-csv', help="CSV file to be parsed")

  args = parser.parse_args()
  csv_file = parseCSV(args.csv)

  f_ssa, f_mpa = TFile(), TFile()
  h_scurve_ssa, h_scurve_mpa = TH2F(), TH2F()
  board_id, optical_group_id = 0,0

  mpa_noise_dict = {}
  ssa_noise_dict = {}
  modules = []

  for line in csv_file:
    module, folder = line["module"], line["folder"]
    
    modules.append(module)

    ext_ssa, ext_mpa = "", ""

    f_ssa = TFile.Open(f'results/{folder}/Hybrid'+ str(ext_ssa) +'.root', 'READ')
    f_mpa = TFile.Open(f'results/{folder}/Hybrid' + str(ext_mpa) + '.root', 'READ')

    if module == "PS_40_05_DSY-00005":
      optical_group_id = 1

    noise_mpa, noise_ssa = [], []
    
    ssa_p0_mean, ssa_p0_sig = 77, 6
    mpa_p0_mean, mpa_p0_sig = 200, 3

    print()
    for hybrid_local_id in range(0, 1):
      hybrid_id = 2*optical_group_id + hybrid_local_id
      for chip_id in range(0, 8):
        ssa_id, mpa_id = chip_id, chip_id + 8
        print(f'Module : {module} -- Hybrid : {hybrid_id} -- Chip : {chip_id}')

        #for ssa
        h_scurve_ssa = f_ssa.Get(f'Detector/Board_{board_id}/OpticalGroup_{optical_group_id}/Hybrid_{hybrid_id}/SSA_{ssa_id}/D_B({board_id})_O({optical_group_id})_H({hybrid_id})_SCurve_Chip({ssa_id})')
        if h_scurve_ssa == None:
          continue
        for ch_id in range(0, h_scurve_ssa.GetNbinsX()):
          x_array, y_array = [], []
          for th in range(0, h_scurve_ssa.GetNbinsY()):
            x_array.append(th) 
            y_array.append(h_scurve_ssa.GetBinContent(ch_id, th))
          fit_param, cov = optimize.curve_fit(fit_func, np.array(x_array), np.array(y_array), p0=[ssa_p0_mean, ssa_p0_sig], maxfev=10000)
          noise_ssa.append(fit_param[1])

        #for mpa
        h_scurve_mpa = f_mpa.Get(f'Detector/Board_{board_id}/OpticalGroup_{optical_group_id}/Hybrid_{hybrid_id}/MPA_{mpa_id}/D_B({board_id})_O({optical_group_id})_H({hybrid_id})_SCurve_Chip({mpa_id})')
        if h_scurve_mpa == None:
          continue
        for ch_id in range(0, h_scurve_mpa.GetNbinsX()):
          x_array, y_array = [], []
          for th in range(0, h_scurve_mpa.GetNbinsY()):
            x_array.append(th) 
            y_array.append(h_scurve_mpa.GetBinContent(ch_id, th))
          fit_param, cov = optimize.curve_fit(fit_func, np.array(x_array), np.array(y_array), p0=[mpa_p0_mean, mpa_p0_sig], maxfev=10000)
          noise_mpa.append(fit_param[1])
     
    mpa_noise_dict[module] = noise_mpa
    ssa_noise_dict[module] = noise_ssa

  ssa_thdac, mpa_thdac = 250, 94

  fig1, ax1 = plt.subplots()
  plt.tight_layout()

  m_colors = ["orange", "purple", "brown", "olive"]

  #ssa
  ax11 = ax1.twiny()
  ax11.set_xlabel(r"Channel Noise ($e^{-}$)", fontsize=16)
  ax11.set_xlim(0,8*ssa_thdac)
  #ax11.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
  ax11.set_box_aspect(1)

  for idx, m in enumerate(modules):
    print('Module ' + str(m) + ' ' + str(len(ssa_noise_dict[m])))
    ax1.hist(ssa_noise_dict[m], bins=40, range=(0,10), density=True, histtype='step', color=m_colors[idx], linewidth=1, label=m, zorder=3)

  ax1.set_xlabel('Channel Noise (ThDAC)', fontsize=16)
  ax1.set_ylabel('Entries', fontsize=16)
  ax1.grid(zorder=0, alpha=0.5)
  #ax1.set_xlim(0,8)
  ax1.set_ylim(0,2)
  #ax1.xaxis.set_ticks(np.arange(0,8.1,2))
  ax1.yaxis.set_ticks(np.arange(0,2.1,0.2))
  legend = ax1.legend(loc='upper left', ncol=1, fontsize=16, bbox_to_anchor=(1., 1.03))
  ax1.set_box_aspect(1)
  plt.savefig("./plots/noise_modules_ssa.pdf", bbox_inches="tight")


  #mpa
  fig2, ax2 = plt.subplots()
  plt.tight_layout()

  ax22 = ax2.twiny()
  ax22.set_xlabel(r"Channel Noise ($e^{-}$)", fontsize=16)
  ax22.set_xlim(0, 500)
  #ax22.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
  ax22.set_box_aspect(1)

  for idx, m in enumerate(modules):
    print('Module ' + str(m) + ' ' + str(len(mpa_noise_dict[m])))
    ax2.hist(mpa_noise_dict[m], bins=40, range=(0,10), density=True, histtype='step', color=m_colors[idx], linewidth=1, label=m, zorder=3)

  ax2.set_xlabel('Channel Noise (ThDAC)', fontsize=16)
  ax2.set_ylabel('Entries', fontsize=16)
  ax2.grid(zorder=0, alpha=0.5)
  #ax2.set_xlim(0,8)
  ax2.set_ylim(0,2)
  #ax2.xaxis.set_ticks(np.arange(0,8.1,2))
  ax2.yaxis.set_ticks(np.arange(0,2.3,0.2))
  ax2.set_box_aspect(1)

  legend = ax2.legend(loc='upper left', ncol=1, fontsize=16, bbox_to_anchor=(1., 1.03))
  plt.savefig("./plots/noise_modules_mpa.pdf", bbox_inches="tight")

if __name__ == "__main__":
  sys.exit(main())


