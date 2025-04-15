使用 PyAEDT 建立 Q3D 封裝模型
---
使用 PyAEDT 建立 Q3D 電子封裝中腳位與導線模型，並進行電磁模擬分析。

### 目的與功能
這段程式碼主要是利用 `PyAEDT` 套件操作 Ansys Q3D Extractor，建立電子元件中的腳位（Leg）與金屬導線（Bondwire）幾何模型，並指定相對應的電氣網路（net），最後進行電磁場模擬分析。

### 流程架構
1. **初始化與設定**：
   - 匯入必要模組，初始化 Q3D 模擬環境，設定單位與材料覆蓋規則。

2. **定義輔助函式**：
   - `_unit_vector`：計算方向向量並標準化。
   - `_closest_face`：找出多面體中距離參考點最近的面，方便後續指定電氣接點。

3. **Leg 類別**：
   - 代表元件腳位。
   - 建立 polyline 結構來模擬腳位的幾何延伸。
   - 根據腳位方向設定焊接點（solder_point），作為導線連接目標。

4. **LegBuilder 類別**：
   - 工廠模式協助建立 `Leg` 物件，並統一 thickness、width、height 設定。

5. **Bondwire 類別**：
   - 模擬連接焊點的金屬導線。
   - 使用多點折線建構曲面，具有圓形橫截面，模擬實際導線外型。

6. **主流程**：
   - 建立一組腳位資料（`leg_data`），產生對應的 Leg 物件。
   - 指定導線起點與對應腳位的焊點位置建立 Bondwire。
   - 建立底板（substrate），代表封裝基板。
   - 呼叫 `auto_identify_nets()` 自動辨識模擬網路，並設定各物件的電氣角色（source/sink）。
   - 建立頻率掃描設置並執行分析。

### 補充說明
- **q3d.modeler.create_polyline**：用於產生線段模型，可以設定橫截面形狀與尺寸。這裡 `rectangle` 用於腳位，`circle` 用於導線。
- **q3d.sink / q3d.source**：用來定義模擬中各物件的電氣角色，例如輸入（source）或輸出（sink）。
- **auto_identify_nets()**：能夠分析幾何模型的連接性，自動劃分網路，減少人工設定錯誤。
- **create_setup / create_frequency_sweep / analyze**：是建立模擬設置、設定頻率掃描範圍並執行模擬的標準流程。

這段程式碼結構清晰，採用物件導向設計，有效地拆分腳位、導線與建模邏輯，方便擴充與維護。


![2025-04-15_13-08-52](/assets/2025-04-15_13-08-52.png)

```python
from math import sqrt
from pyaedt import Q3d

q3d = Q3d(version='2024.1')
q3d.modeler.model_units = 'mm'
q3d.design_settings['MaterialOverride'] = True


def _unit_vector(x0, y0, x1, y1):
    dx, dy = x1 - x0, y1 - y0
    length = sqrt(dx**2 + dy**2)
    return dx / length, dy / length


def _closest_face(polyline, ref_point):
    x0, y0, z0 = ref_point
    return min(polyline.faces,
               key=lambda f: sqrt((f.center[0]-x0)**2 + (f.center[1]-y0)**2 + (f.center[2]-z0)**2))


class Leg:
    def __init__(self, pts, builder):
        self.pts = pts
        self.builder = builder

        (x0, y0), (x1, y1) = pts[-2:]
        self.vx, self.vy = _unit_vector(x0, y0, x1, y1)

        (x0, y0), (x1, y1) = pts[:2]
        vx, vy = _unit_vector(x0, y0, x1, y1)
        self.solder_point = (
            0.1 * vx + x0,
            0.1 * vy + y0,
            builder.thickness / 2
        )

    def create(self):
        profile = [(x, y, 0) for x, y in self.pts]
        x1, y1 = self.pts[-1]
        vx, vy = self.vx, self.vy
        h = self.builder.height

        profile += [
            (0.5 * vx + x1, 0.5 * vy + y1, -0.5),
            (0.5 * vx + x1, 0.5 * vy + y1, -h + 0.3),
            (0.7 * vx + x1, 0.7 * vy + y1, -h),
            (1.2 * vx + x1, 1.2 * vy + y1, -h),
        ]

        p = q3d.modeler.create_polyline(
            profile,
            xsection_type='rectangle',
            xsection_width=self.builder.width,
            xsection_height=self.builder.thickness
        )

        self.name = p.name
        self.face = _closest_face(p, profile[-1])

    def set(self, net_name):
        q3d.sink(self.face, net_name=net_name)


class LegBuilder:
    def __init__(self, thickness=0.2, width=0.5, height=2):
        self.thickness = thickness
        self.width = width
        self.height = height

    def build(self, pts):
        return Leg(pts, self)


class Bondwire:
    def __init__(self, pt1, pt2, height=0.5, radius=0.05):
        x1, y1, z1 = pt1
        x4, y4, z4 = pt2

        p1 = pt1
        p2 = (x1, y1, z1 + height)
        p3 = ((x4 - x1) * 0.25 + x1, (y4 - y1) * 0.25 + y1, z1 + height)
        p4 = (x4, y4, z4 + 2 * radius)
        p5 = pt2

        p = q3d.modeler.create_polyline(
            [p1, p2, p3, p4, p5],
            xsection_type='circle',
            xsection_width=radius * 2,
            xsection_num_seg=6
        )

        self.name = p.name
        self.face = _closest_face(p, p1)

    def set(self, net_name):
        q3d.source(self.face, net_name=net_name)


# ---------------- 主流程 ----------------

objects = {}
builder = LegBuilder()

leg_data = [
    ((0, -7), (0, -6), (1, -6)),
    ((0, -5), (0, -4), (1, -4)),
    ((0, -3), (0, -2), (1, -2)),
    ((0, 1), (0, 0), (1, 0)),
    ((0, 3), (0, 2), (1, 2)),
    ((0, 5), (0, 4), (1, 4)),
    ((-6, -7), (-6, -6), (-7, -6)),
    ((-6, -5), (-6, -4), (-7, -4)),
    ((-6, -3), (-6, -2), (-7, -2)),
    ((-6, 1), (-6, 0), (-7, 0)),
    ((-6, 3), (-6, 2), (-7, 2)),
    ((-6, 5), (-6, 4), (-7, 4)),
]

legs = []
for pts in leg_data:
    leg = builder.build(pts)
    leg.create()
    legs.append(leg)
    objects[leg.name] = leg

wire_points = [
    (-2, -3.5, 0.5), (-2, -2.5, 0.5), (-2, -1.5, 0.5),
    (-2, -0.5, 0.5), (-2, 0.4, 0.5), (-2, 1.5, 0.5),
    (-4, -3.5, 0.5), (-4, -2.5, 0.5), (-4, -1.5, 0.5),
    (-4, -0.5, 0.5), (-4, 0.4, 0.5), (-4, 1.5, 0.5),
]

# 建立底板
substrate = q3d.modeler.create_box((-7, -8, -0.8), (8, 14, 2), material="polyimide")
substrate.color = (0, 200, 0)
substrate.transparency = 0.9

# 建立 Bondwire
for pt1, leg in zip(wire_points, legs):
    wire = Bondwire(pt1, leg.solder_point)
    objects[wire.name] = wire

# 自動辨識網路並設定 source/sink
q3d.auto_identify_nets()
for net_name, obj_names in q3d.objects_from_nets(q3d.nets).items():
    for obj_name in obj_names:
        objects[obj_name].set(net_name)

# 建立設置與分析
setup = q3d.create_setup()
setup.create_frequency_sweep()
q3d.analyze()

```