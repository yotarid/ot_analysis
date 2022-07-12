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

  skipSSA = []
  if args.skipSSA : 
    skipSSA = list(map(int, args.skipSSA.split(",")))

  skipMPA = []
  if args.skipMPA : 
    skipMPA = list(map(int, args.skipSSA.split(",")))

  th_unit = "[Th_DAC]"
  cal_unit = "[Cal_DAC]"
  x_range = 255
  thDACtoEl_mpa, calDACtoEl_mpa = 1, 1
  thDACtoEl_ssa, calDACtoEl_ssa = 1, 1
  if args.electron :
    x_range = 65e3
    th_unit = "[e-]"
    cal_unit = "[e-]"
    thDACtoEl_mpa, calDACtoEl_mpa = 94, 220
    thDACtoEl_ssa, calDACtoEl_ssa = 250, 243
    fig_name += "_Electron"
  else :
    fig_name += "_DAC"

  ssa_file_paths = ["Results/FEH_2S_DESY_FullModule_AllSSA_HV300_TP50_271021_Run571/Hybrid.root",
		 	              "Results/FEH_2S_DESY_FullModule_AllSSA_HV300_TP70_271021_Run572/Hybrid.root",
		 	              "Results/FEH_2S_DESY_FullModule_AllSSA_HV300_TP90_271021_Run573/Hybrid.root",
		 	              "Results/FEH_2S_DESY_FullModule_AllSSA_HV300_TP150_271021_Run574/Hybrid.root",
		 	              "Results/FEH_2S_DESY_FullModule_AllSSA_HV300_TP250_271021_Run575/Hybrid.root"]
  ssa_cal_dac = np.array([50,70,90,150,250]) * calDACtoEl_ssa

  mpa_file_paths = ["Results/FEH_2S_DESY_FullModule_AllMPA_HV300_TP50_011121_Run620/Hybrid.root",
		 	              "Results/FEH_2S_DESY_FullModule_AllMPA_Tuned_HV300_TP70_311021_Run617/Hybrid.root"]
  mpa_cal_dac = np.array([50,70]) * calDACtoEl_mpa
  fig_name = "DESY26_2_InjectionScan"


  hybridIds = [0,1]
  chipIds = [0,1,2,3,4,5,6,7]

  ssaPulsePeak = {0:[], 1:[]}
  ssaPulsePeakError = {0:[], 1:[]}
  mpaPulsePeak = {0:[], 1 : []}
  mpaPulsePeakError = {0:[], 1:[]}

  for file_idx, file_path in enumerate(ssa_file_paths) : 
    file = TFile.Open(file_path, 'READ')
    hybridPulsePeak = []
    hybridPulsePeakError = []
    cal_DAC = ssa_cal_dac[file_idx]
    for hybridId in hybridIds :
      chipPulsePeak = []
      chipPulsePeakError = []
      for chipId in chipIds :
        if chipId in skipSSA : continue
        pulsePeakHist = file.Get(f'Detector/Board_0/OpticalGroup_0/Hybrid_{hybridId}/SSA_{chipId}/D_B(0)_O(0)_H({hybridId})_PedestalDistribution_Chip({chipId})')
        pulsePeak = pulsePeakHist.GetMean()
        pulsePeakError = pulsePeakHist.GetStdDev()
        print(f'SSA{chipId}, Cal_DAC = {cal_DAC}, pulse peak = {pulsePeak}')
        chipPulsePeak.append(pulsePeak)
        chipPulsePeakError.append(pulsePeakError)
      ssaPulsePeak[hybridId].append(np.array(chipPulsePeak).mean() * thDACtoEl_ssa)
      ssaPulsePeakError[hybridId].append(np.array(chipPulsePeakError).mean() * thDACtoEl_ssa)

  for file_idx, file_path in enumerate(mpa_file_paths) : 
    file = TFile.Open(file_path, 'READ')
    hybridPulsePeak = []
    hybridPulsePeakError = []
    cal_DAC = mpa_cal_dac[file_idx]
    for hybridId in hybridIds :
      chipPulsePeak = []
      chipPulsePeakError = []
      for chipId in chipIds :
        if chipId in skipMPA : continue
        pulsePeakHist = file.Get(f'Detector/Board_0/OpticalGroup_0/Hybrid_{hybridId}/MPA_{chipId}/D_B(0)_O(0)_H({hybridId})_PedestalDistribution_Chip({chipId})')
        pulsePeak = pulsePeakHist.GetMean()
        pulsePeakError = pulsePeakHist.GetStdDev()
        print(f'MPA{chipId}, Cal_DAC = {cal_DAC}, pulse peak = {pulsePeak}')
        chipPulsePeak.append(pulsePeak)
        chipPulsePeakError.append(pulsePeakError)
      mpaPulsePeak[hybridId].append(np.array(chipPulsePeak).mean() * thDACtoEl_mpa)
      mpaPulsePeakError[hybridId].append(np.array(chipPulsePeakError).mean() * thDACtoEl_mpa)
  

  x_fit = np.linspace(0, x_range)

  h0_mpaPulsePeak_coef =  np.polyfit(mpa_cal_dac, mpaPulsePeak[0], 1)
  h0_mpaPulsePeak_poly = np.poly1d(h0_mpaPulsePeak_coef)
  h0_mpaPulsePeak_fit = h0_mpaPulsePeak_poly(x_fit)

  h1_mpaPulsePeak_coef =  np.polyfit(mpa_cal_dac, mpaPulsePeak[1], 1)
  h1_mpaPulsePeak_poly = np.poly1d(h1_mpaPulsePeak_coef)
  h1_mpaPulsePeak_fit = h1_mpaPulsePeak_poly(x_fit)

  mpa_baseline = (h0_mpaPulsePeak_fit[0] + h1_mpaPulsePeak_fit[0])/2
  print(f'MPA-L baseline = {mpa_baseline} {th_unit}')

  h0_ssaPulsePeak_coef =  np.polyfit(ssa_cal_dac, ssaPulsePeak[0], 1)
  h0_ssaPulsePeak_poly = np.poly1d(h0_ssaPulsePeak_coef)
  h0_ssaPulsePeak_fit = h0_ssaPulsePeak_poly(x_fit)

  h1_ssaPulsePeak_coef =  np.polyfit(ssa_cal_dac, ssaPulsePeak[1], 1)
  h1_ssaPulsePeak_poly = np.poly1d(h1_ssaPulsePeak_coef)
  h1_ssaPulsePeak_fit = h0_ssaPulsePeak_poly(x_fit)

  ssa_baseline = (h0_ssaPulsePeak_fit[0] + h1_ssaPulsePeak_fit[0])/2
  print(f'FEH-L baseline = {ssa_baseline} {th_unit}')

  plt.plot(mpa_cal_dac, np.array(mpaPulsePeak[0]) - h0_mpaPulsePeak_fit[0], linestyle="None", marker='s', markersize=5, color='tomato', label='MPA-R')
  plt.plot(x_fit, np.array(h0_mpaPulsePeak_fit) - h0_mpaPulsePeak_fit[0], linestyle='dashed', marker='None', linewidth=2, color='tomato')

  plt.plot(mpa_cal_dac, np.array(mpaPulsePeak[1]) - h1_mpaPulsePeak_fit[0], linestyle="None", marker='s', markersize=5, color='darkred', label='MPA-L')
  plt.plot(x_fit, np.array(h1_mpaPulsePeak_fit) - h1_mpaPulsePeak_fit[0], linestyle='dashed', marker='None', linewidth=2, color='darkred')

  plt.plot(ssa_cal_dac, np.array(ssaPulsePeak[0]) - h0_ssaPulsePeak_fit[0], linestyle="None", marker='o', markersize=5, color='blue', label='FEH-R')
  plt.plot(x_fit, np.array(h0_ssaPulsePeak_fit) - h0_ssaPulsePeak_fit[0], linestyle='dashed', marker='None', linewidth=2, color='blue')

  plt.plot(ssa_cal_dac, np.array(ssaPulsePeak[1]) - h1_ssaPulsePeak_fit[0], linestyle="None", marker='o', markersize=5, color='navy', label='FEH-L')
  plt.plot(x_fit, np.array(h1_ssaPulsePeak_fit) - h1_ssaPulsePeak_fit[0], linestyle='dashed', marker='None', linewidth=2, color='navy')

  plt.xlabel(f'Injected charge {cal_unit}')
  plt.ylabel(f'Pulse peak {th_unit}')
  plt.title("DESY26_2 Charge injection scan @Bias(300V)")
  plt.legend(loc="upper left", fontsize=12)
  plt.grid()
  plt.savefig("./plots/" + fig_name)
  # plt.show()
        
if __name__ == "__main__":
  sys.exit(main())
    
    

