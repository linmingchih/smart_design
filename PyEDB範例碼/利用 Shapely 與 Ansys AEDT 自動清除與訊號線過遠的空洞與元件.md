利用 Shapely 與 Ansys AEDT 自動清除與訊號線過遠的空洞與元件
---

簡化電源平面設計，清除與信號線距離超過 1mm 的 void polygon（空洞）與元件，以減少不必要的複雜性與潛在的電氣干擾。透過移除不必要的幾何物件，可以**大幅減少模擬所需的記憶體與計算資源**，進而**縮短模擬時間**並提升效能。

### 功能

* 載入 AEDB 電路板設計檔。
* 擷取所有信號線段並建立空間查詢樹（STRtree）。
* 擷取所有空洞與元件輪廓。
* 計算每個空洞或元件與信號線的最短距離。
* 自動刪除距離過遠（>1mm）的空洞與元件。
* 儲存簡化後的設計檔。

### 流程架構

1. **載入資料**：使用 `ansys.aedt.core.Edb` 載入指定路徑的 AEDB 設計檔案。
2. **擷取信號線段**：掃描所有 signal net 中的 primitive，轉為 Shapely 的 `LineString`，並建立 `STRtree` 用於後續快速空間查詢。
3. **擷取 void polygon 和元件輪廓**：從 power nets 擷取 `is_void` 為 True 的 primitive，再加上所有元件的 bounding box 作為多邊形處理。
4. **距離計算**：對每個 polygon 建立查詢區域（多邊形擴大 100mm），用 `STRtree` 找出可能的鄰近線段，計算最小距離。
5. **過濾刪除**：刪除與最近線段距離大於 1mm（0.001 公尺）的 primitive。
6. **儲存結果**：儲存為新的 AEDB 設計檔。

### 補充說明

* **Shapely 與 STRtree**：`STRtree` 是 Shapely 提供的空間索引工具，用於加速多邊形與線段之間的距離計算。
* **Polygon 建立時的錯誤處理**：有些 raw\_pts 可能格式錯誤或不合法，會跳過處理。
* **距離單位**：Ansys AEDB 使用公尺為單位，因此 0.001 相當於 1mm。

### 範例程式

```python
from shapely.geometry import LineString, Polygon, box
from shapely.strtree import STRtree
from ansys.aedt.core import Edb

# 載入 AEDB 檔案
path = r"d:/demo/test.aedb"
edb = Edb(path, edbversion="2024.1")

# 擷取信號線段並建立 STRtree
lines = []
for net in edb.nets.signal_nets.values():
    for prim in net.primitives:
        lines.append(LineString(prim.center_line))
line_tree = STRtree(lines)

# 擷取所有 void polygon 與元件框線
polygons = {}
for net in edb.nets.power_nets.values():
    for prim in net.primitives:
        if prim.is_void:
            polygons[prim] = prim.points()

for _, comp in edb.components.components.items():
    x1, y1, x2, y2 = comp.bounding_box
    polygons[comp] = ([x1, x2, x2, x1], [y1, y1, y2, y2])

# 計算每個 polygon 與最近線段距離
poly_distances = {}
for prim, raw_pts in polygons.items():
    if isinstance(raw_pts, tuple) and len(raw_pts) == 2:
        coords = list(zip(*raw_pts))
    elif isinstance(raw_pts, list) and raw_pts and len(raw_pts[0]) == 2:
        coords = raw_pts
    else:
        continue

    try:
        poly = Polygon(coords)
    except Exception:
        continue

    minx, miny, maxx, maxy = poly.bounds
    search_box = box(minx - 0.01, miny - 0.01, maxx + 0.01, maxy + 0.01)
    idxs = line_tree.query(search_box)

    if len(idxs) > 0:
        candidate_lines = [lines[i] for i in idxs]
        min_dist = min(poly.distance(line) for line in candidate_lines)
    else:
        min_dist = float("inf")

    poly_distances[prim] = min_dist

# 刪除距離過遠的 primitive
to_delete = [prim for prim, dist in poly_distances.items() if dist > 0.001]
for prim in to_delete:
    prim.delete()

# 儲存新的 AEDB 檔案
edb.save_edb_as("d:/demo/simp6.aedb")
```



![2025-05-26_14-24-52](/assets/2025-05-26_14-24-52.png)