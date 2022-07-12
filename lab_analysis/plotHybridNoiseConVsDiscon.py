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

  ssa_file_paths = ["Results/ps_module_test_BothFEH_OnlySSA_10V_300V_run24/ps_module_result.root",
                    "Results/ps_module_test_OnlyFEHL_DisconnectedFEHR_OnlySSA_10V_300V_run26/ps_module_result.root"]

  hybridIds = [0,1]
  chipIds = [0,1,2,3,4,5,6,7]
  voltages = [7,8,9,10,11]
  configs = ["FEH-R Connected", "FEH-R Disconnected"]

  ssaNoise = {"FEH-R Connected" : [None]*8,
              "FEH-R Disconnected" : [None]*8}

  ssaNoiseError = {"FEH-R Connected" : [None]*8,
                   "FEH-R Disconnected" : [None]*8}
              
  xerr = [0.5]*8

  for file_idx, ssa_file_path in enumerate(ssa_file_paths) :
    ssa_file = TFile.Open(ssa_file_path, "READ")
    config = configs[file_idx]
    for hybridId in hybridIds :
      hybridNoiseDist = ssa_file.Get(f'Detector/Board_0/OpticalGroup_0/Hybrid_{hybridId}/D_B(0)_O(0)_HybridNoiseDistribution_Hybrid({hybridId})')
      for chipId in chipIds:
        meanNoise, meanNoiseError = 0, 0
        chipNoiseDist = ssa_file.Get(f'Detector/Board_0/OpticalGroup_0/Hybrid_{hybridId}/SSA_{chipId}/D_B(0)_O(0)_H({hybridId})_NoiseDistribution_Chip({chipId})')
        if chipNoiseDist :
          meanNoise = chipNoiseDist.GetMean()
          meanNoiseError = chipNoiseDist.GetStdDev()
        ssaNoise[config][chipId] = meanNoise * thDACtoEl_ssa
        ssaNoiseError[config][chipId] = meanNoiseError * thDACtoEl_ssa

  plt.errorbar(chipIds, ssaNoise["FEH-R Connected"], ssaNoiseError["FEH-R Connected"], xerr, linestyle='None', marker='o', markersize=5, color="blue", label="FEH-R Connected" ) 
  plt.errorbar(chipIds, ssaNoise["FEH-R Disconnected"], ssaNoiseError["FEH-R Disconnected"], xerr, linestyle='None', marker='o', markersize=5, color="red", label="FEH-R Disconnected" ) 

  plt.title("DESY26_2 FEH-L - Noise vs FEH-R @Bias(300V)")
  plt.xlabel("Chip Id")
  plt.ylabel(f'Noise {unit}')
  plt.legend(loc="upper left", fontsize=10)
  plt.grid()
  plt.savefig("./plots/DESY26_2_Noise_FEHL_vs_FEHR" + fig_name_term)

if __name__ == "__main__":
  sys.exit(main())