#include "TCanvas.h"
#include "TFile.h"
#include "TF1.h"
#include "TH1F.h"
#include "TGraphErrors.h"
#include "TGraph.h"
#include "TMultiGraph.h"
#include "TLegend.h"

#include <string>
#include <map>
#include <vector>
#include <iostream>
#include <utility>

void plotIV()
{
  std::vector<float> rampUpVoltage = {0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200,
                                210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310, 320, 330, 340, 350, 360, 370, 380, 390, 400};

/*
  std::vector<float> DESY26_2_I_withVTRx = {3.24, 3.35, 3.40, 3.43, 3.46, 3.48, 3.50, 3.52, 3.54, 3.56, 3.58, 3.60, 3.62, 3.64, 3.66, 3.68, 3.70, 
                                            3.70, 3.70, 3.72, 3.72, 3.72, 3.74, 3.75, 3.76, 3.77, 3.78, 3.79, 3.79, 3.80, 3.80, 3.81, 3.81, 3.82, 3.83, 3.83, 3.84, 3.84, 3.85, 3.86, 3.87};
  
  std::vector<float> DESY26_2_I_withoutVTRx = {0.34, 0.43, 0.46, 0.49, 0.51, 0.53, 0.55, 0.57, 0.59, 0.61, 0.63, 0.65, 0.66, 0.68, 0.69, 0.70, 0.72, 
                                               0.73, 0.74, 0.75, 0.76, 0.77, 0.77, 0.78, 0.78, 0.79, 0.80, 0.80, 0.80, 0.80, 0.81, 0.81, 0.82, 0.82, 0.82, 0.83, 0.83, 0.84, 0.84, 0.85, 0.85};

*/

  std::vector<float> DESY40_3_I_withVTRx = {3.68, 3.90, 4.01, 4.07, 4.11, 4.16, 4.20, 4.26, 4.33, 4.36, 4.41, 4.47, 4.52, 4.56, 4.62, 4.67, 4.72, 4.76, 4.80, 4.82, 4.84, 4.90, 4.90, 4.91, 4.93, 4.95, 4.96, 4.96, 4.96, 4.99, 5.00, 5.01, 5.01, 5.02, 5.03, 5.06, 5.06, 5.06, 5.06, 5.06, 5.06};

  TMultiGraph* mg_DESY_IV = new TMultiGraph();
  TLegend* leg_DESY_IV = new TLegend(0.5, 0.3, 0.9, 0.5);
/*
  TGraph* gr_DESY26_2_IV_withVTRx = new TGraph(rampUpVoltage.size(), rampUpVoltage.data(), DESY26_2_I_withVTRx.data());
  gr_DESY26_2_IV_withVTRx->SetMarkerStyle(25);
  gr_DESY26_2_IV_withVTRx->SetMarkerSize(1);
  gr_DESY26_2_IV_withVTRx->SetMarkerColor(2);
  mg_DESY_IV->Add(gr_DESY26_2_IV_withVTRx);
  leg_DESY_IV->AddEntry(gr_DESY26_2_IV_withVTRx, "DESY26_2 - VTRx+ connected");

  TGraph* gr_DESY26_2_IV_withoutVTRx = new TGraph(rampUpVoltage.size(), rampUpVoltage.data(), DESY26_2_I_withoutVTRx.data());
  gr_DESY26_2_IV_withoutVTRx->SetMarkerStyle(25);
  gr_DESY26_2_IV_withoutVTRx->SetMarkerSize(1);
  gr_DESY26_2_IV_withoutVTRx->SetMarkerColor(4);
  mg_DESY_IV->Add(gr_DESY26_2_IV_withoutVTRx);
  leg_DESY_IV->AddEntry(gr_DESY26_2_IV_withoutVTRx, "DESY26_2 - VTRx+ disconnected");
*/

  TGraph* gr_DESY40_3_IV_withVTRx = new TGraph(rampUpVoltage.size(), rampUpVoltage.data(), DESY40_3_I_withVTRx.data());
  gr_DESY40_3_IV_withVTRx->SetMarkerStyle(22);
  gr_DESY40_3_IV_withVTRx->SetMarkerSize(1);
  gr_DESY40_3_IV_withVTRx->SetMarkerColor(2);
  mg_DESY_IV->Add(gr_DESY40_3_IV_withVTRx);
  leg_DESY_IV->AddEntry(gr_DESY40_3_IV_withVTRx, "DESY40_3 - VTRx+ connected");



  mg_DESY_IV->SetTitle("DESY PS Modules IV measurement");
  mg_DESY_IV->GetXaxis()->SetTitle("Voltage [V]");
  mg_DESY_IV->GetYaxis()->SetTitle("Current [uA]");
  mg_DESY_IV->SetMaximum(6);
  mg_DESY_IV->SetMinimum(0);
  mg_DESY_IV->GetXaxis()->SetLimits(0, 450);

  //gr_DESY26_2_IV->Draw("AP");
  mg_DESY_IV->Draw("AP");
  leg_DESY_IV->Draw();

}
