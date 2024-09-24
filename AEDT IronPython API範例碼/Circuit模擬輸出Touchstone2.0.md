Circuit模擬輸出Touchstone2.0
---
這段程式碼的目的是在AEDT Circuit當中自動化處理數據並生成Touchstone2.0文件，過程如下：
 
1. `oProject` 和 `oDesign` 用於獲取目前活動中的專案和設計。
 
2. 使用 `oTool` 取得 NdExplorer 工具，這是用於進行波形模擬數據處理的工具。
 
3. 透過 `oModule` 進入 ReportSetup 模組，並呼叫 `GetSolutionDataPerVariation` 來獲取解算資料，參數包括「標準變異」和「線性頻率」的資料。
 
4. 使用 `GetSweepValues('Freq')` 取得解算結果中的頻率數據。
 
5. 最後，透過 `ExportFullWaveSpice` 將解算結果輸出為Touchstone格式的SPICE文件，設定詳細的輸出選項如文件格式、數據擬合類型、多核心運算等，並指定輸出檔案的存放路徑及名稱。

```python
oProject = oDesktop.GetActiveProject()
oDesign = oProject.GetActiveDesign()
oTool = oDesktop.GetTool("NdExplorer")

oModule = oDesign.GetModule('ReportSetup')

arr = oModule.GetSolutionDataPerVariation(  
"Standard", 
"LinearFrequency", 
["NAME:Context", "SimValueContext:=", [3,0,2,0,False,False,-1,1,0,1,1,"",0,0]],
['Freq:=', ['All']], 
[""])

freqs = list(arr[0].GetSweepValues('Freq'))

oTool.ExportFullWaveSpice(oDesign.GetName().split(';')[1], False, "LinearFrequency", "",
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
		"Renormalize:="		, True,
		"RenormImpedance:="	, 0.1,
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
		"ExportDirectory:="	, "d:/demo/",
		"ExportSpiceFileName:="	, "HFSSDesign1_Setup1_Sweep1_1_sp.ts",
		"FullwaveSpiceFileName:=", "HFSSDesign1_Setup1_Sweep1_1_sp.ts",
		"UseMultipleCores:="	, True,
		"NumberOfCores:="	, 10
	])

```