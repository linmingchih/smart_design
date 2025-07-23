Stackup匯出匯入EXCEL
---

### 目的

將 AEDB 中的 Stackup 資訊匯出成 Excel 檔並清楚標示單位與層屬性。使用者可以修改EXCEL當中厚度及材料參數

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
import warnings
import pandas as pd
from pyedb import Edb

# 忽略 FutureWarning 以避免 fillna 等操作產生警告
warnings.filterwarnings('ignore', category=FutureWarning)

def export_stackup_to_excel(edb_path: str,
                            excel_path: str = None,
                            unit: str = 'mm') -> str:
    """
    讀取 AEDB 的 stackup 資訊，並輸出為 Excel：
      • 第一列顯示單位
      • 第二列為欄位名稱
      • 第三列起為資料
      • 介電層：conductivity, Etch Factor, Roughness 欄位空白
      • 非介電層：permittivity / loss tangent 欄位空白
      • 不輸出 Material 欄位
      • 新增欄位：Etch Factor, Roughness Enabled,
               Nodule Radius (µm), Surface Ratio
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

        if typ == 'dielectric':
            perm = getattr(mat, 'permittivity', None)
            loss = getattr(mat, 'dielectric_loss_tangent', None)
            cond = None
            etch = None
            roughness_enabled = None
            nodule_radius = ''
            surface_ratio = ''
        else:
            perm = None
            loss = None
            cond = getattr(mat, 'conductivity', None)
            etch = getattr(layer, 'etch_factor', None)
            roughness_enabled = getattr(layer, 'roughness_enabled', None)
            rough_model = layer.get_roughness_model()
            nodule_radius = rough_model.get_NoduleRadius().ToString() if rough_model else ''
            surface_ratio = rough_model.get_SurfaceRatio().ToString() if rough_model else ''

        rows.append({
            'Layer Name':           layer_name,
            'Type':                 layer.type,
            f'Thickness ({unit})':  _meter_to_unit(layer.thickness, unit),
            'Permittivity':         perm,
            'Loss Tangent':         loss,
            'Conductivity (S/m)':   cond,
            'Etch Factor':          etch,
            'Roughness Enabled':    roughness_enabled,
            'Nodule Radius (µm)':   nodule_radius,
            'Surface Ratio':        surface_ratio
        })

    edb.close_edb()

    df = pd.DataFrame(rows)
    # 所有欄位轉為 object 讓空字串可寫入
    df = df.astype(object)
    df.fillna('', inplace=True)

    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        pd.DataFrame().to_excel(writer, index=False, sheet_name='Sheet1')
        ws = writer.sheets['Sheet1']
        ws.cell(row=1, column=1, value=f"Unit: {unit}")
        df.to_excel(writer, sheet_name='Sheet1', startrow=1, index=False)

    return excel_path

if __name__ == "__main__":
    edb_path = r"D:\demo2\Galileo_G87173_204.aedb"
    out = export_stackup_to_excel(edb_path, unit='mm')
    print(f"已輸出：{out}")

```
### 用修改完成的EXCEL來更新.aedb

從 Excel 匯入 PCB 材料特性並更新 AEDB

### 目的

將修改過的 Excel 中 Stackup 層的材料特性（導電或介電）讀入，並在 AEDB 中建立或重用對應材料，再將各 layer 的 material 屬性替換成新的材料。

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
    從 Excel 匯入 stackup 資訊，並更新 AEDB：

      • 替換每層的 material（cond 或 diel 特性重用材料）
      • 設定 layer.etch_factor
      • 只在 signal layer（非 dielectric）上設定 layer.roughness_enabled
      • 若同時有 Nodule Radius / Surface Ratio，才呼叫 assign_roughness_model()

    參數：
    ----------
    edb_path : str
        AEDB 檔案路徑
    xlsx_path : str
        之前 export 時產生的 Excel 路徑（第 1 列為單位、第 2 列為標題）
    edbversion : str
        AEDB 版本字串，預設 '2024.1'
    """
    # 1. 讀 Excel
    df = pd.read_excel(xlsx_path, header=1, dtype=str).fillna('')

    # 2. 收集所有不同的材料特性 key（cond 或 diel）
    prop_keys = []
    for _, row in df.iterrows():
        cond = row['Conductivity (S/m)']
        perm = row['Permittivity']
        loss = row['Loss Tangent']
        if cond:
            key = ('cond', float(cond))
        else:
            p = float(perm) if perm else 1.0
            l = float(loss) if loss else 0.0
            key = ('diel', p, l)
        if key not in prop_keys:
            prop_keys.append(key)

    # 3. 開啟 AEDB，準備比對與新增材料
    edb = Edb(edb_path, edbversion=edbversion)
    existing = edb.materials.materials  # name -> material obj
    prop_to_mat = {}

    # 4. 建材料並建立 key→material name 映射
    for key in prop_keys:
        if key[0] == 'cond':
            _, cond_val = key
            found = next((name for name, m in existing.items()
                          if hasattr(m, 'conductivity') and m.conductivity == cond_val), None)
            mat_name = found or f"m_cond_{int(cond_val)}"
            if not found:
                edb.materials.add_conductor_material(mat_name, cond_val)
        else:
            _, p_val, l_val = key
            found = next((name for name, m in existing.items()
                          if hasattr(m, 'permittivity') and hasattr(m, 'dielectric_loss_tangent')
                             and m.permittivity == p_val and m.dielectric_loss_tangent == l_val), None)
            mat_name = found or f"m_diel_{p_val:.2f}_{l_val:.3f}"
            if not found:
                edb.materials.add_dielectric_material(mat_name, p_val, l_val)
        prop_to_mat[key] = mat_name
        existing = edb.materials.materials

    # 5. 逐列設定 layer
    for _, row in df.iterrows():
        layer = edb.stackup.stackup_layers[row['Layer Name']]
        typ   = layer.type.lower()

        # 5.1 設定材料
        cond = row['Conductivity (S/m)']
        if cond:
            key = ('cond', float(cond))
        else:
            p = float(row['Permittivity']) if row['Permittivity'] else 1.0
            l = float(row['Loss Tangent'])   if row['Loss Tangent']   else 0.0
            key = ('diel', p, l)
        layer.material = prop_to_mat[key]

        # 5.2 Etch Factor
        if row['Etch Factor']:
            layer.etch_factor = float(row['Etch Factor'])

        # 5.3 Roughness Enabled：只在非 dielectric 上依 Flag 設定
        flag = row['Roughness Enabled'].strip().lower()
        if typ != 'dielectric' and flag in ('true', '1', 'yes'):
            layer.roughness_enabled = True
        else:
            layer.roughness_enabled = False

        # 5.4 只有在啟用且有設定粗糙度參數才呼叫 assign_roughness_model
        if layer.roughness_enabled:
            nodule = row['Nodule Radius (µm)']
            surf   = row['Surface Ratio']
            if nodule or surf:
                layer.assign_roughness_model(
                    huray_radius=str(nodule),
                    huray_surface_ratio=str(surf)
                )

    # 6. 儲存並關閉
    edb.save_edb()
    edb.close_edb()

# 範例用法
if __name__ == '__main__':
    edb_path  = r"D:\demo2\Galileo_G87173_204.aedb"
    xlsx_path = r"D:\demo2\Galileo_G87173_204_mm.xlsx"
    import_excel(edb_path, xlsx_path)
    print("已將 Excel 內容匯入並更新 AEDB。")

```