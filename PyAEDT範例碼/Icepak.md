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

### Group建立

![2024-04-03_07-53-36](/assets/2024-04-03_07-53-36.png)

```
icepak = Icepak(specified_version='2024.1')

x1 = icepak.modeler.create_box((0,0,0),(1,1,1))
x2 = icepak.modeler.create_cylinder('XY', (2,2,2), 1, 3)
x3 = icepak.modeler.create_sphere((-1,-1,-1), 1)

g1 = icepak.modeler.create_group([x1, x2], group_name='IC_ASSM')
g2 = icepak.modeler.create_group(objects=[x3], groups=[g1], group_name='PCB_ASSM')
```

代碼片段使用Icepak PyAEDT API來創建幾何體並將它們分組。這裡是對代碼的解釋：

1. **初始化Icepak模型** ： 
- `icepak = Icepak(specified_version='2024.1')`
這一行代碼創建了一個Icepak對象，指定了其版本為2024.1。 
2. **創建幾何體** ： 
- `x1 = icepak.modeler.create_box((0,0,0),(1,1,1))`
這創建了一個以原點為一角，邊長為1的立方體。 
- `x2 = icepak.modeler.create_cylinder('XY', (2,2,2), 1, 3)`
這創建了一個位於(2,2,2)點，基於XY平面，半徑為1，高度為3的圓柱體。 
- `x3 = icepak.modeler.create_sphere((-1,-1,-1), 1)`
這創建了一個中心點為(-1,-1,-1)，半徑為1的球體。 
3. **分組幾何體** ： 
- `g1 = icepak.modeler.create_group([x1, x2], group_name='IC_ASSM')`
這一步將x1（立方體）和x2（圓柱體）放入一個名為'IC_ASSM'的組中。 
- `g2 = icepak.modeler.create_group(objects=[x3], groups=[g1], group_name='PCB_ASSM')`
這一步將x3（球體）和之前創建的組g1放入一個名為'PCB_ASSM'的更大的組中。

這些步驟在模擬環境中創建了幾個基本幾何形狀，並將它們組織成兩個不同的組。
