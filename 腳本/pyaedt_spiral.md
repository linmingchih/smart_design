PyAEDT - SPIRAL
---
#### 建模、求解並抓取模擬資料

![2024-03-22_08-38-29](/assets/2024-03-22_08-38-29.png)

```python
from math import tan
from cmath import pi, exp
from pyaedt import Hfss

def turn():
    angle = 0
    while True:
        yield exp(1j*angle)
        angle += pi/4

def spiral(inner_radius=100, width=20, thickness=2, spacing=20, height=10,  N=3, padding=50, dk=2, df=0.01):   
    hfss = Hfss(specified_version='2024.1')
    hfss.change_material_override()
    hfss.modeler.model_units = 'um'
    step = (width + spacing) * tan(pi/8) * 2
    dielectric = hfss.materials.add_material('dielectric')
    dielectric.permittivity = dk
    dielectric.dielectric_loss_tangent = df

    
    t = turn()
    p = 0-(inner_radius)*1j
    points = [p]
    l = inner_radius
    
    for i in range(8*N+1):
        if i in [0, 8*N]:
            p += l*next(t)/2
        else:
            l += step/8
            p += l*next(t)
        
        points.append(p)
    
    points.append(p-20j)
    points = [(i.real, i.imag, 0) for i in points]
    obj = hfss.modeler.create_polyline(points,
                                       xsection_type='Rectangle',
                                       xsection_width=width,
                                       xsection_height=thickness,
                                       matname='copper')
    
    x0, y0, z0, x1, y1, z1 = obj.bounding_box
    box = hfss.modeler.create_box((x0-padding, y0-padding, -height),
                                  (x1-x0+2*padding, y1-y0+2*padding, height),
                                  matname='dielectric')
    box.color = (0, 100, 0)
    box.transparency = 0.8

    gnd = hfss.modeler.create_rectangle('XY', 
                                        (x0-padding, y0-padding, -height), 
                                        (x1-x0+2*padding, y1-y0+2*padding))
    
    
    hfss.assign_perfecte_to_sheets(gnd)
    hfss.modeler.fit_all()
    
    x0, y0, z0 = points[0]
    port1 = hfss.modeler.create_rectangle('YZ', 
                                         (x0, y0-width/2, 0), 
                                         (width, -height), name='p1')
    hfss.lumped_port(port1, integration_line=hfss.AXIS.Z)
    
    x1, y1, z1 = points[-1]
    port2 = hfss.modeler.create_rectangle('XZ', 
                                         (x1-width/2, y1, 0), 
                                         (-height, width))
    hfss.lumped_port(port2, integration_line=hfss.AXIS.Z)
    
    hfss.create_open_region('1000GHz')
    
    setup = hfss.create_setup('mysetup')
    setup.props['MaxDeltaS'] = 0.01
    setup.props['MinimumConvergedPasses'] = 2   
    setup.props['Frequency'] = '1GHz'
    setup.props['MaximumPasses'] = 20
    
    hfss.create_linear_step_sweep('mysetup', 'GHz', 0.1, 30, 0.1, sweep_type='Interpolating')
    hfss.analyze_nominal(num_cores=6)
    
    L_formula = "1e9*im(1/Y(1,1))/(2*pi*freq)"
    Q_formula = "im(1/Y11)/re(1/Y11)"
    
    hfss.create_output_variable("L", L_formula, solution="mysetup : LastAdaptive")
    hfss.create_output_variable("Q", Q_formula, solution="mysetup : LastAdaptive")    
    
    data = hfss.post.get_solution_data([L_formula])
    L = data.data_real()
    freq = data.primary_sweep_values
    data = hfss.post.get_solution_data([Q_formula])
    Q = data.data_real()
    
    Qmax, fopt = max(zip(Q, freq))
    Lopt = L[freq.index(fopt)]
    #hfss.release_desktop(True, False)
    
    return Lopt, Qmax, fopt

Lopt, Qmax, fopt = spiral()
print(Lopt, Qmax, fopt)

```