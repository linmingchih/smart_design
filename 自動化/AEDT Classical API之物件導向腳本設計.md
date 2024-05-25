AEDT Classical API之物件導向腳本設計
---

物件導向腳本增強了AEDT中的腳本功能，使其能夠以物件導向的方式檢索或修改物件屬性。這樣做的主要好處是，能夠更輕鬆地讀取、修改和設置AEDT項目或設計中的各種現有物件屬性。這項功能還允許編寫更少的代碼來訪問物件屬性，使代碼更加易讀，避免了複雜的數組輸入。

在物件導向腳本中，有五種基本函數用於檢索和設置屬性：
1. GetChildNames()
2. GetChildObject()
3. GetPropNames()
4. GetPropValue() / GetPropSIValue()
5. SetPropValue()

在高層次上，可以使用GetChildNames()來確定特定物件的實例。下面的示例顯示了一些以物件導向讀取AEDT屬性的函式碼。

### 示例

1. **取得專案底下變數及其數值**
    ```python
    oProject = oDesktop.GetActiveProject()

    for var_name  in oProject.GetChildObject("Variables").GetPropNames():
        var_obj = oProject.GetChildObject("Variables/{}".format(var_name))
        print(var_name, var_obj.GetPropSIValue())
    ```
    輸出
    ```bash
    $x 4.0
    $y 2.0
    $xy 6.0
    ```
2. **取得材料屬性**
    ```python
    oProject = oDesktop.GetActiveProject()

    vacuum = oProject.GetChildObject("Materials/vacuum")
    for prop_name in vacuum.GetPropNames():
        print(prop_name, ':', vacuum.GetPropSIValue(prop_name))
    ```
    輸出
    ```bash
    oordinate System Type : nan
    Coordinate System Type/Choices : ['Cartesian', 'Cylindrical', 'Spherical']
    Relative Permittivity Type : nan
    Relative Permittivity Type/Choices : ['Simple', 'Anisotropic', 'Nonlinear']
    Relative Permittivity : 1.0
    Relative Permeability Type : nan
    Relative Permeability Type/Choices : ['Simple', 'Anisotropic', 'Nonlinear']
    Relative Permeability : 1.0
    Bulk Conductivity Type : nan
    Bulk Conductivity Type/Choices : ['Simple', 'Anisotropic', 'Nonlinear']
    Bulk Conductivity : 0.0
    Dielectric Loss Tangent Type : nan
    Dielectric Loss Tangent Type/Choices : ['Simple', 'Anisotropic']
    Dielectric Loss Tangent : 0.0
    Magnetic Loss Tangent Type : nan
    Magnetic Loss Tangent Type/Choices : ['Simple', 'Anisotropic']
    Magnetic Loss Tangent : 0.0
    Electric Coercivity Type : nan
    Electric Coercivity Magnitude : 0.0
    Magnetic Coercivity Type : nan
    Magnetic Coercivity Magnitude : 0.0
    Thermal Conductivity Type : nan
    Thermal Conductivity Type/Choices : ['Simple', 'Anisotropic']
    Thermal Conductivity : 0.0
    Magnetic Saturation Type : nan
    Magnetic Saturation : 0.0
    Lande G Factor Type : nan
    Lande G Factor : 2.0
    Delta H Type : nan
    Delta H : 0.0
    -  Measured Frequency Type : nan
    -  Measured Frequency : 9400000000.0
    Core Loss Model : nan
    Core Loss Model/Choices : ['None', 'Electrical Steel', 'Power Ferrite', 'B-P Curve']
    Mass Density Type : nan
    Mass Density : 0.0
    Composition : nan
    Composition/Choices : ['Solid', 'Lamination', 'Litz Wire']
    Specific Heat Type : nan
    Specific Heat : 0.0
    Young's Modulus Type : nan
    Young's Modulus Type/Choices : ['Simple', 'Anisotropic']
    Young's Modulus : 0.0
    Poisson's Ratio Type : nan
    Poisson's Ratio Type/Choices : ['Simple', 'Anisotropic']
    Poisson's Ratio : 0.0
    Thermal Expansion Coefficient Type : nan
    Thermal Expansion Coefficient Type/Choices : ['Simple', 'Anisotropic']
    Thermal Expansion Coefficient : 0.0
    Magnetostriction Type : nan
    Inverse Magnetostriction Type : nan
    Thermal Material Type : nan
    Thermal Material Type/Choices : ['Solid', 'Fluid']
    Solar Behavior : nan
    Solar Behavior/Choices : ['Opaque', 'Transparent']
    ```

3. **輸出所有模型及其對應之材料**

    ```python
    oProject = oDesktop.GetActiveProject()

    modeler = oProject.GetChildObject("HFSSDesign1/3D Modeler")
    for name in modeler.GetChildNames():
        obj = modeler.GetChildObject(name)
        if 'Material' in obj.GetPropNames():
            print(name, ':', obj.GetPropValue('Material'))
    ```
    輸出
    ```bash
    board : "FR4_epoxy"
    board2 : "FR4_epoxy"
    body : "modified_epoxy"
    gnd : "copper"
    pad1 : "copper"
    pin1 : "copper"
    pad2 : "copper"
    pad3 : "copper"
    pad4 : "copper"
    pin2 : "copper"
    pin3 : "copper"
    pin4 : "copper"
    air_box : "vacuum"
    ```