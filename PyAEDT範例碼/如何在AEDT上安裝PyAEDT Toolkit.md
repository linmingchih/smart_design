如何在AEDT上安裝PyAEDT Toolkit
---
> 2024/9/21

ANSYS AEDT 提供內建的腳本錄製與撥放功能(圖一紅框)，讓使用者能快速自動化重複性的操作。錄製功能會記錄使用者在圖形介面中的每一個操作，並將其轉換為Python腳本。這些腳本可以用來重複執行相同的步驟，無需手動操作，減少錯誤並節省時間。錄製好的腳本可以在AEDT內直接播放，亦可根據需求進行編輯和擴充功能。這項功能對於處理大量相似的模擬任務，或需要進行批量處理時非常實用，適合提高工作效率並簡化流程。

![2024-09-21_11-21-17](/assets/2024-09-21_11-21-17_m7zh2rs2c.png)

然而，該錄製與執行功能僅支援 Classical API 的腳本。如果是使用 PyAEDT API 編寫的 Python 腳本，則無法執行。


>:memo:**附註** 於 2024R2 版本中，PyAEDT 模組尚未整合至 AEDT 安裝包內，下一個版本或許將支援此功能。

現階段若要執行 PyAEDT 腳本，則需先安裝 PyAEDT 工具包。首先，在AEDT找到上圖黃色框線中的 "Install PyAEDT" 按鈕並點擊，該按鈕將導引至官方網站。在網站上可以下載名為 pyaedt_installer_from_aedt.py 的腳本。

![2024-09-21_11-34-53](/assets/2024-09-21_11-34-53.png)


下載後，在 AEDT 中使用紅框中的 "Run Script" 功能來執行該腳本。安裝完成後，您將在下圖的綠框位置看到 PyAEDT Toolkit，代表工具包已成功安裝並可用於進一步的自動化操作。

![2024-09-21_11-33-11](/assets/2024-09-21_11-33-11.png)

### PyAEDT Toolkit

在上圖中的 PyAEDT Toolkit 中，綠框內包含四個主要按鈕，每個按鈕的功能如下：
 
1. **PyAEDT Console** ：開啟 PyAEDT 控制台，讓使用者可以在 AEDT 環境中直接執行 Python 命令與 PyAEDT API。這個功能方便用於即時測試腳本或進行互動式的模擬控制。
 
2. **Jupyter Notebook** ：開啟 Jupyter Notebook 環境，讓使用者能夠在一個交互的筆記本內撰寫和執行 PyAEDT 相關的 Python 腳本，適合進行實驗或較長的工作流程。
 
3. **Run PyAEDT Script** ：運行已撰寫好的 PyAEDT 腳本。透過這個按鈕，使用者可以選擇並直接執行本地的 Python 腳本，進行批次處理或自動化模擬。
 
4. **Extension Manager** ：用於管理和安裝額外的擴充功能或模組，方便使用者為 AEDT 添加額外的功能或模組，進一步增強 PyAEDT 的應用。

### 安裝細節補充
腳本安裝過程會在每位使用者的個人目錄中建立一個虛擬環境，並安裝所需的套件，包括 `pyaedt`、`ipython` 和 `notebook`。此外，該腳本會在 AEDT 的 `PersonalLib` 目錄中安裝 Toolkit 的按鈕圖片，並建立這些按鈕與虛擬環境中工具的連結。由於虛擬環境和設定位於個人目錄中，因此不同的用戶需要各自執行此安裝流程，以確保環境與 PyAEDT 工具的正確配置和使用。

#### IT統一安裝PyAEDT Toolkit (以Linux為例)

在IT嚴格管理的公司中，為了讓所有 AEDT 使用者都能共用 PyAEDT Toolkit，而不需要每位使用者個別安裝，可以按照以下步驟進行一次性安裝：
 
1. **建立虛擬環境** ：IT 管理員可以利用 Python 3.10 在自訂的目錄上建立虛擬環境，並更新 pip 套件管理工具。

2. **激活虛擬環境** ：使用 `source activate` 來激活虛擬環境，
3. **安裝 PyAEDT、IPython 及 Notebook** ：使用 pip 進行線上安裝，pip 會根據作業系統自動選擇適當的版本來安裝相關套件。具體安裝指令如下：

```bash
pip install pyaedt
pip install ipython
pip install notebook
```

4. **安裝 PyAEDT Toolkit** ：接著輸入 `python` 進入 Python Console，使用以下兩行 Python 指令來將 PyAEDT Toolkit 安裝至 AEDT 工具列中。需要注意的是，`syslib` 目錄應是 AEDT v242 安裝路徑中的 Toolkit 擺放目錄，並且執行這些指令的帳號需要具備寫入權限。

```python
from ansys.aedt.core.workflows.installer.pyaedt_installer import add_pyaedt_to_aedt
add_pyaedt_to_aedt("2024.2", r"/AnsysEM/v242/Linux64/syslib")
```
 
5. **確認安裝完成** ：當安裝完成後，啟動 AEDT，所有使用者便都可以在圖形介面中看到 PyAEDT Toolkit 的圖示 (icons)，這樣就實現了多用戶共用的安裝方式。

這樣的集中管理模式適合那些對使用者軟體安裝權限有嚴格控制的企業，同時又能確保所有 AEDT 使用者能夠方便使用 PyAEDT 的自動化功能。