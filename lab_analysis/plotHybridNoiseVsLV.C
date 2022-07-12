#include "TGraphErrors.h"
#include "TFile.h"
#include "TMultiGraph.h"
#include "TLegend.h"

#include <vector>
#include <string>
#include <iostream>
#include <map>


void plotHybridNoiseVsLV()
{
  //2.6mm noise vs voltage scan
  std::vector<std::string> filePathVector{
    "./Results/ps_module_test_OnlySSA_7V_300V_run9/ps_module_result.root", 
    "./Results/ps_module_test_OnlySSA_8V_300V_run2/ps_module_result.root", 
    "./Results/ps_module_test_OnlySSA_9V_300V_run3/ps_module_result.root", 
    "./Results/ps_module_test_OnlySSA_10V_300V_run4/ps_module_result.root", 
    "./Results/ps_module_test_OnlySSA_11V_300V_run5/ps_module_result.root", 
  };

  std::vector<double> voltages = {7,8,9,10,11};

  std::map<int, std::map<int, std::vector<double>>> ssaNoise { 
    {7 , {{0, std::vector<double>(8)}, {1, std::vector<double>(8)}}},
    {8 , {{0, std::vector<double>(8)}, {1, std::vector<double>(8)}}},
    {9 , {{0, std::vector<double>(8)}, {1, std::vector<double>(8)}}},
    {10 , {{0, std::vector<double>(8)}, {1, std::vector<double>(8)}}},
    {11 , {{0, std::vector<double>(8)}, {1, std::vector<double>(8)}}}};

  std::map<int, std::map<int, std::vector<double>>> ssaNoiseError { 
    {7 , {{0, std::vector<double>(8)}, {1, std::vector<double>(8)}}},
    {8 , {{0, std::vector<double>(8)}, {1, std::vector<double>(8)}}},
    {9 , {{0, std::vector<double>(8)}, {1, std::vector<double>(8)}}},
    {10 , {{0, std::vector<double>(8)}, {1, std::vector<double>(8)}}},
    {11 , {{0, std::vector<double>(8)}, {1, std::vector<double>(8)}}}};

  std::map<int, std::vector<double>> hybridNoise {
    {0, std::vector<double>{}},
    {1, std::vector<double>{}}
  };

  std::map<int, std::vector<double>> hybridNoiseError {
    {0, std::vector<double>{}},
    {1, std::vector<double>{}}
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
    int voltage = voltages[pathIdx];
    
    for(auto hybridId : hybridIdVector)
    {
      TH1F* hybridNoiseDistribution = (TH1F*)file->Get(Form("Detector/Board_0/OpticalGroup_0/Hybrid_%i/D_B(0)_O(0)_HybridNoiseDistribution_Hybrid(%i)", hybridId, hybridId));
      double hybridMeanNoise = hybridNoiseDistribution->GetMean();
      double hybridMeanNoiseError = hybridNoiseDistribution->GetStdDev();
      //hybridNoise[hybridId].push_back(hybridMeanNoise*calDACtoEl);
      hybridNoise[hybridId].push_back(hybridMeanNoise);
      //hybridNoiseError[hybridId].push_back(hybridMeanNoiseError*calDACtoEl);
      hybridNoiseError[hybridId].push_back(hybridMeanNoiseError);
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
          std::cout << "voltage " << +voltage << " , hybridId = " << +hybridId << " , chipId = " << +chipId << " , " << ((withSSA == true) ? "SSA" : "MPA") << std::endl;
        }
        //ssaNoise[voltage][hybridId][chipId] =  ssaMeanNoise*calDACtoEl; 
        ssaNoise[voltage][hybridId][chipId] =  ssaMeanNoise; 
        //ssaNoiseError[voltage][hybridId][chipId] =  ssaMeanNoiseError*calDACtoEl; 
        ssaNoiseError[voltage][hybridId][chipId] =  ssaMeanNoiseError; 
      }
    }
  }


  TMultiGraph* mg_HybridNoise = new TMultiGraph();
  TLegend* leg_HybridNoise = new TLegend(0.15, 0.15, 0.35, 0.3);

  TGraphErrors* h_hybrid0_Noise_Hybrid = new TGraphErrors(5, voltages.data(), hybridNoise[0].data(), errorX.data(), hybridNoiseError[0].data());
  h_hybrid0_Noise_Hybrid->SetMarkerStyle(21);
  h_hybrid0_Noise_Hybrid->SetMarkerSize(1);
  h_hybrid0_Noise_Hybrid->SetMarkerColor(4);
  h_hybrid0_Noise_Hybrid->SetDrawOption("AP");
  mg_HybridNoise->Add(h_hybrid0_Noise_Hybrid);
  leg_HybridNoise->AddEntry(h_hybrid0_Noise_Hybrid, "FEH-R (All SSA chips)");

  TGraphErrors* h_hybrid1_Noise_Hybrid = new TGraphErrors(5, voltages.data(), hybridNoise[1].data(), errorX.data(), hybridNoiseError[1].data());
  h_hybrid1_Noise_Hybrid->SetMarkerStyle(21);
  h_hybrid1_Noise_Hybrid->SetMarkerSize(1);
  h_hybrid1_Noise_Hybrid->SetMarkerColor(38);
  h_hybrid1_Noise_Hybrid->SetDrawOption("AP");
  mg_HybridNoise->Add(h_hybrid1_Noise_Hybrid);
  leg_HybridNoise->AddEntry(h_hybrid1_Noise_Hybrid, "FEH-L (All SSA chips)");

  mg_HybridNoise->SetTitle("DESY26_2 Noise vs LV @300V");
  mg_HybridNoise->GetXaxis()->SetTitle("Voltage [V]");
  mg_HybridNoise->GetXaxis()->SetLimits(6.5, 11.5);
  //mg_HybridNoise->GetYaxis()->SetTitle("Noise [ e^{-} ]");
  mg_HybridNoise->GetYaxis()->SetTitle("Noise [Th_DAC]");
  mg_HybridNoise->GetYaxis()->SetMaxDigits(3);
  //mg_HybridNoise->GetYaxis()->SetRangeUser(0, 2000);
  mg_HybridNoise->GetYaxis()->SetRangeUser(0, 8);
  mg_HybridNoise->Draw("AP");
  leg_HybridNoise->Draw();


  std::vector<double> hybridIds = {0, 1};
  std::vector<double> SSAchipIds = {0, 1, 2, 3, 4, 5, 6, 7};
  errorX = {0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5};
  std::vector<int> markerColors = {1,2,4,6,8};
  TCanvas* c_ssaNoise = new TCanvas();
  c_ssaNoise->Divide(2,1);

  for(auto hybridId : hybridIds)
  {
    c_ssaNoise->cd(2 - hybridId);
    std::string name = "mg_ssaNoiseVsLV_hybrid" + std::to_string(hybridId);
    TMultiGraph* mg_ssaNoise = new TMultiGraph(name.c_str(), "");
    TLegend* leg_ssaNoise = new TLegend(0.15, 0.15, 0.35, 0.35);
    for(int vIdx = 0; vIdx < voltages.size(); vIdx++) 
    {
      auto voltage = voltages[vIdx];
      TGraphErrors* h_ssaNoise = new TGraphErrors(8, SSAchipIds.data(), ssaNoise[voltage][hybridId].data(), errorX.data(), ssaNoiseError[voltage][hybridId].data());
      h_ssaNoise->SetMarkerStyle(22);
      h_ssaNoise->SetMarkerSize(1);
      h_ssaNoise->SetMarkerColor(markerColors[vIdx]);
      h_ssaNoise->SetDrawOption("AP");
      mg_ssaNoise->Add(h_ssaNoise);
      leg_ssaNoise->AddEntry(h_ssaNoise, Form("LV = %iV", (int)voltages[vIdx]));
    }
    std::string feh = ((hybridId == 0) ? "FEH-R" : "FEH-L");
    std::string title = "DESY26_2 - " +  feh + " - Noise vs LV @300V";
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
}


