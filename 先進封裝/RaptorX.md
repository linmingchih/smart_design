RaptorX™
---
**2024 Apr., ANSYS Taiwan**
### I. 概論

RaptorX™是一款創新的pre-LVS驗證電磁建模軟件工具，適用於電磁專家和集成電路（IC）設計工程師。它的引擎極限容量、高度精確的結果以及顯著快速的建模時間是它相比其他傳統電磁工具的主要區別點。

隨著設計複雜性的增加，當前的電路可能包含數百個被認為是“關鍵”的端口和網絡。隨著設計的操作速度提高，了解其所有元件的電磁反應變得越來越重要。RaptorX是市場上唯一能夠為如此複雜、高頻的類比電路和高速數位電路計算RLCk寄生元件的產品。

RaptorX能夠準確地提取任何被動裝置、任意布線、帶有平面（實心或穿孔）的佈局、MiM/MoM電容器等組合的全電磁模型。它的核心建模引擎VeloceRaptor突破了現有的頻率和容量限制，超越了市場上任何其他可用的電磁建模工具。

通過用戶友好的界面，可以在佈局中選擇多個網絡並由VeloceRaptor建模引擎進行建模。模型是即時生成的，並以完全被動且穩定的RLCk網表、S-參數文件和有理函數模型（RFM）的形式交付。RaptorX將準確捕獲所有選定網絡之間的交互作用，準確地模擬所有涉及的高頻現象，例如磁性和電容耦合、皮膚效應和鄰近效應。

這款工具有以下特點： 
- **晶圓廠認證和與HFSS相關的準確性：**  RaptorX/H通過了製造商的認證，並且其模擬結果與HFSS（一款高頻電磁場模擬軟件）的結果具有相關性。 
- **LDE處理能力達到3nm技術節點：**  RaptorX/H能夠處理最先進的製程，其局部密度效應（LDE）模擬可以達到3納米技術節點。 
- **iCAPs（矽中介層電容）的分析建模：**  能夠模擬在矽中介層設計的電容。 
- **高容量、高速度：**  能夠快速處理大規模的數據。 
- **集成和自動化的IC流程：**  RaptorX/H可以無縫集成到IC設計流程中，並自動化處理許多步驟。 
- **進階特性：**  堅固的技術檔案處理、加密以及溫度依賴的處理能力。 
- **自動化幾何處理：**  能夠自動識別和處理IC設計中的幾何形狀。

![2024-04-08_21-13-48](/assets/2024-04-08_21-13-48.png)


### II. 模擬設定

![2024-04-09_09-27-46](/assets/2024-04-09_09-27-46.png)

#### 高階網格設定選單面板

**網格頻率(Mesh Frequency)**
默認情況下，RaptorX 啟用了邊緣網格(Edge Mesh)選項。網格化遵循邊緣網格與最大興趣頻率(Max Frequency of Interest)的組合。你可以覆蓋預設的網格化應用並將邊緣密度和厚度選項擴大。最大網格頻率(`f_mesh`)控制外部元件的寬度和厚度或導線的最大長度。這設定是提供最大頻寬以改善頻率響應，即設置最大興趣頻率到足夠高以改善模擬精度。模擬器通常首先計算一個脈沖響應，然後S參數模型的提供與脈沖響應的保真度可以提升。網格頻率可用於控制電磁提取的硬體需求，同時保留所需的建模精確度。

**邊緣網格(Edge Mesh)**
這個選項控制外部導體絲狀物的厚度和寬度。（圖20：根據邊緣網格設置的導體分割）。默認情況下，邊緣網格設為0.8um。當勾選時，它優先於網格頻率或最大興趣頻率。如果有指定，邊緣網格覆蓋導體外部並且等同於由最大網格頻率（如果啟用）或最大興趣頻率定義的皮層深度。用戶可能更喜歡修改 RaptorX 模型引擎的邊緣網格，以控制要從佈局中提取的導體的分割水平。增加邊緣網格簡化了總體佈局的網格化並加速了提取運行。

當模擬極高頻的長距離傳輸線時，最大興趣頻率可能在數百GHz範圍內。對於 RaptorX，這將轉化為非常低的邊緣網格，這會導致模型提取時間和記憶體足跡顯著增加。適當的最大興趣頻率和邊緣網格組合，仍然允許在傳輸線上保留模型精度（確保適當的範圍有效性並提取模型）。

另一個邊緣網格特別有用的情況是簡化 Vdd 和 Vss 網絡的網格化。這些網絡可以用較低的網格頻率分析和/或使用寬闊的邊緣網格而不會對模型性能有明顯影響。

**單元格/波長(Cells/Wavelength)**
這個設置描述每個波長下能配合的單元格數，預設值是40。波長是根據最大興趣頻率或網格頻率來計算的。將 Cells/Wavelength 設定為20意味著如果一個物件的寬度或長度是半波長，則該物件將被劃分為10個單元格。

**平面投影因子(Plane Projection Factor)**
為了消除大金屬平面的不必要網格複雜性並提高整體提取時間，你可以定義平面投影因子。最佳提取選項和網格進階選項表格（建模階段部分）的設定對於網格化導體有特別的考量。在這些案例中，此設定可以簡化地面平面的網格，同時保留所需的精準度。

**放鬆的 Z-軸網格(Relaxed z-axis Mesh)**
這是一種在 z-軸提供簡化網格的機制。如果導體的厚度超過皮層深度的三倍（3δ），則不會執行動態網格，而只在 z-軸上創建不超過三個絲狀物。頂部和底部絲狀物的厚度與定義的網格頻率相同，中間絲狀物等同於剩餘厚度。

這個特性可以將提取時間和記憶體幾乎減半，同時對精度影響微小。由於在某些情況下這會影響性能，這個功能默認是關閉的。

**啟用佈局相依效應(Enable Layout Dependent Effects)**
考慮到導體寬度和相鄰導線或局部密度變化（因凹槽、繪製厚度、間距等）對電阻率的變化。這個設定會根據導體繪製的厚度和間距來調整它的鄰居。

**啟用蝕刻轉換(Enable Etching Transform)**
“預先扭曲”佈局基於鑄造廠規則，應用導體的偏差(正/負 - 凹陷/膨脹)在導體邊緣因難以避免的光學效應而產生，對應於先進 CMOS 技術。

**啟用高級電容效應(Enable Advanced Capacitance Effects)**
應用所有與電容相關的效應，如符合介電質、載入效應、介電損壞。

**啟用基板網路提取(Enable Substrate Network Extraction)**
使用等效分佈RC網路模型基板耦合效應。默認情況下，此選項已啟用（“開”）。

建模引擎能夠檢測到低損耗(低電阻率)基板的存在，並採用適當的RLCK網絡列表(而不是簡單的RC)來記賬圖像電流效應。

**提取浮動金屬(Extract Floating Metals)**
啟用以兩種模式對浮動金屬的建模：
- 作為虛擬填充(As Dummy Fill)：捕捉虛擬填充的效果，通過提取有效電容隔離帶之間的配對金屬片段，從而模擬虛擬填充密度的影響。
- 作為浮動網(As Floating Nets)：浮動金屬被視為任何其他金屬。任何不屬於所選淨值的金屬段，明確地由現有佈局標籤/標誌或虛擬放置的RaptorX針腳定義，則被視為獨立的淨值（"floatingNets"）並根據提取模式和網格頻率設定被網格化。

**啟用混合提取(Enable Hybrid Extraction)**
混合提取的概念建立在電磁(EM)效應主導的層面，以進行更高效的提取。可以將佈局水平分成兩部分。上層預計包含較小數量的端口，並以電磁精度提取，而下層則在RC或只有電阻/電容模式中提取，因為捕獲任何基板耦合的影響僅需模擬/或電容內容。而底部的模型考慮了上部份存在，提供兩部分設計的電容耦合。此方法的主要好處是：
1. 整體提取時間更短，因為電路的EM部分顯著降低了複雜度。
2. 作為提取模式的結果，提取產品即時性更強。

混合模式提取的設置細節可在建模階段部分找到。

**覆蓋收縮因子(Override Shrink Factor)**
明確地設定收縮因子，即，評估遷移到半節點技術的假設情境。此設定將覆蓋技術文件提供的默認值。

**清單輸出格式(Nodelist Output Format for RLCK/RC Extraction Modes)**
RLCK/RC提取模式的標準輸出是寄生提取的網絡列表。需要預減少的結果 - 比如Model Order Reduction模型 - 可以生成。當選擇"物理"輸出時，"啟用SP算法" (Model Physical Extraction) 模式的選項將被生成。當選擇"簡化"輸出時，S參數模型還將被額外生成。

**附加提取引擎參數(Additional Extraction Engine Arguments)**
這個子面板應由進階使用者使用，以設定特定的進階提取參數。勾選方框然後點擊設定來啟用進階參數面板。

### III. 提取模式

提取模式子面板提供兩種不同的提取類型："電磁"和"寄生提取"。不同的模式可以用來解決不同的需求，因此提供了在提取複雜性和所需計算資源之間找到最佳折衷方案的靈活性。下面是對每個提取模式的詳細說明：

- **電磁**：包含黃金電磁（Golden EM）和快速電磁（Fast EM）模式。輸出模型是 S 參數、RFM 和 netlist。S 參數模型包括一個直流點（不需要從電路模擬器進行外推）。所有模型都適合任何頻率或時間域分析。在這些模式下，版圖的詳細網格由版圖的幾何形狀和最大操作頻率設定共同決定。
  - **黃金電磁**：是最終精準的電磁建模模式。它特別針對非常敏感的高頻應用，在 60 GHz 及以上頻率上精確覆蓋從直流到 100+ GHz 的頻率。網格生產是非常細致的，這種模式在 CPU 時間和記憶體佔用方面是最資源密集的。
  - **快速電磁**：是一種加速的電磁提取模式，目標是直流到 100+ GHz 頻率範圍。這種提取模式是複雜度和所需計算資源之間的最佳折衷方案，用於模型高達 60 GHz 的網格相比黃金電磁模式略微簡單。
  
- **寄生提取**：包括 RLCK、RLCK lite、RC、C 和 R 只模式。適用於低 GHz 範圍提取。輸出模型是物理 RLCK netlist。"高級"選項卡下的一個特殊設置可以按需創建簡化 netlist 和 S 參數模型（參見圖 19：HelicCentral 設置 - Advanced Tab on page 28）。當使用這些模式時，最大頻率設定對版圖的網格化沒有任何影響。
  - **RLCK**：當操作頻率、線寬和線幾何的組合使得趨肤效應和鄰近效應很小時，這個模式提供了一種快速有效的方法來獲得一個準確的 EM 模型，這在密集連接和包含大量端口的情況下特別有用。
  - **RLCK lite**：是 RLCK 的一種加速替代品，適用於極度資源要求嚴格的情況，只模擬電感（這樣實際上是避免了為所有電感模型提取互感的需要）。RLCK lite 可以在保持合理的準確度的同時，進一步增強提取引擎的容量，與 RLCK 提取相比，可以進一步增強電容提取引擎的能力。



### IV. 模擬引擎

VeloceRaptor 是驅動所有晶片上電磁（EM）模擬工具核心的 EM 引擎。它突破了傳統頻率和容量限制，性能超越市面上任何其他電磁模型工具。

#### 建模方法概述

在半導體 IC 環境中進行電磁（EM）分析的兩個主要問題歷來是版圖和堆疊的複雜性。==複雜的版圖通常需要通過同等複雜的網格進行分析，而複雜技術堆疊則需要數值計算密集型的 Green 函數==。VeloceRaptor 建模引擎通過結合精妙的方法解決了這些問題，將傳統電磁學與混合 EM 建模引擎相結合。

在布局環境中，VeloceRaptor 階層式掃描電路版圖設計。基於從 Ansys EM 技術文件獲得的信息，使用專有的網格算法對幾何體進行離散化處理（參見第92頁的版圖處理），從而生成最適合其建模方法的網格。為了提升速度和效率，引擎結合了兩種不同的建模方法。==第一種是專有版的部分元素等效電路（PEEC）方法，用於模擬自感和互感==（參見第93頁的感應阻抗和阻抗阻抗模擬），==第二種是隨機漫步（RW）方法，用於計算幾何體不同部分之間的電容，以及基板耦合==（參見第94頁的電容提取以及第95頁的基板網絡提取）。輸出可用於多種格式，包括 RLCK 網絡表、S 參數和有理函數模型(Rational Function Models, RFM)。

這些建模方法確保了從直流點至少至 110GHz 的準確性（如模型測試所證實）。結果模型與各種非線性分析（瞬態、噪聲等）兼容。

#### 版圖處理

由於需要模擬從直流（DC）到毫米波頻率的電磁效應，這要求對版圖進行特殊處理。RaptorX 採用了一種專有的混合網格技術，有效地區分出版圖中電流流動主導方向的區域。在這些區域中，==採用單一方向（而不是矩形）網格單元，因此相比傳統網格技術，生成了更粗糙但也更高效的網格==。其餘區域則使用矩形和三角形網格單元的適當組合進行網格劃分（圖96：混合網格概覽，參見第93頁），同樣實現了網格複雜性的顯著減少。引擎能夠在網格步驟之前根據技術檔案中描述的所有版圖依賴效應（LDE）來調整工具對幾何形狀和材料屬性的視圖。

#### 感抗和阻抗建模

對於感抗和阻抗的建模，VeloceRaptor 採用了創新的部分元素等效電路（Partial Element Equivalent Circuit, PEEC）方法，這一方法結合了全波電磁建模引擎的準確性和 spice Netlist 輸出的靈活性與互操作性。PEEC 方法的主要優勢之一是它允許獨立解決感抗和部分電容問題。在求解感抗時，由於介質是磁性均勻的，可以輕易獲得 Green 函數的解析表達式。電容計算—必須使用更複雜的 Green 函數進行—則採用不同的方法處理（參見第94頁的電容提取）。通過利用部分感抗理論進一步加快計算，建模引擎涵蓋了複雜的電磁現象（例如，電流分佈、趨肤效應和鄰近效應），並提供了從直流到毫米波頻率完整捕捉感抗和阻抗行為的模型。


#### 電容提取

在 3D 多導體 nm-CMOS 製程中，電容提取是關於電荷分佈的全面考量。這背後的物理法則由高斯定律來解釋，它關聯了通過導體封閉表面的外向電場通量和被封閉的總電荷。解決靜電問題允許我們確定任何兩個導體間耦合電容 C_ij 與封閉的電荷。Helic 工具所使用的 3D 電容提取方法採用了基於隨機漫步方法的精密隨機抽樣算法，用於計算高斯表面及相對應任意形狀導體之間耦合電容的電場。這種提取原理的示意圖見於圖 98：基於隨機漫步的抽樣程序及相關耦合電容，詳見第 94 頁。

電容提取器是一個完全意識到電荷並分佈式的 3D 靜電電容解算器。這種隨機抽樣依賴於多層 Green 函數的複雜數值解決方案和不使用模式匹配表和平均化，因此它能達到可能的最高準確度。其表現也因為無導體離散化瓶頸而令人印象深刻，且在電路尺寸方面比邊界或體積網格方法有更好的擴展性。準確的電容提取與優異的計算效率結合在一起，因為隨機漫步本質上是一種平行且極快的算法。

#### 基板網絡提取

Helic 工具背後運行的獨特提取引擎，使用分佈式 RC 網絡模擬基板耦合效應。一種基於隨機蒙地卡羅方法的策略和 3D 基板模型，允許非常快速且準確地提取分佈式 RC 基板網絡，如圖 99 所示：分佈式 RC 基板網絡提取，詳見第 95 頁。

該方法採用隨機漫步算法，能夠在不需要三維離散化的情況下，通過適當的 Green 函數對多個基板層進行特性描述。其電容提取和基板模型算法的平行性質提供了可擴展性和總提取時間，優於任何其他方法。建模引擎能夠檢測出損耗性（低電阻率）基板的存在，並採用適合的 RLCK Netlist（而不是簡單的 RC），以考慮影像電流效應。

#### 模型簡化

前段落所呈現的建模方法確保了從直流（DC）到毫米波應用頻率的準確電磁模擬。然而，在某些結合高版圖複雜度與高應用頻率的案例中，可能需要極為細緻的網格來保證整個感興趣頻寬的準確性，這樣的離散化水平可能導致極大的 Netlist 模型（節點計數和裝置計數）。這些模型反過來在模擬過程中需要極大的計算資源（記憶體和時間）。==必須採取額外措施來最小化計算時間和記憶體要求是至關重要的==。透過應用模型次序簡化（MOR）技術，結合專利的 Netlist 去標記方法，實現了在保持出色準確度的同時，為模擬減少時間和記憶需求的艱難任務。

模型簡化的輸出是 S 參數、有理函數模型（RFM），和 Netlist 格式，以滿足不同分析需求（線性、瞬態、PSS 等等）。此外，從直流點到保證的準確度，所有簡化過程的階段都被設計用來確保原始（完整）Netlist 的因果性和被保存。

#### 輸出格式

建模引擎的輸出有多種不同格式，允許您獲得從直流（DC）到毫米波頻率可能應用的整個頻帶的分析解決方案。這些輸出包括：

- **物理 Netlist**：這是建模引擎的直接輸出，並未經過模型次序簡化（MOR）處理。在 Spectre 和 Spice（Hspice）格式都有提供，它是一個典型的 RLCK 提取輸出，用於低至中頻段的分析。
- **S 參數檔案**：作為最受歡迎和廣泛使用的電磁模型輸出之一，它是 MOR 過程的直接輸出。可在業界標準的 Touchstone 格式中獲得，通常用於頻域分析。
- **簡化 Netlist 格式**：經過模型次序簡化後生成的 Netlist 包含正負電阻和電感、正負電容以及電壓/電流控制源。Netlist 是被動的、因果的且與噪聲兼容（因為正電阻）。控制源不違反被動性，因為它們只用於連接輸入/輸出端口與內部節點。當設計變得過於龐大和複雜時，是物理 Netlist 的理想替代品。
- **RFM 模型**：Helic 建模引擎還輸出一個有理函數模型（RFM），可作為模擬的替代模型。RFM 是一個數值模型（不是 Netlist），與模型次序簡化過程後產生的傳遞函數的有理近似相對應。

### V. 進階製造效應(Advanced Fabrication Effects)

下列部分描述了下述工具支持的進階製造效應：

- **偏壓(Biasing)**：作為導體繪製寬度及其鄰近空間或局部密度功能的蝕刻。
- **佈局依賴性電阻率(Layout Dependent Resistivity)**：電阻率作為導體繪製寬度和鄰近空間或其局部密度的功能，因凹槽、開槽、包覆厚度等而變化。
- **侵蝕(Erosion)**：導體厚度的變化作為其繪製寬度和鄰近空間或其局部密度的功能，主要由於化學機械拋光(CMP)。
- **負載效應(Loading Effect)**：變化導體下方介電質的厚度作為導體繪製寬度和繪製間距的功能。
- **符合介電層(Conformal Dielectric Layers)**：符合特定導體層而造成非平面介電層形成。
- **介電損壞(Dielectric Damage)**：薄層介電“塗層”（旁邊和/或下面）附屬於相關的導體層。
- **側壁依賴性介電損壞(Sidewall-dependent Dielectric Damage)**：類似於介電損壞，但不同的是導體寬度和鄰近導體間距的介電“塗層”依賴性。
- **彩色遮罩和多重圖案化(Color Masks and Multi-patterning)**：支持更小特徵和間距的多重遮罩技術。所有上述效應都是基於掩模對對象的基礎（即，興趣導體和鄰居的掩模）來定義的。

#### 偏壓(Biasing)

導體偏壓指定了因製造過程中無法避免的光學效應而在導體邊緣發生的蝕刻（正面或負面 - 凹陷或膨脹）。在小於100納米技術中的影響是顯著的，如圖34所示：蝕刻後輪廓與繪製的佈局(DRAWN Layout)的比較，該圖位於第42頁。有可能的是，偏壓/蝕刻過程會根據線路的方向不同而對線路產生不同的影響，如第42頁的圖35：基於方向的蝕刻實例(Orientation Based Etching Example)所示。

在某些技術中，偏壓值可能會因將要提取的元件而有所不同。例如，一些金屬層可能會因電容計算而遭受完全不同的偏壓，與電阻計算完全不同。這樣的蝕刻情境（基於電容和電阻的）由RaptorX支持。

#### 佈局依賴厚度(Layout Depended Thickness)

先進的CMOS製程也會受到銅線上的凹陷效應的影響，這會直接影響到橫截面，隨後影響到互連的電阻和電容（圖36：作為寬度和間距功能的厚度變化，第43頁）。對給定線路的影響量取決於其所在的環境，即金屬層的“局部”密度、與鄰近線路的間距及其自身的寬度。金屬厚度的變化也會導致側介電質厚度的變化，必須正確計算以進行正確的電容計算（圖37：金屬厚度變化與側介電質（IMD3b）厚度變化，第43頁）。考慮到即使是鄰近的互連也可能會有顯著不同的厚度變化，因此使用加權平均過程來得出最終的側介電質厚度。

在某些技術中，厚度變化值可能會因將要提取的元件而有所不同。例如，一些金屬層可能會因電容計算而遭受完全不同的偏壓，與電阻計算完全不同。RaptorX支持這樣的蝕刻情景（基於電容和電阻的）。

#### 佈局依賴電阻率(Layout Dependent Resistivity)

在小於100納米技術中，導體電阻率會因數個因素而變化。化學機械拋光(CMP)過程通常會導致自導體頂部的銅材料被顯著移除（凹陷），這對於寬導體影響更大。此效應在圖36所示：作為寬度和間距功能的厚度變化，第43頁。此外，包覆層是在銅導體周圍和底部生長的材料，以保護導體免受化學反應的影響，也可能對導體電阻率有顯著影響，並且在更窄的導體上更為明顯（效應以粉紅色在圖38所示：包覆效應，第44頁）。

類似於厚度變化，電阻率對給定線路的影響量取決於其所在的環境，即特定金屬層的“局部”密度、與鄰近線路的間距以及自身的寬度。

#### 負載效應(Loading Effect)

負載效應指的是由於化學機械拋光(CMP)過程（過度或不足的蝕刻）引起的導體下方介電層厚度的變化（減少或增加），其影響在圖39所示：由於過度或不足蝕刻的負載效應，第44頁。這種介電層厚度變化預期將影響垂直電容，這是金屬導體寬度和相鄰導體間距的函數。

類似於厚度變化，考慮到即使是鄰近的互連也可能會有顯著不同的負載效應，因此使用加權平均過程來得出最終的基層介電層厚度，以便在RaptorX提取中得到正確的計算。

#### 符合層和介電損傷(Conformal Layers and Dielectric Damage)

符合介電質層被鋪設在導體層的上方、旁邊或下方，其厚度要麼是均勻的（均勻符合介電質），要麼在某些區域比其他區域厚（非均勻符合介電質）。它們對電容的影響是非可忽視的，需要適當消耗才能提供準確的結果。最常用的符合介電質排列在圖40所示：各種符合介電質排列，第45頁。

符合介電質的一個子集是著名的“損傷介電質”。它們在小於16納米技術中變得流行，這是由於用來創建低K介電質的步驟，其中在介電質膜中引入了孔隙性，相對介電常數低於約2.5。在這樣的低K層中，多孔材料容易受到化學過程步驟（如蝕刻和去除阻抗層）的影響，導致介電質的修改（即損壞）。在小於100納米的過程中，側壁和底部的損傷不能忽視，因為它們可能對寄生電容的準確提取有重大影響。介電損傷應該通過定義沿金屬邊緣的溝槽介電質來解決，如圖41所示：各種介電損傷情景，第45頁。

在小於7納米技術中，側壁損壞厚度也可能依賴於線寬和間距。



#### 光罩與多重圖案化(Masks & Multi-patterning)

多重圖案化過程將單一金屬層的部分分割成多個圖案。這些“不同”的圖案分別印刷，因此，這些過程可以實現比單一圖案更小的尺寸（金屬尺寸和間距）。如果一個圖案相對於另一個移動，提取結果可能會受到這種做法的顯著影響，因為它導致不同的蝕刻（偏壓）值（圖42：在雙重圖案技術上的蝕刻應用過程，第45頁和圖43：在第46頁的蝕刻應用示例）。典型地，雙重圖案化技術（兩個圖案）更常被使用。然而，使用超過兩個圖案的多重圖案化技術也是可能的，但它們導致了更加複雜的蝕刻情境。

除了蝕刻機制和值之外，多重圖案化還可能影響其他佈局依賴效應，如佈局依賴電阻率和金屬/介電質厚度，甚至側壁依賴損壞寬度。

#### RaptorX 支持的效應列表

| Category  | Description                                      |
|-----------|--------------------------------------------------|
| Conductor | 多重圖案化 / 著色 (Multi-patterning / Coloring) |
| Conductor | 蝕刻 (單一或多重表格) (Etching (single or multiple tables)) |
| Conductor | 依寬度的 TCI/TC2 (Width dependent TCI/TC2)      |
| Conductor | 金屬厚度變化 (電阻) (Metal thickness variation (Resistance)) |
| Conductor | 金屬厚度和密度界限 (電阻) (Metal thickness and density bounds (Resistance)) |
| Conductor | 金屬厚度變化 (電容) (Metal thickness variation (Capacitance)) |
| Conductor | 金屬厚度和密度界限 (電容) (Metal thickness and density bounds (Capacitance)) |
| Conductor | 側壁損壞厚度變化 (Sidewall damage thickness variation) |
| Dielectric | 恆定損壞厚度 (Constant damage thickness)       |
| Dielectric | 底部介電質厚度變化 (Bottom dielectric thickness variation) |
| Dielectric | 側介電質厚度變化 (Side dielectric thickness variation) |
| Via       | RPV 通孔面積 (Contact table) (RPV vs via area (Contact table)) |
| Via       | RPV TCI/TC2 通孔面積 (RPV TCI/TC2 vs via area)  |


### IX. Raptor X 設定重點
在RaptorX的情境中，當金屬層在z方向上不連續時，沒有通孔(via)連接就會產生錯誤。RaptorX求解器需要連續的金屬層通過通孔相連接，所以如果缺少通孔，就會出現錯誤。

![2024-04-08_20-42-11](/assets/2024-04-08_20-42-11.png)

技術檔案生成過程中提前驗證RaptorX求解器的要求並發出具體警告是有意義的。這樣可以在設計過程早期就識別出潛在的問題，避免在後期模擬過程中出現錯誤。通過這種方式，如果檢測到金屬層在z方向上連續但未通過通孔連接，系統應該發出特定的警告。這有助於提高效率，避免進行不必要的設計修正，並且確保模擬結果的準確性。

因此，修改技術檔案生成過程，以在早期階段驗證金屬層和通孔的連接，並在發現潛在問題時發出警告，是一


#### RaptorX 是否使用電路元件來模擬導通孔？


答：不，RaptorX 不使用電路元件來模擬導通孔。相反，它通過計算 z 方向上的阻抗元件來處理導通孔。對於小尺寸的導通孔，RaptorX 會創建堆疊區域並在這些區域內計算阻抗。它可以為堆疊區域內的所有金屬層和導通孔計算平均阻抗，或者為每層單獨計算阻抗。

#### 當無法獲得導通孔的網格信息時，RaptorX 如何處理？

答：即使無法獲取導通孔的網格信息，RaptorX 也能進行有效的模擬與分析。對於具有顯著長度的導通孔（例如，連接封裝層或通過矽孔的導通孔），RaptorX 會計算 z 方向上的阻抗和感抗元件。這意味著 RaptorX 進行的是明確計算，不依賴於導通孔的網格表示。

#### 進行電源完整性（PI）模擬時是否需要為端口/端子指定低阻抗負載？


答：不需要。RaptorX 會提取具有參考阻抗的 S-參數模型，然後設計師可以使用電路模擬器，在 S-參數端口處指定所需的阻抗。這意味著在 PI 模擬過程中，無需事先為端口/端子分配低阻抗負載，因為模擬過程中可以靈活設定和調整阻抗。
