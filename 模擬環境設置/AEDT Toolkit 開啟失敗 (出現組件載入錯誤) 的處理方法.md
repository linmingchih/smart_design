AEDT Toolkit 開啟失敗 (出現組件載入錯誤) 的處理方法
---

### 1. 問題概要

在 **ANSYS Electronics Desktop (AEDT)** 中開啟部分 **Toolkit** 時，可能會出現以下錯誤訊息：

```
TypeLoadException: 因為父類型不存在，無法載入組件 'System.Private.CoreLib, Version=6.0.0.0,
Culture=neutral, PublicKeyToken=7cec85d7bea7798e' 載入類型 'System.Object'
In file "C:\Program Files\ANSYS Inc\v252\AnsysEM\syslib\Toolkits\CircuitDesign\Maxwell RL Component.py", line 12
```
![](/assets/2025-09-22_08-55-55.png)

這代表 **AEDT 嘗試載入的 .NET 執行環境版本與實際環境不符**，導致 Toolkit 初始化失敗。


### 2. 問題原因

1. **.NET 版本衝突**

   * AEDT 本身是以 **.NET Framework** 為基礎開發，但部分 Toolkit 腳本可能會呼叫 **.NET Core / .NET 6+** 元件。
   * 如果環境變數 `DOTNET_ROOT` 被設定為指向錯誤的 .NET Core 版本，就會發生 **TypeLoadException**。

2. **Windows 升級後相容性問題**

   * 從 **Windows 10 升級到 Windows 11** 之後，部分舊版 AEDT 或 Toolkit 仍假設使用特定版本的 .NET Framework，造成相容性錯誤。


### 3. 解決方法與 Workaround

在啟動 AEDT 前，先清除環境變數，避免 AEDT 誤用 .NET Core 執行環境。

建立一個批次檔，例如 `Launch_AEDT.bat`：

```bat
@echo off
:: 清除 DOTNET_ROOT，避免 Toolkit 使用錯誤的 .NET Core 執行環境
set DOTNET_ROOT=

:: 確保使用系統預設的 .NET Framework
set PATH=C:\Windows\system32;C:\Windows

:: 啟動 AEDT (請依照實際版本修改路徑)
start "" "C:\Program Files\ANSYS Inc\v252\AnsysEM\ansysedt.exe"
```

> ✅ 建議為不同版本的 AEDT（例如 v241, v252）各建立一個專屬批次檔，避免手動修改。



### 4. 注意事項

* 若錯誤僅在「部分 Toolkit」出現，代表這些 Toolkit 使用了與當前環境不相容的 .NET API。
* 官方更新或 Hotfix 可能會修正此問題，建議定期檢查 ANSYS 下載中心。
* 若仍無法解決，請聯繫 ANSYS 技術支援，並提供 **AEDT 版本、Windows 版本、已安裝的 .NET 版本**等資訊。




