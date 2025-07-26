## 用 ChatGPT 深度研究查找API

在現代高頻電子系統設計中，模擬自動化是提升效率與精度的核心手段。Ansys 推出的 PyAEDT 與 PyEDB 函式庫，作為其 Electronics Desktop (AEDT) 平台的 Python 介面，為研究人員與工程師提供了強大的模型建構與模擬控制能力。然而，由於這些函式庫涵蓋眾多模組且文件繁雜，要快速查找特定 API 的結構與功能仍具挑戰。本文旨在示範如何整合 GitHub 原始碼、大型語言模型（LLM）以及互動式開發環境（IDE），以系統化地剖析 PyAEDT 與 PyEDB 的 API。我們將以「導體粗糙度設定」為具體範例，展示完整的探索與應用流程。


### **第一步：建立 GitHub 帳號並 Fork 相關專案**

首先，請造訪 Ansys 的官方 GitHub 倉庫：

*   **pyaedt:** `https://github.com/ansys/pyaedt`
*   **pyedb:** `https://github.com/ansys/pyedb`

接著，執行以下步驟：

1.  **登入 GitHub 帳號** 。
2.  點擊頁面右上角的 **`Fork`** 按鈕，將專案複製到您的個人帳號下。此舉有助於ChatGPT後續進行倉庫連結及讀取。

![2025-07-26_21-32-48](/assets/2025-07-26_21-32-48.png)

### **第二步：連接 AI 模型與您的 GitHub 倉庫**

若您使用 ChatGPT Plus，可以將其與您的私有或公開 repository 連接，從而實現以自然語言查詢程式碼的功能。

1.  在 AI 模型的操作介面中，找到相關的外部應用或連接器設定。
2.  選擇連接 GitHub，並授權該應用程式存取您的 GitHub 倉庫。


![2025-07-26_21-34-25](/assets/2025-07-26_21-34-25.png)
#### **第三步：透過自然語言查詢探索 API 結構與用法**

![2025-07-26_21-35-49](/assets/2025-07-26_21-35-49.png)

以「導體粗糙度設定」為例，您可以透過**深入研究**並設定**資料來源**到PyAEDT倉庫並提出以下問題：

```
如何在 PyAEDT 中，為一個導體表面指派有限導體邊界條件 (Finite Conductivity) 並設定其粗糙度 (Roughness) 參數？
```

AI 模型會根據其分析的 GitHub 專案內容，提供具體的程式碼範例，例如：

```python
from pyaedt import Hfss

# 初始化 HFSS 專案
hfss = Hfss(version="2025.1")

# 建立一個金屬盒作為範例幾何
box = hfss.modeler.create_box(
    position=[0, 0, 0],
    dimensions_list=[10, 10, 1],
    name="MetalBox",
    matname="copper"
)

# 指派 Coating 邊界條件並設定粗糙度
# 此處的 Coating 等同於在 UI 中設定有限導體邊界
hfss.assign_coating(
    obj="MetalBox",
    mat="copper",
    roughness="5um"
)
```

上述指令的意涵是：對名為 `MetalBox` 的物件表面，施加一層以 `copper` 材質定義的 `Coating` 邊界，並將其表面粗糙度設定為 5 微米。



### **第四步：在 IDE 中驗證與除錯**

將前述程式碼複製到您慣用的 IDE (如 Spyder、VS Code 或 PyCharm) 中執行。首先確認 AEDT 能夠正常啟動，接著檢查幾何模型與邊界條件是否已如預期般建立。

若執行時發生錯誤，可利用 IDE 的 **全文搜尋功能** 或直接在 GitHub 專案頁面中查找 `assign_coating` 函式的定義。通常，這類函式會位於 `Boundary.py` 或 `Analysis3D.py` 等模組檔案中。透過檢視原始碼，您可以確認其支援的參數、預期的資料型別與單位格式，從而完成除錯。

![2025-07-26_21-39-19](/assets/2025-07-26_21-39-19.png)

### **結語**

整合原始碼、語意 AI 與互動式開發環境，可以建立一套高效率且具可重複性的函式庫學習與應用流程。此方法不僅適用於 PyAEDT 與 PyEDB，也能廣泛應用於其他科學計算工具的探索，具備高度的實用性與推廣潛力。