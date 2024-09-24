Classical API輸出Touchstone2.0
---
這段程式碼的主要功能是在 HFSS 設計中自動化地提取數據並導出 Touchstone2.0(.ts) 文件。具體功能包括：

1. 設定指定的 HFSS 專案和設計為活躍狀態。

2. 提取特定設置和掃描條件下的模擬結果，特別是頻率相關的數據。

3. 將提取的數據以 Touchstone 2.0格式導出S參數文件，並設置相關參數，例如使用多核心處理、文件精度和格式等，該檔案用於後續的電路模擬。

```python
oProject = oDesktop.SetActiveProject('connector')
oDesign = oProject.SetActiveDesign('HFSSDesign1')
oTool = oDesktop.GetTool("NdExplorer")


#%%
oModule = oDesign.GetModule('ReportSetup')

arr = oModule.GetSolutionDataPerVariation(  
"Matrix", 
"Setup1 : Sweep1", 
["Context:=", "Original"],
['Freq:=', ['All']], 
[""])

freqs = list(arr[0].GetSweepValues('Freq'))

oTool.ExportFullWaveSpice(oDesign.GetName(), False, "Setup1 : Sweep1", "",
	[
		"NAME:Frequencies", 
	] + freqs, 
	[
		"NAME:SpiceData",
		"SpiceType:="		, "TouchStone2.0",
		"EnforcePassivity:="	, False,
		"EnforceCausality:="	, False,
		"UseCommonGround:="	, True,
		"ShowGammaComments:="	, False,
		"Renormalize:="		, False,
		"RenormImpedance:="	, 50,
		"FittingError:="	, 0.5,
		"MaxPoles:="		, 10000,
		"PassivityType:="	, "IteratedFittingOfPV",
		"ColumnFittingType:="	, "Matrix",
		"SSFittingType:="	, "FastFit",
		"RelativeErrorToleranc:=", False,
		"EnsureAccurateZfit:="	, True,
		"TouchstoneFormat:="	, "MA",
		"TouchstoneUnits:="	, "GHz",
		"TouchStonePrecision:="	, 15,
		"SubcircuitName:="	, "",
		"ExportDirectory:="	, "C:/Program Files/AnsysEM/v242/Win64/Examples/HFSS/Signal Integrity/",
		"ExportSpiceFileName:="	, "HFSSDesign1_Setup1_Sweep1_1_sp.ts",
		"FullwaveSpiceFileName:=", "HFSSDesign1_Setup1_Sweep1_1_sp.ts",
		"UseMultipleCores:="	, True,
		"NumberOfCores:="	, 10
	])

```
