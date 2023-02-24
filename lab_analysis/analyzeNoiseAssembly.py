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
  parser.add_argument('-file', help="CSV file to be parsed")

  args = parser.parse_args()
  noise_files = parseCSV(args.file)

  f_ssa, f_mpa = TFile(), TFile()
  h_scurve_ssa, h_scurve_mpa = TH2F(), TH2F()
  board_id, optical_group_id = 0,0

  
  #module_noise_map = {
  #  0:{
  #    "SSA":{
  #      0:[],  1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]
  #    },
  #    "MPA":{
  #      0:[],  1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]
  #    }
  #  },
  #  
  #  1:{
  #    "SSA":{
  #      0:[],  1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]
  #    },
  #    "MPA":{
  #      0:[],  1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]
  #    }
  #  }  
  #}

  ssa_noise_array = {"pre-assembly":[], "pre-encapsulation":[], "post-encapsulation":[]}
  mpa_noise_array = {"pre-assembly":[], "pre-encapsulation":[], "post-encapsulation":[]}

  for line in noise_files:
    stage, folder = line["stage"], line["folder"]
    f_noise = TFile.Open(f'results/{folder}/Hybrid.root', 'READ')
    if stage == "pre-encapsulation" or stage == "post-encapsulation":
      optical_group_id = 1
    for hybrid_local_id in range(0, 2):
      hybrid_id = 2*optical_group_id + hybrid_local_id
      hybrid_ssa, hybrid_mpa = [], []
      for chip_id in range(0, 8):
        ssa_id, mpa_id = chip_id, chip_id + 8
        print(hybrid_local_id, chip_id)

        #for ssa
        chip_ssa = []
        h_scurve_ssa = f_noise.Get(f'Detector/Board_{board_id}/OpticalGroup_{optical_group_id}/Hybrid_{hybrid_id}/SSA_{ssa_id}/D_B({board_id})_O({optical_group_id})_H({hybrid_id})_SCurve_Chip({ssa_id})')
        if h_scurve_ssa == None:
          continue
        for ch_id in range(0, h_scurve_ssa.GetNbinsX()):
          x_array, y_array = [], []
          for th in range(0, h_scurve_ssa.GetNbinsY()):
            x_array.append(th) 
            y_array.append(h_scurve_ssa.GetBinContent(ch_id, th))
          fit_param, cov = optimize.curve_fit(fit_func, np.array(x_array), np.array(y_array), p0=[77, 6], maxfev=10000)
          ssa_noise_array[stage].append(fit_param[1])
          #if stage == "post-encapsulation":
          #  module_noise_map[hybrid_local_id]["SSA"][chip_id].append(fit_param[1])

        #for mpa
        chip_mpa = []
        if stage == "pre-assembly":
          mpa_id = chip_id + chip_id*hybrid_local_id + 1
          noise_file = parseCSV(f'results/OT_ModuleTest_Dobby_MaPSA/mpa_test_35494_002_PSP_MAINL_chip{mpa_id}.csv')
          for line in noise_file:
            ch, noise = int(line["channel"]), float(line["noise"])
            mpa_noise_array[stage].append(noise/sqrt(2))
        else:  
          h_scurve_mpa = f_noise.Get(f'Detector/Board_{board_id}/OpticalGroup_{optical_group_id}/Hybrid_{hybrid_id}/MPA_{mpa_id}/D_B({board_id})_O({optical_group_id})_H({hybrid_id})_SCurve_Chip({mpa_id})')
          if h_scurve_mpa == None:
            continue
          for ch_id in range(0, h_scurve_mpa.GetNbinsX()):
            x_array, y_array = [], []
            for th in range(0, h_scurve_mpa.GetNbinsY()):
              x_array.append(th) 
              y_array.append(h_scurve_mpa.GetBinContent(ch_id, th))
            fit_param, cov = optimize.curve_fit(fit_func, np.array(x_array), np.array(y_array), p0=[200, 3], maxfev=10000)
            mpa_noise_array[stage].append(fit_param[1])
            #if stage == "post-encapsulation":
            #  module_noise_map[hybrid_local_id]["MPA"][chip_id].append(fit_param[1])

  #fig0, ax0 = plt.subplots()
  #plt.tight_layout()
  #n_mpa_row, n_mpa_col = 16, 120
  #n_mpa_ch = n_mpa_col * n_mpa_row
  #for hybrid_id in range(0,1):
  #  for chip_id in range(0,1):
  #    mpa_cols, mpa_rows, mpa_ch = [], [], []
  #    for ch_id in range(0, n_mpa_ch):
  #      mpa_ch.append(ch_id)
  #      mpa_col = ch_id%120
  #      mpa_row = int(ch_id/120)
  #      mpa_cols.append(mpa_col)
  #      mpa_rows.append(mpa_row)
  #    print(len(mpa_ch), len(module_noise_map[hybrid_id]["MPA"][chip_id]))
  #    ax0.hist2d(mpa_ch, mpa_ch, bins=[len(mpa_cols), len(mpa_rows)], weights=module_noise_map[hybrid_id]["MPA"][chip_id], cmap=plt.cm.jet)
  #plt.savefig("./plots/noise_mpa.pdf", bbox_inches="tight")


  ssa_thdac, mpa_thdac = 250, 94

  fig1, ax1 = plt.subplots()
  plt.tight_layout()

  #ssa
  ax11 = ax1.twiny()
  ax11.set_xlabel(r"Channel Noise ($e^{-}$)", fontsize=16)
  ax11.set_xlim(0,8*ssa_thdac)
  #ax11.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
  ax11.set_box_aspect(1)

  ax1.hist(ssa_noise_array["pre-assembly"], bins=40, range=(0,10), density=True, histtype='step', color='darkgrey', linewidth=1, label='PreAs', zorder=3)
  ax1.hist(ssa_noise_array["pre-encapsulation"], bins=40, range=(0,10), density=True, histtype='step', color='steelblue', linewidth=1, label='PreEn', zorder=3)
  ax1.hist(ssa_noise_array["post-encapsulation"], bins=40, range=(0,10), density=True, histtype='step', color='navy', linewidth=1, label='PostEn', zorder=3)
  ax1.set_xlabel('Channel Noise (ThDAC)', fontsize=16)
  ax1.set_ylabel('Entries', fontsize=16)
  ax1.grid(zorder=0, alpha=0.5)
  ax1.set_xlim(0,8)
  ax1.set_ylim(0,2)
  ax1.xaxis.set_ticks(np.arange(0,8,2))
  ax1.yaxis.set_ticks(np.arange(0,2,0.2))
  ax1.legend(loc='upper right', ncol=3, columnspacing=1, fontsize=16, bbox_to_anchor=(1.04, 1.28))
  ax1.set_box_aspect(1)
  plt.savefig("./plots/noise_assembly_ssa.pdf", bbox_inches="tight")


  #mpa
  fig2, ax2 = plt.subplots()
  plt.tight_layout()

  ax22 = ax2.twiny()
  ax22.set_xlabel(r"Channel Noise ($e^{-}$)", fontsize=16)
  ax22.set_xlim(0, 500)
  #ax22.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
  ax22.set_box_aspect(1)

  ax2.hist(mpa_noise_array["pre-assembly"], bins=40, range=(0,10), density=True, histtype='step', color='darkgrey', linewidth=1, label='PreAs', zorder=3)
  ax2.hist(mpa_noise_array["pre-encapsulation"], bins=40, range=(0,10), density=True, histtype='step', color='steelblue', linewidth=1, label='PreEn', zorder=3)
  ax2.hist(mpa_noise_array["post-encapsulation"], bins=40, range=(0,10), density=True, histtype='step', color='navy', linewidth=1, label='PostEn', zorder=3)
  ax2.set_xlabel('Channel Noise (ThDAC)', fontsize=16)
  ax2.set_ylabel('Entries', fontsize=16)
  ax2.grid(zorder=0, alpha=0.5)
  ax2.set_xlim(0,8)
  ax2.set_ylim(0,2)
  ax2.xaxis.set_ticks(np.arange(0,8,2))
  ax2.yaxis.set_ticks(np.arange(0,2,0.2))
  ax2.set_box_aspect(1)

  ax2.legend(loc='upper right', ncol=3, columnspacing=1, fontsize=16, bbox_to_anchor=(1.04, 1.28))
  plt.savefig("./plots/noise_assembly_mpa.pdf", bbox_inches="tight")
       
if __name__ == "__main__":
  sys.exit(main())



