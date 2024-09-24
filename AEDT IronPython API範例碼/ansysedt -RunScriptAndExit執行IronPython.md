ansysedt -RunScriptAndExit執行IronPython
---
ANSYS Electronics Desktop (AEDT) 執行 IronPython 腳本的兩種方式如下：
 
1. **在 GUI 當中執行 `test.py`** ：
  - 你可以直接在 AEDT 的圖形介面 (GUI) 裡，通過 "Tools" -> "Run Script" 選擇並執行 Python 腳本。這個方法適合在 GUI 中即時調試或需要視覺化結果的場合。
 
2. **在 Command Window 中以 `ansysedt -RunScriptAndExit test.py`** ：
  - 這個方法可以透過命令列執行 Python 腳本並自動退出 AEDT。適合用於批次處理或自動化流程，尤其是在不需要 GUI 介面的情況下。
 
  - 執行範例：

```bash
"C:\Program Files\AnsysEM\v241\Win64\ansysedt.exe" -RunScriptAndExit C:\path\to\test.py
```

兩者的區別在於執行場景：GUI 提供即時互動與可視化，命令列則適合自動化與批次處理。

### 背景模式執行

使用 `-ng` 參數可以支援 non-graphical 模式，不會開啟 GUI。這樣可以在背景執行腳本，節省系統資源並加速處理，特別適合自動化流程。指令如下：

```bash
ansysedt.exe -feature=beta -ng -RunScriptAndExit test.py
```
 
- **`-ng`** : 表示 non-graphical 模式，不會啟動 AEDT 的圖形介面。
 
- **`-RunScriptAndExit test.py`** : 執行 Python 腳本 `test.py` 並在腳本執行完成後退出。

這樣的配置非常適合用於批次運算、腳本自動化或大型模擬的情境，並且能節省系統資源。

### 傳遞參數
當你在命令列使用 `-scriptargs` 傳遞參數進IronPython腳本時，該參數會作為單一字串傳入 `ScriptArgument` 變數中，並且你可以透過 `split()` 方法來將該字串分割為多個部分。
具體來說，這段代碼：


```python
aedt_path, design_name = ScriptArgument.split()
```
是將 `ScriptArgument` 中的字串以空白字元進行分割，並將結果分別賦值給 `aedt_path` 和 `design_name` 兩個變數。也就是說，你在命令列使用 `-scriptargs` 傳遞的參數如果是這樣的格式：

```bash
ansysedt.exe -RunScriptAndExit test.py -scriptargs "C:/path/to/aedt_file Design1"
```
那麼在腳本中，`ScriptArgument` 的值將是 `"C:/path/to/aedt_file Design1"`。當執行 `split()` 之後，`aedt_path` 會被賦值為 `"C:/path/to/aedt_file"`，而 `design_name` 會被賦值為 `"Design1"`。如果你的 `-scriptargs` 中有多個參數以空白分隔，這種方式可以方便地提取出每個參數並進行進一步處理。