如何在 AEDT 中高效進行 DQ 網路的 TDR 掃描
---

**適用於：Ansys Electronics Desktop (AEDT) Circuit**

![TDR Sweep Concepts](https://img.youtube.com/vi/xn8yxk11rYg/maxresdefault.jpg)

這項技術主要介紹如何利用簡單的 SPICE 子電路（Sub-circuit）作為「電子開關」，自動切換測試路徑，大幅提升在 AEDT 中對多組記憶體 DQ 信號線進行時域反射原理 (TDR) 模擬的效率。

### :video_camera: 操作參考影片
[How to Make TDR Sweep of DQ nets Efficiently in AEDT](https://www.youtube.com/watch?v=xn8yxk11rYg)

---

### 核心痛點解決
*   **避免串擾失真**：在對多條 DQ 信號網絡進行 TDR 阻抗分析時，傳統上必須採用「逐根單獨測試（One by one）」的策略，以防止通道間的串擾（Crosstalk）導致模擬結果失真。
*   **消除手動設定的繁瑣**：當 PCB 上的 DQ 信號線數量龐大時（如 DDR 記憶體通道），手動為每個網路設定 TDR 探針與驅動源非常耗時且容易出錯。


### 關鍵功能與實現技術
#### 1. SPICE 子電路切換路由
導入一個結構簡單的 SPICE 子電路（.subckt）作為電子開關。透過外部參數控制，即可自動切換 TDR 訊號源與不同 DQ 網路之間的連接關係。

**SPICE 邏輯範例：**
```spice
.subckt switch in o1 o2 o3 o4 on=1 Zt=50
.if(on==1)
r1 o1 in 0
r2 o2 0 Zt
r3 o3 0 Zt
r4 o4 0 Zt
.elseif(on==2)
r1 o1 0 Zt
r2 o2 in 0
r3 o3 0 Zt
r4 o4 0 Zt
...
.endif
.ends
```

#### 2. 自動化變數掃描 (Variable Sweep)
在 AEDT Circuit 設計中，定義一個代表「當前測試網路編號」的變數（例如 `test_idx`），並結合 **Parametric Setup**。

#### 3. 一鍵完成多網路 TDR 模擬
系統會根據設定的步進值，自動切換 SPICE 開關並依序完成所有 DQ 線路的 Transient（時域）波形模擬。

### 預期應用效益
*   **極大化節省工作量**：將數小時的手動設定縮短至幾分鐘。
*   **維持高精準度**：在完全不引入鄰近線路串擾的前提下，快速收集整組 DQ 匯流排的阻抗不連續點（Impedance Variation）數據。

---

### :link: 相關工具
若需要自動生成任意 Port 數量的開關 Netlist，可以使用以下腳本：
[create_switch.py](/assets/create_switch.py)
