Stackup匯出匯入EXCEL
---

### 目的

將 AEDB 中的 Stackup 資訊匯出成 Excel 檔，方便查看與後續處理，並清楚標示單位與層屬性。

### 功能

1. 根據 `unit`（預設 mm 或 mil）轉換每層厚度。
2. 讀取 AEDB 中每個 layer 的：

   * 層名稱（Layer Name）
   * 層類型（Type）
   * 厚度（Thickness）
   * 材料特性：介電層顯示 Permittivity / Loss Tangent，非介電層顯示 Conductivity。
3. 生成含單位說明的 Excel：

   * 第一列顯示輸出單位（`Unit: mm` 或 `Unit: mil`）。
   * 第二列為標題欄位。
   * 從第三列起寫入資料，空值以空白儲存格呈現。
4. 回傳產生的檔案路徑。

### 流程架構

```
設定輸出路徑 → 開啟 AEDB → 收集每層資料 → 關閉 AEDB → 建立 DataFrame → 寫入 Excel → 回傳路徑
```

### 補充說明

* `_meter_to_unit(val_m, unit)`：將公尺轉為 mm 或 mil。
* `edb.stackup.stackup_layers`：取得所有堆疊層物件。
* `edb.materials.materials`：材料字典，用於查找材料屬性。
* 介電層（`dielectric`）只保留 `permittivity` 和 `dielectric_loss_tangent`；金屬或其他層只保留 `conductivity`。
* `pd.ExcelWriter(..., engine='openpyxl')`：使用 openpyxl 寫入，手動插入單位列後，再寫入 DataFrame。
* `df.fillna('', inplace=True)`：將所有 NaN/None 置為 `''`，保證儲存格為空白。


### export_xlsx.py
```python
import os
import pandas as pd
from pyedb import Edb

def export_stackup_to_excel(edb_path: str,
                            excel_path: str = None,
                            unit: str = 'mm') -> str:
    """
    讀取 AEDB 的 stackup 資訊，並輸出為 Excel：
      • 第一列顯示單位
      • 第二列為欄位名稱
      • 第三列起為資料
      • 介電層：conductivity 欄位空白
      • 非介電層：permittivity / loss tangent 欄位空白
      • 不輸出 Material 欄位
    """
    def _meter_to_unit(val_m: float, unit: str) -> float:
        if unit == 'mm':
            return val_m * 1e3
        elif unit == 'mil':
            return val_m * 39_370.07874
        else:
            raise ValueError("unit 必須是 'mm' 或 'mil'")

    if excel_path is None:
        base, _ = os.path.splitext(edb_path)
        excel_path = f"{base}_{unit}.xlsx"

    edb = Edb(edb_path, edbversion='2024.1')
    rows = []
    for layer_name, layer in edb.stackup.stackup_layers.items():
        mat = edb.materials.materials.get(layer.material, None)
        typ = layer.type.lower()

        # 依層型態有條件地保留／清空屬性
        if typ == 'dielectric':
            perm  = getattr(mat, 'permittivity', None)
            loss  = getattr(mat, 'dielectric_loss_tangent', None)
            cond  = None
        else:
            perm  = None
            loss  = None
            cond  = getattr(mat, 'conductivity', None)

        rows.append({
            'Layer Name':           layer_name,
            'Type':                 layer.type,
            f'Thickness ({unit})':  _meter_to_unit(layer.thickness, unit),
            'Permittivity':         perm,
            'Loss Tangent':         loss,
            'Conductivity (S/m)':   cond
        })
    edb.close_edb()

    df = pd.DataFrame(rows)
    # 將所有 NaN/None → ''，保證空白儲存格
    df.fillna('', inplace=True)

    # 寫入 Excel
    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        # 建立一個空 sheet
        pd.DataFrame().to_excel(writer, index=False, sheet_name='Sheet1')
        ws = writer.sheets['Sheet1']
        # 第一列：顯示輸出單位
        ws.cell(row=1, column=1, value=f"Unit: {unit}")
        # 第二列開始寫入 DataFrame
        df.to_excel(writer, sheet_name='Sheet1', startrow=1, index=False)

    return excel_path

# 範例呼叫
if __name__ == "__main__":
    edb_path = r"D:\demo2\Galileo_G87173_20454.aedb"
    out = export_stackup_to_excel(edb_path, unit='mm')
    print(f"已輸出：{out}")

```
### 主題

從 Excel 匯入 PCB 材料特性並更新 AEDB

### 目的

將先前匯出的 Excel 中 Stackup 層的材料特性（導電或介電）讀入，並在 AEDB 中建立或重用對應材料，再將各 layer 的 material 屬性替換成新的材料。

### 功能

1. 讀取 Excel，解析各層材料的導電率、介電常數與損耗角正切。
2. 對於每種不同特性的材料：

   * 若 AEDB 已有相同特性材料，則重用該材料。
   * 否則，依特性命名並新增導體或介電材料。
3. 將 Excel 中每列對應的 layer，替換 AEDB 堆疊結構中的材料屬性。
4. 儲存並關閉 AEDB。

### 流程架構

```
Excel 讀取 → 收集不同材料特性 → 開啟 AEDB → 檢查／新增材料 → 逐層替換 → 儲存關閉
```

### 補充說明

* `pandas.read_excel(..., header=1)`：第二列當作欄位名稱。
* 材料特性 key:

  * `'cond'` + 導電率，表示導電材料。
  * `'diel'` + 介電常數、損耗角正切，表示介電材料。
* 用 `Edb` 物件管理 AEDB，透過 `edb.materials.add_conductor_material` 和 `add_dielectric_material` 新增材料。
* 使用 `existing = edb.materials.materials` 讀取現有材料字典，並同步更新以利重複檢查。
* 屬性替換後須呼叫 `edb.save_edb()` 和 `edb.close_edb()` 儲存變更。


### import_xlsx.py


```python
import os
import pandas as pd
from pyedb import Edb

def import_excel(edb_path: str,
                 xlsx_path: str,
                 edbversion: str = '2024.1') -> None:
    """
    從 Excel 匯入 stackup 資訊，為每種材料特性只建立一次材料（若已存在則重用），
    並替換 AEDB 中所有 layer 的 material 屬性。

    參數：
    ----------
    edb_path : str
        AEDB 檔案路徑
    xlsx_path : str
        之前 export 時產生的 Excel 路徑（第一列為單位，第 2 列為標題）
    edbversion : str
        AEDB 版本字串，預設 '2024.1'

    回傳：None（直接修改並儲存 AEDB）
    """
    # 1. 讀 Excel（第 2 列為欄位名稱）
    df = pd.read_excel(xlsx_path, header=1)

    # 2. 收集所有不同的材料特性 key
    prop_keys = []
    for _, row in df.iterrows():
        cond = row.get('Conductivity (S/m)',   pd.NA)
        perm = row.get('Permittivity',         pd.NA)
        loss = row.get('Loss Tangent',         pd.NA)

        if pd.notna(cond) and cond != '':
            key = ('cond', float(cond))
        else:
            key = (
                'diel',
                float(perm) if pd.notna(perm) else 1.0,
                float(loss) if pd.notna(loss) else 0.0
            )
        if key not in prop_keys:
            prop_keys.append(key)

    # 3. 開啟 AEDB，準備檢查現有材料並新增
    edb = Edb(edb_path, edbversion=edbversion)
    existing = edb.materials.materials  # dict: name -> material obj

    # 建立「特性 key → 材料名稱」映射
    prop_to_matname = {}

    for key in prop_keys:
        if key[0] == 'cond':
            _, cond_val = key
            # 先嘗試在 existing 中找到相同 conductivity
            found = None
            for name, mat in existing.items():
                if hasattr(mat, 'conductivity') and mat.conductivity == cond_val:
                    found = name
                    break
            if found:
                mat_name = found
            else:
                mat_name = f"m_cond_{int(cond_val)}"
                edb.materials.add_conductor_material(mat_name, cond_val)

        else:
            _, perm_val, loss_val = key
            # 找相同 permittivity & loss_tangent
            found = None
            for name, mat in existing.items():
                if (hasattr(mat, 'permittivity') and hasattr(mat, 'dielectric_loss_tangent')
                        and mat.permittivity == perm_val
                        and mat.dielectric_loss_tangent == loss_val):
                    found = name
                    break
            if found:
                mat_name = found
            else:
                mat_name = f"m_diel_{perm_val:.2f}_{loss_val:.3f}"
                edb.materials.add_dielectric_material(mat_name,
                                                      perm_val,
                                                      loss_val)

        prop_to_matname[key] = mat_name
        # 同步更新 existing，方便下一次檢查
        existing = edb.materials.materials

    # 4. 依 Excel 每一列，替換對應 layer 的 material
    for _, row in df.iterrows():
        layer_name = row['Layer Name']
        cond = row.get('Conductivity (S/m)', pd.NA)
        perm = row.get('Permittivity',       pd.NA)
        loss = row.get('Loss Tangent',       pd.NA)

        if pd.notna(cond) and cond != '':
            key = ('cond', float(cond))
        else:
            key = (
                'diel',
                float(perm) if pd.notna(perm) else 1.0,
                float(loss) if pd.notna(loss) else 0.0
            )

        new_mat = prop_to_matname[key]
        layer = edb.stackup.stackup_layers[layer_name]
        layer.material = new_mat

    # 5. 儲存並關閉
    edb.save_edb()
    edb.close_edb()



# 範例用法
if __name__ == "__main__":
    edb_path  = r"D:\demo2\Galileo_G87173_20454.aedb"
    xlsx_path = r"D:\demo2\Galileo_G87173_20454_mm.xlsx"
    import_excel(edb_path, xlsx_path)
    print("已將 Excel 內容匯入並更新 AEDB。")

```