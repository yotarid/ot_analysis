from ROOT import TFile
import matplotlib.pyplot as plt
import csv, sys, argparse
import numpy as np

def main():
  parser = argparse.ArgumentParser(description="Module Noise")
  parser.add_argument('-electron', help="Noise in units of electrons", action="store_true")
  # parser.add_argument('-skipSSA', help="List of SSA Ids to skip")
  # parser.add_argument('-skipMPA', help="List of MPA Ids to skip")

  #2.6mm in lab
  # mpa_file_path = "./Results/FEH_2S_DESY_FullModule_AllMPA_Tuned_HV300_TP70_311021_Run617/Hybrid.root"
  # ssa_file_path = "./Results/FEH_2S_DESY_FullModule_AllSSA_HV300_TP70_271021_Run572/Hybrid.root"
  # title = "DESY26_2 Noise in lab @Bias(300V)"
  # fig_name = "DESY26_2_Lab_Noise"

  #4mm in lab
  # mpa_file_path = "./Results/FEH_2S_DESY_FullModule_4mm_AllMPA_PostEncap_111121_Run673/Hybrid.root" 
  # ssa_file_path = "./Results/FEH_2S_DESY_FullModule_4mm_AllSSA_PostEncap_TP70_141121_Run691/Hybrid.root" 
  # title = "DESY40_3 Noise in lab @Bias(300V)"
  # fig_name = "DESY40_3_Lab_Noise"

  #2.6mm in testbeam
  # mpa_file_path = "./Results/FEH_2S_DESY_FullModule_26mm_AllMPA_TP70_TestBeam_171121_Run746/Hybrid.root"
  # ssa_file_path = "./Results/FEH_2S_DESY_FullModule_26mm_AllSSA_TP70_TestBeam_171121_Run745/Hybrid.root"
  # title = "DESY26_2 Noise in testbeam @Bias(300V)"
  # fig_name = "DESY26_2_TestBeam_Noise"

  #2.6mm in testbeam
  mpa_file_path = ""
  ssa_file_path = "./Results/ps_module_test_DESY26_2_OnlySSA_10V_300V_MCground_15022022_run28/ps_module_result.root"
  title = "DESY26_2 Noise in lab @Bias(300V) with grounded module carrier"
  fig_name = "DESY26_2_Lab_Noise_ModuleCarrierGrounded"



  args = parser.parse_args()
  ###
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
  if args.electron :
    unit = "[e-]"
    thDACtoEl_mpa, calDACtoEl_mpa = 94, 220
    thDACtoEl_ssa, calDACtoEl_ssa = 250, 243
    fig_name += "_Electron"
  else :
    fig_name += "_DAC"

  hybridIds = [0,1]
  chipIds = [0,1,2,3,4,5,6,7]

  ssaNoise = {0 : [None]*8, 1 : [None]*8}
  ssaNoiseError = {0 : [None]*8, 1 : [None]*8}

  mpaNoise = {0 : [None]*8, 1 : [None]*8}
  mpaNoiseError = {0 : [None]*8, 1 : [None]*8}

  xerr = [0.5]*8

  mpa_file = TFile.Open(mpa_file_path, "READ")
  for hybridId in hybridIds :
    hybridNoiseDist = mpa_file.Get(f'Detector/Board_0/OpticalGroup_0/Hybrid_{hybridId}/D_B(0)_O(0)_HybridNoiseDistribution_Hybrid({hybridId})')
    for chipId in chipIds :
      meanNoise, meanNoiseError = 0, 0
      chipNoiseDist = mpa_file.Get(f'Detector/Board_0/OpticalGroup_0/Hybrid_{hybridId}/MPA_{chipId}/D_B(0)_O(0)_H({hybridId})_NoiseDistribution_Chip({chipId})')
      if chipNoiseDist :
        meanNoise = chipNoiseDist.GetMean()
        meanNoiseError = chipNoiseDist.GetStdDev()
      mpaNoise[hybridId][chipId] = meanNoise * thDACtoEl_mpa
      mpaNoiseError[hybridId][chipId] = meanNoiseError * thDACtoEl_mpa
  
  ssa_file = TFile.Open(ssa_file_path, "READ")
  for hybridId in hybridIds :
    hybridNoiseDist = ssa_file.Get(f'Detector/Board_0/OpticalGroup_0/Hybrid_{hybridId}/D_B(0)_O(0)_HybridNoiseDistribution_Hybrid({hybridId})')
    for chipId in chipIds:
      meanNoise, meanNoiseError = 0, 0
      chipNoiseDist = ssa_file.Get(f'Detector/Board_0/OpticalGroup_0/Hybrid_{hybridId}/SSA_{chipId}/D_B(0)_O(0)_H({hybridId})_NoiseDistribution_Chip({chipId})')
      if chipNoiseDist :
        meanNoise = chipNoiseDist.GetMean()
        meanNoiseError = chipNoiseDist.GetStdDev()
      ssaNoise[hybridId][chipId] = meanNoise * thDACtoEl_ssa
      ssaNoiseError[hybridId][chipId] = meanNoiseError * thDACtoEl_ssa

  ssa_h0 = plt.errorbar(chipIds, ssaNoise[0], ssaNoiseError[0], xerr, linestyle='None', marker='o', markersize=5, color='blue', label='FEH-R')
  ssa_h1 = plt.errorbar(chipIds, ssaNoise[1], ssaNoiseError[1], xerr, linestyle='None', marker='o', markersize=5, color='navy', label='FEH-L')
  mpa_h0 = plt.errorbar(chipIds, mpaNoise[0], mpaNoiseError[0], xerr, linestyle='None', marker='s', markersize=5, color='tomato', label='MPA-R')
  mpa_h1 = plt.errorbar(chipIds, mpaNoise[1], mpaNoiseError[1], xerr, linestyle='None', marker='s', markersize=5, color='darkred', label='MPA-L')

  plt.xlabel("Chip Id")
  plt.ylabel(f'Noise {unit}')
  plt.title(title)
  plt.legend(loc="upper left", fontsize=8)
  plt.grid()
  # plt.show()
  plt.savefig("./plots/" + fig_name)
  
if __name__ == "__main__":
  sys.exit(main())
  
