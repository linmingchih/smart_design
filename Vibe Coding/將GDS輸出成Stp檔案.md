透過 ChatGPT，把 GDS 自動轉成 STEP，從此告別手動建模
---

最近接到一個案子，內容其實並不陌生：將版圖檔（GDS）轉成 3D 結構，準備進行應力分析模擬。流程上我早就很熟了：打開工具，讀進 GDS 檔，再根據 `.tech` 技術檔案標示的圖層高度與厚度，一層一層建成立體幾何，然後轉成 `.step`，最後輸入到 Ansys Mechanical 跑模擬。這流程我重複過很多次，問題是這次資料量有點大 —— 超過 100 個 layout，要我一個一個框、一個一個轉，我的內心直接崩潰。


### 「這種重複工作，不就是 AI 最擅長的嗎？」

以前我會忍耐，畢竟能動手解決就不是問題。但這次我決定換個方式，試著請 ChatGPT 幫我寫腳本來自動化這一切。我上傳.tech檔案，並開門見山地對它說：

```
我有一個 GDS 檔和一個 tech 檔，GDS 裡面是 layout 多邊形，tech 檔裡記錄每個 layer 對應的高度和厚度（μm），我想要擷取一塊特定區域，例如 (100, 100) 到 (300, 300)，然後把落在這個區域內的每個圖形依照對應高度與厚度建成立體幾何，再全部輸出成一個 STEP 檔。
```

它馬上就理解我要幹嘛，還很貼心地回我說：「這個任務可以分成幾個模組來做，我會幫你用三個 Python 套件來完成這件事。」，它接著解釋說：

* 使用 **`gdstk`**：用來讀取 GDS 檔，能取得每個 polygon 的點座標與對應的 layer 資訊。
* 使用 **`shapely`**：做區域擷取（ROI），比如把圖形和你指定的框框做交集。
* 使用 **`cadquery`**：把 2D 的圖形拉成立體幾何，再轉成 `.step` 檔。

我想說：這說明也太清楚，根本像教學。它甚至還主動說：「單位是 μm，我會幫你轉成 mm 輸出到 CAD。」

### 實際測試程式

它寫的程式邏輯超清楚，從讀檔、解析 tech 層、篩選 ROI、建立 3D 幾何、再到輸出 STEP，全都一次完成。我只花了幾分鐘改一下檔案路徑，就可以跑起來了。終端機跳出訊息：

```
✅ ROI STEP 檔案輸出完成：D:/demo/gds_roi.step
```

我用 CAD 工具打開來看，結果幾何堆疊完全正確，厚度、高度、平移全部 OK。連原本最怕的多邊形問題、無效幾何，它也幫我自動排除並提醒我哪幾個圖形跳過了。

這時我腦袋開始轉：「那能不能一次處理整個資料夾裡的所有 GDS？」我問 ChatGPT：「可以批次處理多個檔案嗎？」

它馬上改寫了程式邏輯，加入迴圈掃描目錄中的 `.gds` 檔，並對每個檔案自動執行剛剛的流程，並且輸出對應的 `.step` 檔。整批 layout 一口氣處理完，原本預期要花我三天的工作，現在不到十分鐘就結束，整個人差點跪著感謝。

我後來把程式包成小工具，甚至還加了幾個變數設定區域，讓我可以換 tech 檔、換 ROI 座標、或是換輸出資料夾。

過去我總以為要會寫程式，才能做自動化。但現在，我只需要「能說出我要幹嘛」，剩下的交給 AI 幫我翻譯成程式語言。這不是偷懶，是讓我把時間專注在分析和決策，而不是在那裡 Ctrl+C、Ctrl+V。這又是一個和 ChatGPT 成功的協作。

### 轉檔範例碼

```python
import gdstk
import shapely.geometry as sg
import cadquery as cq
import os
import re

# === 路徑設定 ===
gds_path = r"d:/demo/example.gds"
tech_path = r"d:/demo/example.tech"
output_dir = r"d:/demo"
os.makedirs(output_dir, exist_ok=True)

# === 解析 tech 檔案 ===
layer_info = {}
with open(tech_path, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("//"):
            continue
        match = re.match(r"(\d+)\s+\S+\s+\S+\s+(\d+)\s+(\d+)", line)
        if match:
            layer = int(match.group(1))
            elevation = int(match.group(2))
            thickness = int(match.group(3))
            layer_info[layer] = (elevation, thickness)

# === 匯入 GDS 檔案 ===
lib = gdstk.read_gds(gds_path)
cell = lib.top_level()[0]

# === 顯示 GDS 檔案使用的單位與範圍 ===
all_xy = [pt for poly in cell.polygons for pt in poly.points]
x_vals = [pt[0] for pt in all_xy]
y_vals = [pt[1] for pt in all_xy]
x_min, x_max = min(x_vals), max(x_vals)
y_min, y_max = min(y_vals), max(y_vals)

print(f"📐 GDS 單位: {lib.unit} (1 表示 mm)")
print("📏 GDS bounding box:")
print(f"    X: {x_min:.3f} ~ {x_max:.3f} mm")
print(f"    Y: {y_min:.3f} ~ {y_max:.3f} mm")

# === 使用者指定欲擷取區域（mm）===
bounding_box = [(100, 100), (300, 300)]  # 左下, 右上
(x1, y1), (x2, y2) = bounding_box
roi_box = sg.box(x1, y1, x2, y2)

# === 建立 ROI 內的 polygon 列表 ===
roi_polygons = []
for poly in cell.polygons:
    layer = poly.layer
    if layer not in layer_info:
        continue
    pts = poly.points
    g_poly = sg.Polygon(pts)
    if not g_poly.is_valid or g_poly.is_empty:
        continue
    clipped = g_poly.intersection(roi_box)
    if clipped.is_empty:
        continue
    if isinstance(clipped, sg.Polygon):
        roi_polygons.append((clipped, layer))
    elif isinstance(clipped, sg.MultiPolygon):
        for sub in clipped.geoms:
            roi_polygons.append((sub, layer))

# === 建立 3D 幾何體 ===
solids = []
for shp, layer in roi_polygons:
    elevation, thickness = layer_info[layer]
    coords = list(shp.exterior.coords)
    try:
        wire = cq.Workplane("XY").polyline(coords).close()
        solid = wire.extrude(thickness * 1e-3)  # μm ➜ mm
        solid = solid.translate((0, 0, elevation * 1e-3))  # μm ➜ mm
        solids.append(solid)
    except Exception as e:
        print(f"⚠️ 幾何錯誤：{e}")

# === 匯出 STEP 檔案 ===
if solids:
    compound = cq.Compound.makeCompound([s.val() for s in solids])
    step_path = os.path.join(output_dir, "gds_roi.step")
    cq.exporters.export(compound, step_path)
    print(f"✅ ROI STEP 檔案輸出完成：{step_path}")
else:
    print("⚠️ ROI 區域內沒有成功建模的圖形。")

```