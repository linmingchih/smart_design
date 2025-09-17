如何使用 PyInstaller 將 Python 程式碼打包成EXE可執行檔
---
> 感謝**陳奕廷**提供此方法

使用 PyInstaller 將 PyEDB 程式碼打包成可執行檔，並解決與 pythonnet 相容性相關的問題。

### 範例程式 

這段程式碼的主要目的是透過 `pyedb` 套件操作 Ansys 的 AEDB 檔案，執行訊號與接地網路的切割，並儲存成新的 AEDB 檔案。

### 流程架構

1. 使用 `argparse` 處理命令列參數：包括輸入與輸出檔案、訊號與接地網路列表，以及指定 EDB 版本。
2. 使用 `Edb` 類別開啟 AEDB 檔案。
3. 執行 `cutout()` 方法，根據指定的訊號與接地網路進行切割。
4. 呼叫 `save_edb_as()` 儲存成新檔案，最後關閉 EDB。

### 補充說明

#### PyInstaller 打包說明與常見問題

* 使用指令：

  ```bash
  pyinstaller --onedir cutout.py
  ```

  此指令會產生一個 `cutout.exe` 以及 `_internal` 資料夾。

* 問題點：
  執行 `cutout.exe` 時會發生錯誤，原因是 `PyInstaller` 沒有自動將 `pythonnet` 套件正確打包進去。

* 解法：
  創建名為 `hook-pythonnet.py` 的檔案，內容如下：

  ```python
  from PyInstaller.utils.hooks import collect_all

  datas, binaries, hiddenimports = collect_all('pythonnet')
  ```

  並將此檔案放到 PyInstaller 預設的 hooks 目錄：

  ```
  D:\demo2\.venv\Lib\site-packages\PyInstaller\hooks
  ```

* 重新打包後，\_internal 資料夾中會包含 `pythonnet` 所需資源，程式即可正常執行。將exe連同\_internal資料夾一起移動至其他台電腦即可。

### 範例程式

```python
import argparse
from pyedb import Edb

def main():
    parser = argparse.ArgumentParser(description="Cutout nets in EDB")
    parser.add_argument("--aedb", required=True, help="Input AEDB file path")
    parser.add_argument("--version", default="2024.1", help="EDB version")
    parser.add_argument("--signals", nargs="+", required=True, help="Signal nets list")
    parser.add_argument("--grounds", nargs="+", required=True, help="Ground nets list")
    parser.add_argument("--out", required=True, help="Output AEDB path")
    args = parser.parse_args()

    # 開啟 EDB
    edb = Edb(args.aedb, edbversion=args.version)

    # 切割訊號與接地網路
    edb.cutout(args.signals, args.grounds)

    # 儲存並關閉 EDB
    edb.save_edb_as(args.out)
    edb.close_edb()

if __name__ == "__main__":
    main()
```

### 執行範例
開啟環境後，執行以下指令：
```bash
d:\demo2\dist\cutout\cutout.exe --aedb "D:/demo/Galileo_G87173_204.aedb" --signals M_DQ<0> M_DQ<1> M_DQ<2> --grounds GND --out "D:/demo2/simple.aedb"
```
![](/assets/2025-09-17_09-58-19.png)

### 匯入simple.aedb至3D Layout開啟檢查
![](/assets/2025-09-17_09-54-28.png)