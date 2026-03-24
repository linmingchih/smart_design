SPIRAL
---

```python
import math
from ansys.aedt.core import Maxwell3d
from ansys.aedt.core.modeler.cad.polylines import PolylineSegment

def create_spiral(m3d, name, center, radius, width, gap, rounds):
    points = []
    segments = []
    
    cx, cy, cz = center
    pitch = width + gap
    r_current = radius
    angle_current = math.pi / 2  # Start at 90 degrees (along +Y)
    
    # First point
    p0 = [cx + r_current * math.cos(angle_current), cy + r_current * math.sin(angle_current), cz]
    points.append(p0)
    
    for _ in range(rounds):
        # Calculate angle to leave a gap of 'pitch'
        # To avoid math domain error if pitch > r_current, cap the ratio
        ratio = pitch / r_current
        if ratio > 0.99:
            ratio = 0.99
            
        delta_angle_rad = math.asin(ratio)
        arc_angle_deg = 360.0 - math.degrees(delta_angle_rad)
        angle_end = angle_current - delta_angle_rad
        
        # Add Arc
        segments.append(PolylineSegment(segment_type="AngularArc", arc_center=center, arc_angle=f"{arc_angle_deg}deg", arc_plane="XY"))
        
        # Next radius
        r_next = r_current + pitch
        
        # Add Line
        segments.append(PolylineSegment(segment_type="Line"))
        
        # Next point (End of Line)
        next_pt = [cx + r_next * math.cos(angle_end), cy + r_next * math.sin(angle_end), cz]
        points.append(next_pt)
        
        # Update for next turn
        r_current = r_next
        angle_current = angle_end

    return m3d.modeler.create_polyline(
        points=points,
        segment_type=segments,
        name=name,
        xsection_type="Rectangle",
        xsection_width=width,
        xsection_height=0.01
    )

m3d = Maxwell3d(version="2026.1")
m3d.modeler.model_units = "mm"

p6 = create_spiral(
    m3d=m3d,
    name="P6",
    center=[0.0, 0.0, 0.0],
    radius=0.5,
    width=0.1,
    gap=0.02,
    rounds=10
)

print(p6.name)

```

![](/assets/2026-03-24_12-16-20.png)