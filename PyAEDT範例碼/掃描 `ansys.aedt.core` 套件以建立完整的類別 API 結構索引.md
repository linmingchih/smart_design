掃描 `ansys.aedt.core` 套件以建立完整的類別 API 結構索引
---

**目的**

此工具用來自動化盤點 ANSYS AEDT Python API（`ansys.aedt.core`）中的所有類別，彙整每個類別的：

* 文件字串（docstring）
* 建構子與方法（參數型別、預設值、回傳型別）
* 屬性（@property 的回傳型別）

輸出為 `aedt_core_api_database.json`，方便製作文檔、建立 API 瀏覽器、或進一步做靜態分析。

---

### 功能

* **套件檢查**：確認 `ansys.aedt.core` 是否可匯入，若無則提示安裝 `pyaedt`。
* **模組遍歷**：用 `pkgutil.walk_packages` 遞迴列舉 `ansys.aedt.core` 底下所有子模組並匯入。
* **類別過濾**：僅針對 `__module__` 前綴為 `ansys.aedt.core` 的類別，避免誤收外部相依。
* **API 抽取**：

  * `__init__` 參數型別 / 預設值、方法與屬性文件與回傳型別。
  * 忽略私有成員（以 `_` 開頭）但保留 `__init__`。
* **型別轉字串**：支援現代/舊式泛型（`list[str]`、`dict[str, int]`、`str | None`、`typing.Union` 等）。
* **錯誤容忍**：面對 C 擴充（無法被 `inspect`）或回溯錯誤時不中斷流程，記錄錯誤資訊。
* **JSON 輸出**：將結果以 UTF-8、美觀縮排輸出成檔。

---

### 流程架構

1. **初始化與安全匯入**：嘗試 `import ansys.aedt.core as aedt_core`，失敗則印出指引後 `sys.exit(1)`。
2. **走訪模組**：以 `walk_packages(path=aedt_core.__path__, prefix=aedt_core.__name__ + '.')` 列舉子模組並逐一 `importlib.import_module`。
3. **提取類別**：在每個模組使用 `inspect.getmembers(module, inspect.isclass)` 找類別；僅保留 `module` 前綴符合的類別。
4. **分析類別**：

   * **建構子 `__init__`**：`inspect.signature` 取得參數（略過 `self`），記錄型別與預設值。
   * **方法**：公開方法的參數與回傳型別。
   * **屬性**：對 `property` 以其 `fget` 的簽章解出回傳型別。
5. **型別名稱標準化**：透過 `get_type_name` 處理 `GenericAlias`（`list[str]`）、`UnionType`（`str | None`）、`typing._GenericAlias`（`typing.List[str]`）、`typing.Union` 等。
6. **結果去重與儲存**：以「實際模組路徑 + 類別名」作 key 去重，最後寫入 `aedt_core_api_database.json`。

---

### 補充說明

* **為何要特別處理型別提示？**
  Python 3.9 之後引入 `list[str]` 這種語法（`types.GenericAlias`），3.10 又加入 `X | Y`（`types.UnionType`）。而舊程式碼常見 `typing.List[str]`、`typing.Union[str, None]`。`get_type_name` 的目的就是把各個版本的寫法都「統一成可讀字串」。
* **`__origin__` 與 `__args__`**：

  * `__origin__` 指向基礎型別（如 `list`、`dict`、`typing.Union`）。
  * `__args__` 是泛型參數（如 `list[str]` 的 `str`，`dict[str, int]` 的 `str, int`）。
* **無法被 `inspect` 的情況**：
  由 C/C++ 綁定的方法/建構子常取不到簽章，程式以 try/except 捕捉並在輸出中以 `error` 欄位標示，確保流程不中斷。
* **私有成員過濾**：
  以名稱前綴 `_` 判斷並略過，避免把內部細節混入公開 API 清單。
* **效能與實務建議**：

  * 可加入模組/類別白名單以縮小掃描範圍。
  * 遇到大型套件時，可將結果分檔或增量更新（例如先存每個模組一份，再彙整）。
  * 若要顯示進度，可整合 `tqdm` 或使用自家 logger。

---

### 範例程式

```python
import inspect
import importlib
import pkgutil
import json
import sys
import types  # 用於類型提示分析
import typing # 用於類型提示分析

# 關鍵更改：我們導入 ansys.aedt.core 而不是 pyaedt
# 您必須已安裝 ansys-aedt-core (通常會隨 pyaedt 一起安裝)
try:
    import ansys.aedt.core as aedt_core
except ImportError:
    print("錯誤：找不到 'ansys.aedt.core' 套件。")
    print("請確保已安裝最新版本的 pyaedt (pip install pyaedt)")
    sys.exit(1)


def get_type_name(annotation):
    """(已改進) 將類型提示轉換為字串，支援 Python 3.10+"""
    if annotation == inspect.Parameter.empty:
        return "ANY"

    # 處理現代泛型 (e.g., list[str], dict[str, int], Union[str, None])
    # types.GenericAlias 是 Python 3.9+ 的 list[str]
    # types.UnionType 是 Python 3.10+ 的 str | None
    # typing._GenericAlias 是舊版 typing.List[str]
    if isinstance(annotation, (types.GenericAlias, getattr(typing, '_GenericAlias', type(None)), getattr(types, 'UnionType', type(None)))):
        
        # 獲取基礎類型名稱 (e.g., 'list', 'dict', 'Union')
        if hasattr(annotation, '__origin__'):
            name = get_type_name(annotation.__origin__)
        else:
            name = str(annotation) # Fallback

        args = getattr(annotation, '__args__', [])
        
        if not args:
            return name
        
        # 處理特殊情況 e.g., tuple[str, ...]
        if len(args) == 2 and args[1] == Ellipsis:
            return f"{name}[{get_type_name(args[0])}, ...]"
        
        # 組合泛型 e.g., list[str], dict[str, int]
        return f"{name}[{', '.join(get_type_name(arg) for arg in args)}]"

    # 處理 typing.Union (Python 3.9 及更早版本)
    if hasattr(annotation, '__origin__') and annotation.__origin__ == typing.Union:
        args = getattr(annotation, '__args__', [])
        if not args: return "Union"
        return f"Union[{', '.join(get_type_name(arg) for arg in args)}]"

    # 處理簡單類型 (int, str) 和自定義類別
    if hasattr(annotation, '__module__') and hasattr(annotation, '__name__'):
        if annotation.__module__ == 'builtins':
            return annotation.__name__
        return f"{annotation.__module__}.{annotation.__name__}"
    
    # Fallback
    return str(annotation)


def analyze_class(class_obj):
    """分析單個類別並回傳其 API 結構"""
    if not inspect.isclass(class_obj):
        return None
        
    api_info = {
        "doc": inspect.getdoc(class_obj),
        "methods": {},
        "properties": {}
    }
    
    # 增加對 __init__ 的分析
    try:
        init_sig = inspect.signature(class_obj.__init__)
        params = {}
        for pname, p in init_sig.parameters.items():
            if pname == 'self':
                continue
            params[pname] = {
                "type": get_type_name(p.annotation),
                "default": repr(p.default) if p.default != inspect.Parameter.empty else "REQUIRED"
            }
        api_info["methods"]["__init__"] = {
            "doc": inspect.getdoc(class_obj.__init__),
            "params": params,
            "return_type": "None"
        }
    except (ValueError, TypeError):
         # 很多底層的 __init__ (例如 C 綁定的) 無法被 inspect
         api_info["methods"]["__init__"] = {"error": "Could not inspect __init__"}


    for name, member in inspect.getmembers(class_obj):
        if name.startswith('_') and name != '__init__': # 允許 __init__
            continue # 忽略私有成員

        try:
            # 1. 分析屬性 (Properties)
            if isinstance(member, property):
                if member.fget:
                    sig = inspect.signature(member.fget)
                    return_type = get_type_name(sig.return_annotation)
                else:
                    return_type = "ANY" 
                    
                api_info["properties"][name] = {
                    "doc": inspect.getdoc(member),
                    "return_type": return_type
                }

            # 2. 分析方法 (Methods)
            elif (inspect.isfunction(member) or inspect.ismethod(member)) and name != '__init__': # 已處理過 __init__
                sig = inspect.signature(member)
                params = {}
                for pname, p in sig.parameters.items():
                    if pname == 'self':
                        continue
                    params[pname] = {
                        "type": get_type_name(p.annotation),
                        "default": repr(p.default) if p.default != inspect.Parameter.empty else "REQUIRED"
                    }
                
                api_info["methods"][name] = {
                    "doc": inspect.getdoc(member),
                    "params": params,
                    "return_type": get_type_name(sig.return_annotation)
                }
                
        except (ValueError, TypeError, AttributeError) as e:
            # 很多 C++ 綁定的方法無法被 inspect
            if isinstance(member, property):
                api_info["properties"][name] = {"error": f"Could not inspect (Error: {e})"}
            else:
                api_info["methods"][name] = {"error": f"Could not inspect (Error: {e})"}
            
    return api_info

# --- 主執行緒 ---
def crawl_aedt_core():
    print(f"Starting to crawl 'ansys.aedt.core' package...")
    database = {}
    
    # 關鍵更改：使用 aedt_core
    package = aedt_core
    
    # 遍歷 ansys.aedt.core 套件下的所有模組
    for importer, modname, ispkg in pkgutil.walk_packages(path=package.__path__,
                                                         prefix=package.__name__ + '.',
                                                         onerror=lambda x: None):
        try:
            module = importlib.import_module(modname)
            print(f"Inspecting module: {modname}")
            
            # 遍歷模組中的所有成員，找出所有類別
            for class_name, class_obj in inspect.getmembers(module, inspect.isclass):
                
                # 檢查類別是否 *屬於* ansys.aedt.core 套件
                if class_obj.__module__.startswith(package.__name__):
                    
                    # 使用類別的 *實際* 模組路徑 + 類別名稱作為 key
                    full_class_name = f"{class_obj.__module__}.{class_name}"
                    
                    # 檢查是否已經分析過 (避免重複)
                    if full_class_name not in database:
                        print(f"  -> Analyzing class: {full_class_name}")
                        api_data = analyze_class(class_obj)
                        if api_data:
                            database[full_class_name] = api_data
                        
        except ImportError as e:
            print(f"Could not import {modname}: {e}", file=sys.stderr)
        except Exception as e:
            # 打印更詳細的錯誤日誌，以便追蹤
            print(f"Error inspecting module {modname} (Class: {class_name}): {e}", file=sys.stderr)
            import traceback
            traceback.print_exc(file=sys.stderr)


    print("Crawl complete. Saving database...")
    # 更改: 輸出檔案名稱
    with open("aedt_core_api_database.json", "w", encoding="utf-8") as f:
        json.dump(database, f, indent=2, ensure_ascii=False)
        
    print("Database saved to 'aedt_core_api_database.json'")

# --- 執行爬蟲 ---
if __name__ == "__main__":
    # 更改: 呼叫的函數名稱
    crawl_aedt_core()
```

> 產出檔：`aedt_core_api_database.json`，為 `ansys.aedt.core` 全套件中可被 `inspect` 的類別 API 概覽。
