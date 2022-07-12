from ROOT import TFile
import matplotlib.pyplot as plt
import csv, sys, argparse
import numpy as np

def main():
  parser = argparse.ArgumentParser(description="Module Noise")
  parser.add_argument('-electron', help="Noise in units of electrons", action="store_true")
  parser.add_argument('-skipSSA', help="List of SSA Ids to skip")
  parser.add_argument('-skipMPA', help="List of MPA Ids to skip")

  args = parser.parse_args()

  ###
  # skipped_ssa = []
  # if args.skipSSA :
  #   skipped_ssa = list(map(int, args.skipSSA.split(",")))
  # ###
  # skipped_mpa = []
  # if args.skipMPA :
  #   skipped_mpa = list(map(int, args.skipMPA.split(",")))
  # ##
  unit = "[Th_DAC]"
  thDACtoEl_mpa, calDACtoEl_mpa = 1, 1
  thDACtoEl_ssa, calDACtoEl_ssa = 1, 1
  fig_name_term = ""
  if args.electron :
    unit = "[e-]"
    thDACtoEl_mpa, calDACtoEl_mpa = 94, 220
    thDACtoEl_ssa, calDACtoEl_ssa = 250, 243
    fig_name_term = "_Electron"
  else :
    fig_name_term = "_DAC"

  #2.6mm noise vs voltage scan
  ssa_file_paths = ["./Results/ps_module_test_OnlySSA_7V_300V_run9/ps_module_result.root", 
                    "./Results/ps_module_test_OnlySSA_8V_300V_run2/ps_module_result.root", 
                    "./Results/ps_module_test_OnlySSA_9V_300V_run3/ps_module_result.root", 
                    "./Results/ps_module_test_OnlySSA_10V_300V_run4/ps_module_result.root", 
                    "./Results/ps_module_test_OnlySSA_11V_300V_run5/ps_module_result.root"]

  hybridIds = [0,1]
  chipIds = [0,1,2,3,4,5,6,7]
  voltages = [7,8,9,10,11]

  ssaNoise = { 7 : {0:[None]*8 , 1:[None]*8},
                  8 : {0:[None]*8 , 1:[None]*8},
                  9 : {0:[None]*8 , 1:[None]*8},
                  10 : {0:[None]*8 , 1:[None]*8},
                  11 : {0:[None]*8 , 1:[None]*8}}
  ssaNoiseError = { 7 : {0:[None]*8 , 1:[None]*8},
                  8 : {0:[None]*8 , 1:[None]*8},
                  9 : {0:[None]*8 , 1:[None]*8},
                  10 : {0:[None]*8 , 1:[None]*8},
                  11 : {0:[None]*8 , 1:[None]*8}}

  xerr = [0.5]*8

  for file_idx, ssa_file_path in enumerate(ssa_file_paths) :
    ssa_file = TFile.Open(ssa_file_path, "READ")
    voltage = voltages[file_idx]
    for hybridId in hybridIds :
      hybridNoiseDist = ssa_file.Get(f'Detector/Board_0/OpticalGroup_0/Hybrid_{hybridId}/D_B(0)_O(0)_HybridNoiseDistribution_Hybrid({hybridId})')
      for chipId in chipIds:
        meanNoise, meanNoiseError = 0, 0
        chipNoiseDist = ssa_file.Get(f'Detector/Board_0/OpticalGroup_0/Hybrid_{hybridId}/SSA_{chipId}/D_B(0)_O(0)_H({hybridId})_NoiseDistribution_Chip({chipId})')
        if chipNoiseDist :
          meanNoise = chipNoiseDist.GetMean()
          meanNoiseError = chipNoiseDist.GetStdDev()
        ssaNoise[voltage][hybridId][chipId] = meanNoise * thDACtoEl_ssa
        ssaNoiseError[voltage][hybridId][chipId] = meanNoiseError * thDACtoEl_ssa

  marker_colors = ['green', 'blue', 'orange', 'red', 'black']
  for hybridId in hybridIds :
    plt.figure(hybridId) 
    for v_idx, voltage in enumerate(voltages) : 
      label = str(voltage) + "V"
      plt.errorbar(chipIds, ssaNoise[voltage][hybridId], ssaNoiseError[voltage][hybridId], xerr, linestyle='None', marker='o', markersize=5, color=marker_colors[v_idx], label=label)
    plt.xlabel("Chip Id")
    # plt.ylim(500,2000)
    plt.ylabel(f'Noise {unit}')
    plt.legend(loc="lower left", fontsize=8)
    plt.grid()
    if hybridId == 0 :
      plt.title("DESY26_2 FEH-R Noise vs LV @Bias(300V)")
      plt.savefig("./plots/DESY26_2_FEHR_vs_LV" + fig_name_term)
    else :
      plt.title("DESY26_2 FEH-L Noise vs LV @Bias(300V)")
      plt.savefig("./plots/DESY26_2_FEHL_vs_LV" + fig_name_term)

if __name__ == "__main__":
  sys.exit(main())
