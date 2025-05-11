如何批次執行SIWave模擬
--- 
**Jan 2024, 安矽思科技 台灣 資深技術經理 林鳴志**

### 操作方式
批次執行多個 .siw 設計文件的過程涉及創建一個批次檔案（通常是 .bat 檔案），這個檔案包含了對SIwave的多次呼叫，每次呼叫針對不同的 .siw 檔案。我們可以遵循以下步驟： 

1. **建立批次檔案 (.bat)** ：這個檔案將包含用於執行SIwave命令的指令。 
2. **建立"執行"檔案 (.exec)** ：這個檔案將包含具體的SIwave命令，如 `ExecSyzSim`。
3. **執行批次模擬**：依次執行.siw檔案模擬直至所有模擬工作完成。

> :bookmark: **附註**
> 當使用 siwave_ng 命令在命令列中執行SIwave時，這代表你正在以非圖形化的批次模式運行SIwave。這在自動化流程中特別有用，因為它允許你執行電磁模擬而不需開啟SIwave的圖形用戶介面（GUI）。


#### 1. 建立批次檔案 (.bat) 

假設我們有三個`.siw`檔案：`project1.siw`、`project2.siw` 和 `project3.siw`。我們的批次檔案（run_siwaves.bat）可能看起來像這樣：


```bash
set path=%path%;C:\Program Files\AnsysEM\v241\Win64

siwave_ng.exe "C:\Path\To\project1.siw" "C:\Path\To\execute1.exec" -formatOutput -useSubdir
siwave_ng.exe "C:\Path\To\project2.siw" "C:\Path\To\execute2.exec" -formatOutput -useSubdir
siwave_ng.exe "C:\Path\To\project3.siw" "C:\Path\To\execute3.exec" -formatOutput -useSubdir
```



在這個檔案中，每一行都會調用 `siwave_ng` 指令來執行相應的 `.siw` 和 `.exec` 檔案。`-formatOutput` 和 `-useSubdir` 參數用於控制輸出格式和工作目錄的設置。

> :bookmark: **附註**
> **-formatOutput**：這個參數指示SIwave以一種詳細的格式生成信息、錯誤和警告消息。這種格式適用於SIwave用戶界面的後期處理。
> **-useSubdir**：這個參數指示siwave_ng不創建單獨的.siwave結果工作目錄來進行仿真設置和執行。相反，處理過程將在包含SIwave項目（或AEDB）的目錄中進行。


#### 2. 建立"執行"檔案 (.exec)

接下來，我們需要為每個SIwave專案創建一個`.exec`檔案。這個檔案將包含具體的執行命令。，我們假設每個`.exec`檔案包含`ExecSyzSim`的命令。

例如，`execute1.exec` 檔案的內容是：

```bash
ExecSyzSim
```

同理，`execute2.exec` 和 `execute3.exec` 也會有類似的內容。

> :bookmark: **附註**
>如果需要執行的 .siw 檔案都執行相同的模擬，則可以只建立一個 .exec 檔案來指定模擬參數，並在批次檔案中重複使用這個 .exec 檔案。這樣可以簡化流程並減少重複的工作。如果要跑的是其他類型的模擬，可以使用不同的[模擬命令](#模擬命令)。


#### 3. 執行批次模擬
1. 將這些檔案放置在適當的路徑。 
2. 雙擊或從命令提示符執行 `run_siwaves.bat` 檔案。 
3. 批次檔會依序執行所有指定的 `.siw` 檔案與相對應的 `.exec` 檔案。

這個過程將使得SIwave在批次模式下自動執行這些模擬，而無需手動干預。如下圖所示：

<center>
  <img src="/assets/2024-01-16_19-05-53.png" alt="2024-01-16_19-05-53" width="500">
  <figcaption>批次檔執行</figcaption>
</center><br>


### 模擬命令
本篇是以S參數模擬作為範例，所以.exec當中使用的指令是 `ExecSyzSim` ，如果要做的是其他類型的模擬，則需要代換成對應模擬的指令。下面簡要介紹各個模擬類型的命令： 
1. **ExecAcSim** : 計算頻率掃描。 
2. **ExecCrosstalkSim** : 計算頻域中的串擾掃描。 
3. **ExecDcSim** : 進行直流電壓降模擬。 
4. **ExecEmiScanSim** : 進行電磁干擾（EMI）掃描。 
5. **ExecFfSim** : 計算遠場仿真。 
6. **ExecFwsSim** : 計算全波SPICE子電路。 
7. **ExecHfssPiSyzSim** : 使用HFSS-PI計算SYZ參數。 
8. **ExecIcepakSim** : 進行Icepak仿真（熱分析）。 
9. **ExecInducedVoltageSim** : 計算感應電壓仿真。 
10. **ExecMTTFSim** : 進行電磁MTTF（平均故障時間前）仿真。 
11. **ExecNfSim** : 計算近場仿真。 
12. **ExecPdnSim**  和 **ExecPsiPdnSim** : 進行PDN通道建構仿真。 
13. **ExecPiOptSim** : 進行PI Advisor仿真。 
14. **ExecResModeSim** : 計算諧振模式仿真。 
15. **ExecSentinelCpaSim** : 進行CPA仿真。 
16. **ExecSentinelPsiAcSim**  和 **ExecSentinelPsiSyzSim** : 使用PSI求解器計算AC電流和SYZ參數。 
17. **ExecSyzSim** : 使用SIwave計算SYZ參數。 
18. **ExecTimeDomainCrosstalkSim** : 進行時域串擾掃描。



### 加入設定命令
.exec 檔案包含的命令除了要執行的模擬類型。還可以將模擬的相關設定加入其中，範例如下：

```
ExecSyzSim
     SetSwp 0 5.5e9 200 Linear
     SetInterpSwp
     SetNumCpus 4
     InterpSwpCvg 0.005
     NumInterpPts 30
     UseHpcLicenses pack
     SolverMemoryLimit 80
     ComputeExactDcPt 1
     EnableQ3dDomains 1
```

這些指令用於設置電磁模擬`ExecSyzSim`的各種參數。下面是對指令的簡單解釋： 
1. `SetSwp 0 5.5e9 200 Linear`：這條指令設置了一個頻率掃描範圍。從 0 開始到 5.5 GHz，總共有 200 個點，並使用線性步進。 
2. `SetInterpSwp`：啟用插值掃描。這通常用於在預定的頻率點之間進行細緻的插值，以獲得更平滑的結果。 
3. `SetNumCpus 4`：指定使用 4 個 CPU 核心進行模擬計算，這有助於加快模擬速度。 
4. `InterpSwpCvg 0.005`：設置插值掃描的收斂標準，這裡的 0.005 指的是允許的最大相對誤差。 
5. `NumInterpPts 30`：在插值掃描中設置 30 個插值點。 
6. `UseHpcLicenses pack`：指示使用高性能計算(HPC)的授權包。 
7. `SolverMemoryLimit 80`：為求解器設置內存使用限制，這裡是最大使用 80% 的系統記憶體。 
8. `ComputeExactDcPt 1`：啟用計算精確的直流點功能，這有助於獲得更精確的模擬結果。 
9. `EnableQ3dDomains 1`：開啟 Q3D 域的支持，這通常用於更精確地模擬低頻效應。


更多的指令請參考SIwave Help文檔。

> :bookmark: **附註**
以2024R1版為例，SIwave Help檔案的路徑如下：
C:\Program Files\AnsysEM\v241\Win64\Help\SIwave\SIwave.pdf