Lab1 建立虛擬環境並安裝 PyOptiSLang 與相關工具
---

# 

## 一、目的

本文件說明如何使用 ANSYS 內建的 CPython 建立獨立的 Python 虛擬環境，並安裝以下套件：

* `pyaedt`（AEDT 自動化核心）
* `ansys-optislang-core`（OptiSLang Python API）
* `spyder`（開發與除錯 IDE）

此流程適用於：

* 避免污染系統 Python
* 確保與 AEDT 相容的 Python 環境
* 建立可重現的開發環境

---

## 二、環境前提

請確認以下條件：

* 已安裝 ANSYS Electronics Desktop（版本 v252）
* 有系統管理員權限（建議）
* 網路可連線（或已準備離線套件）

---

## 三、步驟說明

### Step 1：進入 ANSYS 內建 Python

```bash
cd "C:\Program Files\ANSYS Inc\v252\optiSLang\lib\python3.10"
```

**說明：**

* ANSYS 提供官方測試過的 CPython 環境（3.10）
* 使用此 Python 可避免版本不相容問題
* 後續虛擬環境將基於此 Python 建立

---

### Step 2：建立虛擬環境

```bash
.\python -m venv c:\0416
```

**說明：**

* 在 `C:\0416` 建立一個新的虛擬環境
* 該環境包含：

  * 獨立 Python interpreter
  * 獨立 site-packages

📌 建議命名方式：

* `C:\venv\pyaedt_env`
* `C:\envs\aedt_2025`

---

### Step 3：進入虛擬環境 Script 目錄

```bash
cd c:\myvenv\Scripts
```

⚠️ 注意：

你前面建立的是 `c:\0416`，這裡應一致：

```bash
cd c:\0416\Scripts
```

---

### Step 4：啟動虛擬環境

```bash
activate
```

啟動後會看到：

```bash
(0416) C:\0416\Scripts>
```

**說明：**

* 所有後續 `pip install` 都會安裝在此環境中
* 不會影響系統 Python

---

### Step 5：安裝 PyAEDT

```bash
pip install pyaedt[all]
```

**功能：**

* 提供 AEDT automation API
* 支援 HFSS / SIwave / Q3D / Icepak 等

---

### Step 6：安裝 OptiSLang Core API

```bash
pip install ansys-optislang-core
```

**功能：**

* Python 控制 OptiSLang
* 用於最佳化流程、自動化設計空間探索

---

### Step 7：安裝 Spyder IDE

```bash
pip install spyder
```

**功能：**

* 類 MATLAB 的 Python IDE
* 支援：

  * variable explorer
  * debugger
  * interactive console

---

### Step 8：啟動 Spyder

```bash
.\spyder
```

或

```bash
spyder
```

**結果：**

* Spyder 會使用目前虛擬環境作為 Python kernel
* 可直接 import PyAEDT 進行開發