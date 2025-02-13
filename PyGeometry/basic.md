
```python
from ansys.geometry.core.sketch import Sketch
from ansys.geometry.core.math import Point2D
from ansys.geometry.core import Modeler
from ansys.geometry.core import launch_modeler


modeler = launch_modeler('spaceclaim')

design = modeler.create_design('xxx')
sketch = Sketch()
sketch.polygon(Point2D([0,0]), 10, 8, 0)
sketch.polygon(Point2D([30, 0]), 10, 20, 0)
body = design.extrude_sketch("MyBody", sketch, 2)

```
