HFSS網格設定技巧
---

網格劃分技術對於仿真的準確性和效率起著決定性作用。HFSS 提供了幾種網格技術，包括 Classic mesh 和 TAU mesh。本文將專注於這兩種網格技術的特點、適用情景以及手動操作的建議流程。

![2024-04-19_13-34-30](/assets/2024-04-19_13-34-30.png)


#### Classic Mesh

Classic mesh 是一種傳統的網格生成技術，它在各種結構中都有較高的成功率，但這種技術往往會消耗大量的計算資源。Classic mesh 通常在無法使用更高效的網格技術時作為後備選項。
#### TAU Mesh

相對於 Classic mesh，TAU mesh 是較新的技術，尤其適用於具有複雜幾何結構的物體，如具有Z軸弧度變化的3D機殼或是有額外彎曲的結構。TAU mesh 能夠更有效地處理這些複雜形狀，提供更精細的網格劃分，從而可能提高計算的效率。
### 自動與手動 Mesh 劃分 
1. **自動網格設定** ：
- 預設 mesh setting 為 Auto，允許HFSS軟件會自動選擇適合的網格劃分方法。一般情況下，系統會優先嘗試 TAU mesh，若不成功則轉向 Classic mesh。 
2. **手動網格設定** ：
- 對於層狀 PCB 或 package 結構，若布局層次分明且無銅蝕刻設計（etch），選擇 Classic mesh 並啟用 Allow Phi for layered geometry，以利用 Phi mesh 進行更合適的網格劃分。
- 若布局中包含銅蝕刻設計，則應選擇 Classic mesh，並禁用 Phi mesh。

![2024-04-19_13-36-03](/assets/2024-04-19_13-36-03_alq73mkak.png)

#### 物件尺寸調整

對於極小的物件，手動調整 Model resolution 可有助於成功生成初始網格：

![2024-04-19_13-37-57](/assets/2024-04-19_13-37-57.png)


如果物件是有弧度的, 可以試著將slide bar往右移動兩格試試看.  

![2024-04-19_13-40-15](/assets/2024-04-19_13-40-15_nji4nnm90.png)

#### TAU Mesh 手動優化流程

如果自動 TAU mesh 嘗試失敗，可以按照以下步驟手動優化：
1. 使用 TAU 進行初始網格劃分。
2. 若失敗，調整 Surface Approximation 設置。
3. 若再次失敗，將 Maximum Surface Normal deviation 設置調小至 30 度或更低。
4. 若仍未成功，調整 Maximum aspect ratio，從 20 降至 10 或 5。

![2024-04-19_13-44-36](/assets/2024-04-19_13-44-36_42998lscy.png)

5. 若以上步驟均失敗，則使用 Classic mesh 強制進行初始網格劃分。

透過以上的專業指南，使用者可以根據自己的具體需求和結構特點，選擇和調整最適合的網格技術，從而達到最佳的仿真效果和計算效率。