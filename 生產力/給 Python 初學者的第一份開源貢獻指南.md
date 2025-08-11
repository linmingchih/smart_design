## **給 Python 開發者的第一份開源貢獻指南**


想像一下，開源專案就像一座公共圖書館，裡面的書（程式碼）由所有人共同維護。您要修正書中一個錯誤的計算公式，並附上驗算過程，確保它永遠正確。

  * **你不能直接在圖書館的書上寫字。**
  * **正確的做法是：**
    1.  跟圖書館借這本書，**影印一份**（**Fork**）。
    2.  把影印本**帶回家**（**Clone**）。
    3.  為了不把影印本弄髒，你拿出一張**新的便條紙**（**Branch**），把修正寫在上面。
    4.  在提交前，先用**自動品管員**檢查一遍（**pre-commit**）。
    5.  完成後，你把這張**便條紙連同驗算過程**（**Code & Test**）一起拿給管理員（**Pull Request**）。

這就是我們整個流程的核心概念！

#### **階段一：準備工具 (一次性設定)**

在開始之前，請確保你的電腦上裝好了這兩樣工具：

1.  **Git**：版本控制的必備工具。請至 [git-scm.com](https://git-scm.com/downloads) 下載並安裝。
2.  **GitHub 帳號**：全球最大的程式碼託管平台。請至 [github.com](https://github.com) 註冊一個免費帳號。

#### **階段二：影印並帶回家 (Fork & Clone)**

假設我們要貢獻的專案叫做 `cool-python-project`，它的擁有者是 `some-org`。

1.  **Fork 專案**：在 GitHub 頁面點擊 "Fork"。
2.  **Clone 到你的電腦**：
    ```bash
    git clone https://github.com/YOUR-USERNAME/cool-python-project.git
    ```
3.  **進入專案目錄並設定「上游」**：
    ```bash
    cd cool-python-project
    git remote add upstream https://github.com/some-org/cool-python-project.git
    ```

#### **階段三：建立乾淨的工作區與品管員**

我們要建立一個獨立的「沙盒」，並安裝所有開發和測試需要的工具。

1.  **建立並啟用虛擬環境**：

    ```bash
    python -m venv venv
    # Windows: .\venv\Scripts\activate
    # macOS/Linux: source venv/bin/activate
    ```

    啟用後，終端機提示符前會出現 `(venv)`。

2.  **安裝專案與開發工具**：
    一個好的開源專案，會把測試工具（如 `pytest`）也定義在安裝檔中。我們使用 `-e` (可編輯模式) 和 `[dev,test]` 來安裝所有需要的東西。

    ```bash
    # 這會同時安裝專案本身、pytest、pre-commit 等開發工具
    pip install -e ".[dev,test]"
    ```

    > 如果此指令失敗，請查看專案的 `README.md` 或 `CONTRIBUTING.md`，確認安裝開發依賴的正確指令。

3.  **設定自動化品管員 (pre-commit)**：
    安裝 `pre-commit` 並設定掛鉤 (Hook)，讓它在 commit 時自動檢查程式碼品質。

    ```bash
    pre-commit install
    ```

#### **階段四：在便條紙上開始工作 (含測試)**

**這是最重要的部分**：我們將採用「測試驅動」的流程來修正一個 Bug。

**情境**：我們發現一個計算總價的函數，在打折時會算錯。

1.  **建立新的分支 (Branch)**
    為這個修復任務建立一個語意清晰的分支。

    ```bash
    git checkout -b fix/calculator-discount-bug
    ```

2.  **尋找並撰寫測試 (先看著它失敗 훙)**
    我們的第一步不是修改程式碼，而是**寫一個可以抓到這個 bug 的測試**。

      * **測試檔案在哪？** 通常在專案根目錄的 `tests/` 資料夾下。
      * **檔案命名規則**：如果原始碼是 `cool_python_project/calculator.py`，那測試檔案就是 `tests/test_calculator.py`。

    讓我們在 `tests/test_calculator.py` 中加入一個測試案例：

    ```python
    # tests/test_calculator.py
    from cool_python_project.calculator import calculate_total_price

    # ... (可能已存在其他測試) ...

    def test_calculate_total_price_with_discount():
        """測試有折扣時，總價計算是否正確。"""
        # 根據目前的 bug，這個測試會失敗！
        # 預期：100元 * 2個 * (1 - 0.1折扣) = 180元
        assert calculate_total_price(price=100, quantity=2, discount_rate=0.1) == 180.0
    ```

    現在，執行測試。這是\*\*「紅燈」\*\*階段：證明問題的存在。

    ```bash
    pytest
    ```

    您應該會看到 `test_calculate_total_price_with_discount` **FAILED** 的結果。太好了！這表示我們的測試網已經成功佈下。

3.  **找到並修正程式碼 (讓測試通過)**
    現在輪到修改原始碼了。我們在 `cool_python_project/calculator.py` 中找到有問題的函數並修正它。

    ```python
    # cool_python_project/calculator.py

    # --- 原始的錯誤程式碼 ---
    # def calculate_total_price(price, quantity, discount_rate=0.0):
    #     # 錯誤的邏輯：折扣應該是乘上 (1-折扣率)，而不是直接減掉
    #     total = (price * quantity) - discount_rate
    #     return total

    # --- 修正後的正確程式碼 ---
    def calculate_total_price(price, quantity, discount_rate=0.0):
        """計算應用折扣後的商品總價。"""
        if not 0 <= discount_rate < 1:
            raise ValueError("Discount rate must be between 0 and 1.")
        
        subtotal = price * quantity
        total = subtotal * (1 - discount_rate)
        return total
    ```

    > **加分提示**：在修復 bug 的同時，順手增加像 `ValueError` 這樣的錯誤檢查，會讓您的貢獻更有價值！

4.  **再次執行測試 (確認勝利)**
    這是\*\*「綠燈」\*\*階段。回到終端機，再次執行測試：

    ```bash
    pytest
    ```

    這一次，您應該會看到所有測試，包括我們新增的那個，都顯示為 **PASSED**！這代表您不僅修復了 Bug，還確保了沒有弄壞其他功能。

#### **階段五：提交你的建議 (Add, Commit, Push, PR)**

1.  **將修改加入暫存 (Add)**
    這次我們修改了兩個檔案：原始碼和測試碼。

    ```bash
    git add .
    ```

2.  **提交變更 (Commit)**
    `pre-commit` 會在您執行此指令時自動檢查您的程式碼風格。如果失敗，請依照提示修正後（通常是再 `git add .` 一次），重新 commit。

    ```bash
    # 撰寫一個清晰的 commit message
    git commit -m "Fix(calculator): Correct discount calculation logic"
    ```

3.  **推送到你的 GitHub (Push)**

    ```bash
    git push origin fix/calculator-discount-bug
    ```

4.  **建立 Pull Request (PR)**
    回到您在 GitHub 的 Fork 頁面，點擊 "Compare & pull request"，填寫說明後送出。在說明中，您可以簡單描述您是如何透過測試發現並修復這個問題的。

#### **階段六：大功告成與後續**

恭喜！您完成了一次包含**程式碼修改**與**測試驗證**的專業級貢獻！接下來就是與專案維護者溝通，等待您的貢-獻被合併。

希望這份更完整的指南對你有幫助，勇敢踏出第一步吧！