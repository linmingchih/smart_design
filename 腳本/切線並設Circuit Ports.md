切線並設Circuit Ports
---

當差分對在PCB板上通過導通孔（vias）連接至其他層時，如果只需模擬傳輸線本身的特性，則必須在傳輸線進入via的反墊圈（antipad）之前將其截斷。在截斷點，根據參考平面的位置，在上、下或兩端各設置一個電路端口（circuit ports）。如果需要設置的差分對眾多，這項工作可能相當繁瑣。這個腳本能夠半自動化這一流程：用戶只需選擇差分對和對應的空白區域（void），然後依次選擇每對差分對和空白區域。所有選擇完成後，運行腳本即可自動處理。

![Untitled Project (Time 0_00_56;07)](/assets/Untitled%20Project%20(Time%200_00_56;07)_mt08w7w56.png)

[操作影片播放](/assets/set_ports.mp4)

```python
import random
import string
import sys
sys.path.append(r"C:\Program Files\AnsysEM\v241\Win64\PythonFiles\DesktopPlugin")
import ScriptEnv
ScriptEnv.Initialize("", False, "", 50051)

oProject = oDesktop.GetActiveProject()
oDesign = oProject.GetActiveDesign()
oEditor = oDesign.GetActiveEditor()

oDesign.GetName()

def create_polygon(name, layer, positions):
    edges = len(positions)
    positions = positions + [positions[0]]
    arguments = []
    for x, y in positions:
        arguments += ['x:=', x, 'y:=', y]
    
    oEditor.CreatePolygon(
    	[
    		"NAME:Contents",
    		"polyGeometry:=", ["Name:=", name,			
                               "LayerName:=", layer,
                               "0",			
                               "n:=" , edges,			
                               "U:=", "mm",] + arguments
    	])




#%#
def check_intersection(line1, line2):
    """ Check if two lines (each defined by a pair of points) intersect """
    (x1, y1), (x2, y2) = line1
    (x3, y3), (x4, y4) = line2

    # Calculate the determinant of the coefficient matrix
    det = (x2 - x1) * (y4 - y3) - (y2 - y1) * (x4 - x3)
    if det == 0:
        return None  # Lines are parallel

    # Calculate the relative position of the intersection point along each line
    t = ((x3 - x1) * (y4 - y3) - (y3 - y1) * (x4 - x3)) / det
    u = ((x3 - x1) * (y2 - y1) - (y3 - y1) * (x2 - x1)) / det

    # Check if the intersection point is within the line segments
    if 0 <= t <= 1 and 0 <= u <= 1:
        # Calculate the intersection point coordinates
        intersection_x = x1 + t * (x2 - x1)
        intersection_y = y1 + t * (y2 - y1)
        return (intersection_x, intersection_y)
    return None


class Geometry:
    def __init__(self, name):
        self.name = name
        self.layer = oEditor.GetPropertyValue('BaseElementTab', name, 'PlacementLayer')
        
        pt_ids = self.get_ptids() 
        
        self.pts = []
        self.pt_ptid = {}
        for pt_id in pt_ids:
            value = oEditor.GetPropertyValue('BaseElementTab', name, pt_id)
            try:
                x, y = map(float, value.split(','))
                self.pts.append((x, y))
                self.pt_ptid[(x, y)] = pt_id
            except:
                x = float(value.replace('mm',''))
                self.pts.append((x, 1e200))
        
        self.segments = []
        for pt1, pt2 in zip(self.pts[:-1], self.pts[1:]):
            x1, y1 = pt1
            x2, y2 = pt2
            if y1 > 1e100 or y2 > 1e100:
                continue
            else:
                self.segments.append((pt1, pt2))

    def get_ptids(self):
        self.pt_ids = []
        for prop in oEditor.GetProperties('BaseElementTab', name):
            if prop.startswith('Pt') or prop.startswith('ArcHeight'):
                self.pt_ids.append(prop)
        
        return self.pt_ids
                
    def get_intersection(self, other):
        intersection_points = []
        for s1 in self.segments:
            for s2 in other.segments:
                intersection = check_intersection(s1, s2)
                if intersection:
                    intersection_points.append(intersection)

        return intersection_points[0], self.pt_ptid[s1[1]]
        

class Line(Geometry):
    def set_ports(self):
        pass


class Void(Geometry):
    def remove(self):
        pass    


class Item:
    def __init__(self):
        self.lines = []
        self.voids = []
    
    
items = []
item = Item()    
for name in oEditor.GetSelections():
    if oEditor.GetPropertyValue('BaseElementTab', name, 'Type') == 'line':
        if not item.voids:
            item.lines.append(Line(name))
        else:
            items.append(item)
            item = Item()
            item.lines.append(Line(name))
            
    elif oEditor.GetPropertyValue('BaseElementTab', name, 'Type') == 'poly void':
        item.voids.append(Void(name))
else:
    items.append(item)

unit_map = {'nm':1e-9, 'um':1e-6, 'mm':1e-3, 'mil':2.54e-5}

scale = unit_map[oEditor.GetActiveUnits()]

for item in items:
    lines = item.lines
    voids = item.voids
    
    xv, yv = voids[0].pts[0]

    for line in item.lines:
        x0, y0 = line.pts[0]
        x1, y1 = line.pts[-1]
        if ((x1 - xv)**2 + (y1 - yv)**2 ) > ((x0 - xv)**2 + (y0 - yv)**2 ):
            oEditor.ReverseLine(["NAME:elements",line.name])
            line.get_ptids()
        
        (xp, yp), pt_id_collision = line.get_intersection(voids[0])
        for void in voids:
            print(xp, yp)
            oEditor.CreateCircuitPort(
             	[
            		"NAME:Location",
            		"PosLayer:="		, line.layer,
            		"X0:="			, xp*scale,
            		"Y0:="			, yp*scale,
            		"NegLayer:="		, void.layer,
            		"X1:="			, xp*scale,
            		"Y1:="			, yp*scale
             	])
            

        random_name = ''.join([random.choice(string.ascii_letters) for _ in range(10)])
        create_polygon(random_name, line.layer, voids[0].pts)
        oEditor.Subtract(["NAME:primitives", line.name, random_name])
        
    for void in voids:
        oEditor.Delete([void.name])
```

