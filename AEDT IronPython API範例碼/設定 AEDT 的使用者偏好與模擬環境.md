設定 AEDT 的使用者偏好與模擬環境
---
### 目的
透過 AEDT 的 `SetRegistryString` 與 `SetRegistryInt` 方法，直接修改內部設定（儲存在 XML 設定檔中），以自動化並統一模擬環境配置。

### 功能
這段程式主要是：
- 設定 HFSS 的 DSO 組態
- 指定 HPC 授權模式為 Pack
- 啟用「佇列所有模擬」功能
- 設定自動儲存間隔為 10 分鐘
- 設定預設的腳本副檔名為 `.py`
- 關閉 AEDT 啟動時的歡迎畫面

### 流程架構
1. 透過 `oDesktop` 物件操作 AEDT 的內部註冊表（類似偏好設定）
2. 分別設定字串與整數類型的項目
3. 這些設定會反映在對應的 XML 檔中，例如："D:\OneDrive - ANSYS, Inc\Documents\Ansoft\ElectronicsDesktop2025.2\config\EUgTEAAPvhWvmV_user.XML"

### 補充說明
- `SetRegistryString(key, value)`：設定某一設定項目的字串值。
- `SetRegistryInt(key, value)`：設定整數值，例如開關（0 或 1）。
- 這些設定會即時套用到 AEDT 中，且不需手動編輯 XML。
- 可以用來建立自動化流程，確保模擬環境一致。

### 範例程式
```python
# 設定 HFSS 的 DSO 使用本機模式
oDesktop.SetRegistryString("Desktop/ActiveDSOConfigurations/HFSS", "Local")

# 使用 Pack 類型的 HPC 授權
oDesktop.SetRegistryString("Desktop/Settings/ProjectOptions/HPCLicenseType", "Pack")

# 啟用佇列所有模擬的功能
oDesktop.SetRegistryInt("Desktop/Settings/ProjectOptions/QueueAllSimulations", 1)

# 設定自動儲存的時間間隔為 10 分鐘
oDesktop.SetRegistryInt("Desktop/Settings/ProjectOptions/AutoSaveInterval", 10)

# 預設的腳本副檔名為 .py
oDesktop.SetRegistryString("Desktop/Settings/ProjectOptions/RunScriptDefaultExtension", "py")

# 關閉歡迎訊息
oDesktop.SetRegistryInt("Desktop/Settings/ProjectOptions/ShowWelcomeMsg", 0)
```

這樣的程式碼可以在 AEDT 開啟後的初始化腳本中執行，達成快速配置的目的。
