SymPy協助參數化結構
---

![2024-10-30_04-41-58](/assets/2024-10-30_04-41-58.png)
```python
from sympy import symbols, Matrix
from pyaedt import Hfss

# 定義符號變量
L1, L2, L3, W1, W2 = symbols('L1 L2 L3 W1 W2')

# 起始點和向量定義
origin = [0, -L2-W2/2, 0]
vectors = [[W1/2, 0, 0],
           [0, L2, 0],
           [L1, 0, 0],
           [0, W2, 0],
           [-L1, 0, 0],
           [0, L3, 0],
           [-W1/2, 0, 0]]

# 鏡像向量列表
points = [Matrix(origin)]

# 計算所有點的座標
for vector in vectors:
    new_point = points[-1] + Matrix(vector)
    points.append(new_point)

# 將每個點轉換為字串形式的 tuple
points_tuple = [tuple(str(i) for i in point) for point in points]


hfss = Hfss(version='2024.2')

for v in 'L1 L2 L3 W1 W2'.split():
    hfss[v] = '1mm'
    
x = hfss.modeler.create_polyline(points_tuple, close_surface=True, cover_surface=True)
hfss.modeler.duplicate_and_mirror(x, (0,0,0), (-1,0,0))
```
![2024-10-30_04-42-52](/assets/2024-10-30_04-42-52.png)