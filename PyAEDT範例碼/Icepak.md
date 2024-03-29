### 設定圓柱坐標系異相性熱導材料
材料名稱是 dd4，設定了坐標系統類型為「圓柱形」。而且它的導熱性是各向異性的，這意味著在不同的方向導熱性能是不一樣的。


![2024-03-29_12-48-53](/assets/2024-03-29_12-48-53.png)


```python
from pyaedt import Icepak

icepak = Icepak(specified_version='2024.1')

m1 = icepak.materials.add_material('dd4')

m1.coordinate_system = 'Cylindrical'
m1. thermal_conductivity = [1,2,3]
```