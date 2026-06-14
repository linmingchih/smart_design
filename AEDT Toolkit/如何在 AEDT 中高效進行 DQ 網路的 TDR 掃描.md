# AEDT Toolkit 腳本文件模板 (ss)
---

**Linux/Windows AEDT 適用**

<!-- 請替換為腳本執行結果或說明的截圖 -->
![腳本截圖](/assets/placeholder.png)

> **操作參考影片**
<!-- 若有影片教學，請在此放入影片縮圖與連結 -->
[![影片](https://img.youtube.com/vi/YOUR_VIDEO_ID/hqdefault.jpg)](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)

> :link: **下載**
<!-- 請替換為實際的 Python 腳本檔案連結 -->
[ss_script.py](/assets/ss_script.py)

---

## 📖 功能說明
在此處詳細描述此腳本 (`ss.py`) 的主要功能與解決的問題。例如：此腳本可用來自動化處理 S-parameter (S參數) 的匯出與分析，節省繁瑣的手動操作時間。

## 🛠️ 使用方法
1. 打開 AEDT (建議版本 2023 R1 或以上)。
2. 開啟您的目標專案 (Project) 與設計 (Design)。
3. 進入 **Automation** > **Run Script**。
4. 選擇下載的 `ss_script.py` 檔案並執行。

## 📝 程式碼範例 (Optional)
若有核心代碼需要特別說明，可以放在此處：

```python
import pyaedt

# 初始化 AEDT
app = pyaedt.Hfss(specified_version="2023.1", non_graphical=False)

# 您的核心邏輯
app.logger.info("腳本執行成功！")

# 釋放資源
app.release_desktop()
```
