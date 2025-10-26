`pyedb` 套件 API 文件產生器
---

這段程式碼的目的是自動掃描 `pyedb` 套件底下所有自訂的 Python 類別，分析其公開方法與屬性，並將這些資訊整理成 JSON 格式的 API 文件，儲存成一個檔案。這對於了解一個大型套件的架構或產生開發文件非常有幫助。可以提供給AI Agent或其他工具進行後續處理。

### 功能

* 掃描 `pyedb` 套件內所有模組與子模組
* 取得每個類別的註解、方法與屬性
* 將類別的 API 結構轉為 JSON 格式
* 儲存為 `pyedb_api_database.json`

### 流程架構

1. **主程式入口：** 執行 `crawl_pyedb()` 函式啟動整個流程。
2. **模組遞迴：** 使用 `pkgutil.walk_packages()` 遍歷 `pyedb` 所有子模組。
3. **類別篩選：** 找出每個模組中自己定義的類別（排除從其他模組 import 的）。
4. **類別分析：** 對每個類別使用 `analyze_class()` 擷取其公開方法與屬性：

   * 屬性：使用 `property` 判斷、取得回傳型別與註解。
   * 方法：使用 `inspect.signature` 擷取參數、型別與預設值，並記錄註解與回傳型別。
5. **錯誤處理：** 對於無法被分析的 C 綁定類別或特殊情況會略過或標記錯誤。
6. **輸出儲存：** 將結果存成 JSON 檔案。

### 補充說明

* `inspect` 模組：提供一組工具來檢查物件的內容，例如函式簽名與型別註解。
* `pkgutil.walk_packages()`：可用來遞迴尋找指定套件中的所有模組。
* 類別型別提示的處理使用 `__module__`, `__name__`, 以及 `_name` 判斷是否為泛型。
* 無型別註解的參數會標示為 `ANY`。
* 預設參數會顯示其值，沒有的則標記為 `REQUIRED`。

### 範例程式

```python
import inspect
import importlib
import pkgutil
import json
import pyedb  # 必須安裝 pyedb

def get_type_name(annotation):
    if annotation == inspect.Parameter.empty:
        return "ANY"
    if hasattr(annotation, '__module__'):
        if hasattr(annotation, '_name') and annotation._name == 'List':
            args = getattr(annotation, '__args__', [])
            if args:
                return f"list[{get_type_name(args[0])}]"
            return "list"
        return f"{annotation.__module__}.{annotation.__name__}"
    return str(annotation)

def analyze_class(class_obj):
    if not inspect.isclass(class_obj):
        return None
    api_info = {"doc": inspect.getdoc(class_obj), "methods": {}, "properties": {}}

    for name, member in inspect.getmembers(class_obj):
        if name.startswith('_'):
            continue
        try:
            if isinstance(member, property):
                sig = inspect.signature(member.fget)
                api_info["properties"][name] = {
                    "doc": inspect.getdoc(member),
                    "return_type": get_type_name(sig.return_annotation)
                }
            elif inspect.isfunction(member) or inspect.ismethod(member):
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
        except (ValueError, TypeError):
            api_info["methods"][name] = {"error": "Could not inspect (likely C-bound)"}

    return api_info

def crawl_pyedb():
    print("Starting to crawl pyedb package...")
    database = {}
    for importer, modname, ispkg in pkgutil.walk_packages(path=pyedb.__path__,
                                                          prefix=pyedb.__name__ + '.',
                                                          onerror=lambda x: None):
        try:
            module = importlib.import_module(modname)
            print(f"Inspecting module: {modname}")
            for class_name, class_obj in inspect.getmembers(module, inspect.isclass):
                if class_obj.__module__ == modname:
                    full_class_name = f"{modname}.{class_name}"
                    print(f"  -> Analyzing class: {full_class_name}")
                    api_data = analyze_class(class_obj)
                    if api_data:
                        database[full_class_name] = api_data
        except ImportError as e:
            print(f"Could not import {modname}: {e}")
        except Exception as e:
            print(f"Error inspecting {modname}: {e}")

    print("Crawl complete. Saving database...")
    with open("pyedb_api_database.json", "w", encoding="utf-8") as f:
        json.dump(database, f, indent=2, ensure_ascii=False)
    print("Database saved to 'pyedb_api_database.json'")

if __name__ == "__main__":
    crawl_pyedb()
```
