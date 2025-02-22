這些年來，CPU的算力增長速度相較於過去有所減緩，這主要有幾個原因：

1. **摩爾定律放緩**：摩爾定律預測每隔大約兩年，晶體管的數量會翻倍，從而提升計算能力。但近些年，由於製程微縮接近物理極限，將更多晶體管塞入相同面積的芯片變得越來越困難。尤其當製程縮小至7奈米甚至更小，許多工程挑戰，例如功耗和漏電流的增加，已經很難突破。

2. **熱與功耗限制**：提高CPU主頻率（時脈速度）曾是提升算力的主要方式，但更高的頻率會帶來更多的功耗與熱量。隨著主頻增長，功耗與散熱需求呈指數增長，使得散熱問題成為一個很大的瓶頸。因此，製造商近年來更專注於多核設計和能效提升，而非大幅提高時脈速度。

3. **Dennard Scaling 不再成立**：Dennard Scaling 原則指出，隨著晶體管尺寸的縮小，其功耗也應成比例下降，使得性能和功耗可以同步提升。然而，當製程達到某一極限時，這個比例縮放不再成立，功耗問題變得難以控制，從而限制了頻率和晶體管數量的增長。

4. **單核性能的提升難度**：單核性能的提升需要對微架構進行改進，例如增加指令級並行性、提升分支預測的精準度等等。這些微架構的改進越來越接近極限，提升的空間變得越來越小。因此，難以僅通過單核性能的提升來大幅增加CPU的算力。

5. **轉向多核與專用加速器**：由於單核性能的提升受限，處理器製造商更多地轉向多核處理器的設計，並增強系統的並行處理能力。然而，軟體需要針對多核架構進行特別優化，才能充分利用多核的優勢。對於許多應用來說，這種優化並不容易，導致即使CPU增加了多核，整體性能提升也未必如預期。

6. **量子極限**：隨著晶體管尺寸接近原子級別，量子效應（例如隧穿效應）變得不可忽視，這導致傳統的CMOS技術遇到很大的挑戰。而且，目前尚無成熟的替代技術可以替代CMOS來持續延續過去的增長速度。


由於CPU算力增長放緩，對於需要大量計算資源的物理工程模擬工作帶來了極大的不便。物理模擬通常需要高性能計算，依賴於快速和高效的處理器來進行複雜的數學計算和模擬，因此CPU增長速度的放緩趕不上設計複雜度的增長，這意味著模擬可能需要更長的時間才能完成。


雖然 GPU 計算能力在近年來顯著增長，特別是在深度學習和影像處理等應用中取得了突破，但許多傳統的物理工程模擬工具，諸如有限元素分析（FEA）、計算流體力學（CFD）和電磁場分析等，仍然主要依賴於 CPU 來進行運算。

這一現象可以歸結為幾個主要原因：

1. **程式架構的限制**：
   許多工程模擬工具的底層架構自設計之初便基於 CPU，其代碼經過多年的優化和驗證，直接遷移至 GPU 面臨巨大挑戰。將這些成熟的計算邏輯轉換為能利用 GPU 並行處理能力的版本，往往需要徹底的重構，這是一個費時且複雜的過程。不僅需要重寫代碼，還需進行廣泛的測試和驗證，以確保其模擬結果與原始版本一致。許多現有軟體架構並未針對 GPU 的高度並行特性進行設計，這進一步增加了遷移的難度。

2. **數值演算法的特性**：
   物理模擬中的一些數值演算法（如稀疏矩陣求解）對記憶體訪問模式有強烈依賴，而這些訪問模式往往無法充分利用 GPU 的並行架構。GPU 的優勢在於大量簡單運算的並行化處理，但針對涉及複雜數據依賴的計算，GPU 的性能未必優於 CPU。例如，稀疏矩陣求解需要頻繁且隨機地訪問內存位置，這與 GPU 的順序訪問特性並不匹配，從而限制了其應用潛力。此外，數據依賴性高的演算法使得並行化變得困難，進一步降低了 GPU 的加速效果。

3. **記憶體限制**：
   物理模擬通常需要處理非常大量的網格或節點，導致內存需求巨大。GPU 的顯存雖然速度很快，但容量有限，對於超大規模模型來說，其顯存容量成為瓶頸。一旦模型規模超出顯存容量，就需頻繁在 CPU 和 GPU 之間交換數據，這種數據傳輸會顯著降低計算效率。此外，顯存的管理也需要精細的策略，以避免不必要的資源佔用和內存浪費。

4. **開發工具和生態系統的限制**：
   開發基於 GPU 的模擬代碼需要使用專門的工具和技術（如 CUDA 或 OpenCL），這對於大多數工程模擬開發者來說是一大門檻。開發者必須具備深厚的 GPU 編程知識，並學會如何最大化利用 GPU 的性能，這需要投入大量的時間和精力。對於那些已經擁有穩定客戶群的成熟模擬軟體來說，轉換至 GPU 支持架構風險過高，尤其涉及到系統的穩定性和兼容性問題。因此，許多廠商依然選擇以 CPU 為主的運算架構。

因此，軟體廠商現階段主要從平行運算的角度進行改進，通過分散式處理將工作分配給多個 CPU 和 GPU，從而達到充分利用硬體資源的目的。如何有效地架構這些可以並行運算的分散式系統，成為未來提升模擬效率的關鍵課題。

