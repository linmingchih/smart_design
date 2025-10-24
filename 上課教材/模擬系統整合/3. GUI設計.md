GUI設計
---

### GUI設計原則
GUI （Graphical User Interface，圖形用戶界面）設計在物理工程模擬軟體中扮演著重要角色。良好的GUI設計可以提升使用者體驗，使得使用者能夠更直觀地操作軟體，進行模擬設定和結果分析。 在設計GUI時，應該遵循以下幾個原則：

#### 選單
選單應該清晰且易於導航。使用者應該能夠快速找到所需的功能和設定選項。選單結構應該符合邏輯，將相關功能歸類在一起，並使用明確的標籤來描述每個選項的功能。
- Apps
    - SI Automation
    - PI Automation
- Tools
    - Script Manager    
- Help
    - Documentation
    - About

#### Tabs Panel
Tabs Panel 應該根據不同的功能模組進行劃分，使得使用者能夠方便地切換不同的功能區域。每個 Tab 應該包含與該功能相關的設定選項和操作按鈕，並且應該保持一致的佈局和風格。

不同的Apps會有不同的Tabs Panel設計，例如SI Automation可能包含以下Tabs：
- Import Design
- Setup Ports
- Setup Simulation
- Run SYZ Simulation
- Analyze IL/RL

而PI Automation可能包含以下Tabs：
- Import Design
- Setup Sources and Sinks
- Setup Simulation
- Run DCIR Simulation
- Analyze Power Tree

當中有一些是共用的Tabs，例如Import Design和Setup Simulation，這些Tabs可以設計成通用模組，方便在不同的Apps中重複使用。

另外，有些是特定於某個App的Tabs，例如Setup Ports和Analyze IL/RL，這些Tabs應該根據該App的需求進行專門設計。

#### 狀態欄

狀態欄應該顯示當前模擬的狀態和進度，讓使用者能夠隨時了解模擬的進展情況。狀態欄還可以顯示錯誤訊息和警告，幫助使用者及時處理問題。

如果可以，狀態欄還可以不同顏色來區分不同的狀態，例如綠色表示模擬正常進行，黃色表示有警告，紅色表示出現錯誤。


### GUI Prompt設計範例
在設計GUI時，可以使用AI Agent來協助生成相關的程式碼和模組。以下是一個Prompt設計範例，展示如何讓AI Agent生成一個Tabs Panel模組：

```plaintext
請幫我生成一個PySide6 GUI程式碼，最上方為選單，中間為Tabs模組應該包含以下Tabs：Import Design、Setup Ports、Setup Simulation、Run SYZ Simulation和Analyze IL/RL。每個Tab應該包含一個標籤和一個按鈕，按鈕的功能執行腳本。請確保程式碼結構清晰，並包含必要的註解。

Tab 採模組設計，放在/tabs目錄下，主程式碼放在main.py中。 gui.py負責整合選單與Tabs Panel，並處理與腳本的互動。
```

### MVC架構設計
為了提升GUI系統的可維護性和擴展性，建議採用MVC（Model-View-Controller）架構進行設計。這種架構將系統分為三個主要部分：
- Model：負責數據和業務邏輯的處理，例如模擬參數的存儲和管理。
- View：負責GUI的呈現和用戶交互，例如Tabs Panel和狀態欄的設計。
- Controller：負責協調Model和View之間的交互，例如處理用戶操作並觸發相應的模擬腳本。

這種架構有助於將不同的功能模組分離，便於開發者進行協作和擴展。例如，當需要添加新的模擬功能時，只需修改Model和Controller部分，而不需要影響View的設計。反之亦然，當需要調整GUI佈局時，只需修改View部分，而不會影響模擬邏輯。

### GUI 修改與擴展

實際工程可能會隨著需求變化而不斷調整，因此GUI設計應該具備良好的可修改性和擴展性。當需要添加新的功能或修改現有功能時，應該能夠方便地進行調整，而不會影響整個系統的穩定性。

要修改功能或是添加新的Tabs，可以參考以下prompt範例：

```plaintext
請幫我修改/tabs目錄下的gui.py程式碼，新增一個名為“Setup Simulation”的Tab。該Tab應該包含一個標籤和一個按鈕，按鈕的功能是執行setup_simulation.py腳本。請確保程式碼結構清晰，並包含必要的註解。
```

### QT Widgets設計
在設計GUI時，可以使用QT Widgets來實現各種界面元素，例如按鈕、標籤、輸入框等。QT Widgets提供了豐富的組件和功能，可以滿足不同的界面設計需求。在設計Tabs Panel時，可以使用QTabWidget來實現多個選項卡的切換功能。每個Tab可以包含不同的QT Widgets，例如QLabel用於顯示標籤，QPushButton用於觸發腳本執行等。   

以下是常用的QT Widgets及其用途：
- QPushButton：用於創建按鈕，觸發特定的操作。
- QLabel：用於顯示文本或圖像。
- QLineEdit：用於輸入單行文本。
- QTextEdit：用於輸入多行文本。
- QComboBox：用於創建下拉選單，讓使用者選擇一個選項。
- QTabWidget：用於創建多個選項卡，方便切換不同的功能區域。
- QStatusBar：用於顯示狀態信息和進度。
- QMenuBar：用於創建選單欄，包含各種功能選項。
- QVBoxLayout / QHBoxLayout：用於佈局QT Widgets，控制它們的排列方式。
- QGridLayout：用於創建網格佈局，方便排列多個QT Widgets。
- QCheckBox：用於創建複選框，讓使用者選擇多個選項。
-QRadioButton：用於創建單選按鈕，讓使用者在多個選項中選擇一個。
-QGroupBox：用於將相關的QT Widgets分組，提升界面的組織性。
-QSlider：用於創建滑動條，讓使用者調整數值範圍。
-QProgressBar：用於顯示進度條，反映操作的完成程度。
-QFileDialog：用於打開文件對話框，讓使用者選擇文件或目錄。
-QMessageBox：用於顯示消息框，提供提示、警告或錯誤信息。

在prompt中指定的QT Widgets，可以有效地設計和實現GUI界面，提升使用者體驗和操作效率。

