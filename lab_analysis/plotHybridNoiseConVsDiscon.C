#include "TGraphErrors.h"
#include "TFile.h"
#include "TMultiGraph.h"
#include "TLegend.h"

#include <vector>
#include <string>
#include <iostream>
#include <map>

void plotHybridNoiseConVsDiscon()
{
  std::vector<std::string> filePathVector {
    "Results/ps_module_test_BothFEH_OnlySSA_10V_300V_run24/ps_module_result.root",
    "Results/ps_module_test_OnlyFEHL_DisconnectedFEHR_OnlySSA_10V_300V_run26/ps_module_result.root"
  };

  std::vector<std::string> configuration = {"FEH-R Connected", "FEH-R Disconnected"};

  std::map<std::string, std::vector<double>> ssaNoise { 
    {"FEH-R Connected" , std::vector<double>(8)},
    {"FEH-R Disconnected" , std::vector<double>(8)}};

  std::map<std::string, std::vector<double>> ssaNoiseError { 
    {"FEH-R Connected" , std::vector<double>(8)},
    {"FEH-R Disconnected" , std::vector<double>(8)}};

  std::map<std::string, double> hybridNoise {
    {"FEH-R Connected", 0},
    {"FEH-R Disconnected", 0}
  };

  std::map<std::string, double> hybridNoiseError {
    {"FEH-R Connected", 0},
    {"FEH-R Disconnected", 0}
  };

  std::vector<double> errorX = {0.5, 0.5, 0.5, 0.5, 0.5};
  //std::vector<double> errorX = {0, 0, 0, 0, 0};
  //std::vector<double> SSAchipIds = {0, 1, 2, 3, 4, 5, 6, 7};

  bool withSSA = true;
  std::vector<int> chipIdVector = {0, 1, 2, 4, 5, 6, 7}; 
  std::vector<int> hybridIdVector = {0, 1}; 
  double calDACtoEl = 243, thDACtoEl = 250;

  for(size_t pathIdx=0; pathIdx < filePathVector.size(); pathIdx++) 
  {
    TFile* file = TFile::Open(filePathVector[pathIdx].c_str(), "READ"); 
    std::string config = configuration[pathIdx];
    
    for(auto hybridId : hybridIdVector)
    {
      if(hybridId == 0) continue; //skip right hybrid
      TH1F* hybridNoiseDistribution = (TH1F*)file->Get(Form("Detector/Board_0/OpticalGroup_0/Hybrid_%i/D_B(0)_O(0)_HybridNoiseDistribution_Hybrid(%i)", hybridId, hybridId));
      double hybridMeanNoise = hybridNoiseDistribution->GetMean();
      double hybridMeanNoiseError = hybridNoiseDistribution->GetStdDev();
      //hybridNoise[hybridId].push_back(hybridMeanNoise*calDACtoEl);
      hybridNoise[config] = hybridMeanNoise;
      //hybridNoiseError[hybridId].push_back(hybridMeanNoiseError*calDACtoEl);
      hybridNoiseError[config] = hybridMeanNoiseError;
      std::cout << "Hyrid" << +hybridId << ", Mean Noise " << +hybridMeanNoise << std::endl;
      std::cout << "Hyrid" << +hybridId << ", Mean Noise Error " << +hybridMeanNoiseError << std::endl;
      //
      for(auto chipId : chipIdVector)
      {
        std::cout << "---------------------------------------------------------------" << std::endl;
        double ssaMeanNoise = 0;
        double ssaMeanNoiseError = 0;
        auto histPath = Form("Detector/Board_0/OpticalGroup_0/Hybrid_%i/SSA_%i/D_B(0)_O(0)_H(%i)_NoiseDistribution_Chip(%i)", hybridId, (int)chipId, hybridId, (int)chipId);
        std::cout << histPath << "\n" << std::endl;
        TH1F* chipNoiseDistribution = (TH1F*)file->Get(histPath);
        if(chipNoiseDistribution != nullptr) 
        {
          ssaMeanNoise = chipNoiseDistribution->GetMean();
          ssaMeanNoiseError = chipNoiseDistribution->GetStdDev();
          std::cout << "configuration  " << config << " , hybridId = " << +hybridId << " , chipId = " << +chipId << " , " << ((withSSA == true) ? "SSA" : "MPA") << std::endl;
        }
        //ssaNoise[config][hybridId][chipId] =  ssaMeanNoise*calDACtoEl; 
        ssaNoise[config][chipId] =  ssaMeanNoise; 
        //ssaNoiseError[config][hybridId][chipId] =  ssaMeanNoiseError*calDACtoEl; 
        ssaNoiseError[config][chipId] =  ssaMeanNoiseError; 
      }
    }
  }

  std::vector<double> SSAchipIds = {0, 1, 2, 3, 4, 5, 6, 7};
  errorX = {0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5};
  std::vector<int> markerColors = {2,1};

  std::string name = "mg_ssaNoise_hybrid1";
  TMultiGraph* mg_ssaNoise = new TMultiGraph(name.c_str(), "");
  TLegend* leg_ssaNoise = new TLegend(0.15, 0.15, 0.4, 0.4);
  for(int vIdx = 0; vIdx < configuration.size(); vIdx++) 
  {
    auto config = configuration[vIdx];
    TGraphErrors* h_ssaNoise = new TGraphErrors(8, SSAchipIds.data(), ssaNoise[config].data(), errorX.data(), ssaNoiseError[config].data());
    h_ssaNoise->SetMarkerStyle(22);
    h_ssaNoise->SetMarkerSize(1);
    h_ssaNoise->SetMarkerColor(markerColors[vIdx]);
    h_ssaNoise->SetDrawOption("AP");
    mg_ssaNoise->Add(h_ssaNoise);
    leg_ssaNoise->AddEntry(h_ssaNoise, configuration[vIdx].c_str());
  }
  std::string title = "DESY26_2 - FEH-L - Noise vs FEH-R @300V";
  mg_ssaNoise->SetTitle(title.c_str());
  mg_ssaNoise->GetXaxis()->SetTitle("Chip Id");
  mg_ssaNoise->GetXaxis()->SetLimits(-0.5, 7.5);
  //mg_ssaNoise->GetYaxis()->SetTitle("Noise [ e^{-} ]");
  mg_ssaNoise->GetYaxis()->SetTitle("Noise [Th_DAC]");
  mg_ssaNoise->GetYaxis()->SetMaxDigits(3);
  //mg_ssaNoise->GetYaxis()->SetRangeUser(0, 2000);
  mg_ssaNoise->GetYaxis()->SetRangeUser(0, 8);
  mg_ssaNoise->Draw("AP");
  leg_ssaNoise->Draw();
}
