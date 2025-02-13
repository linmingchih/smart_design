如何查找 PyAEDT 函數與屬性
---

## 1. 簡介
PyAEDT 是 ANSYS 開發的 Python 模組，允許使用者透過 API 操控 AEDT，進行模擬自動化。這個工具提供了與 AEDT 互動的強大能力，使工程師能夠編寫 Python 腳本來自動化設計與分析過程。對於許多初學者來說，一個常見的問題是如何在 PyAEDT 中找到對應的函數或屬性。本文件將提供一個快速且系統化的方法來幫助使用者查找所需的 API，進而提升開發效率。

## 2. PyAEDT 與 AEDT GUI 的對應關係
PyAEDT 的函數和屬性與 AEDT GUI 的組織方式相似。AEDT 的 GUI 界面包含不同的功能模組，例如 3D 建模、模擬設置、解算與結果分析等。而 PyAEDT 提供的函數和屬性則對應於這些 GUI 模組。因此，如果使用者熟悉 AEDT 的 GUI 佈局，就能更快地找到對應的函數或屬性來執行相同的操作。

**以下是一些AEDT的功能分類：**
- 建模：用於創建和編輯 3D 幾何結構。
- 模擬設定：包括設置模擬類型、求解器參數等。
- 材料設定：定義和分配材料屬性。
- 網格劃分：生成並優化計算所需的網格。
- 求解與後處理：執行模擬並分析結果。

## 3. 使用 dir 函數列出可用的函數與屬性
在 Python 的 IDE 或 Console 中，可以使用 `dir()` 函數來探索物件內的所有函數與屬性。例如：

```python
from pyaedt import Hfss
app = Hfss()
print(dir(app))
```

執行上述指令後，將會列出 `app` 物件內所有可能的函數與屬性。這有助於使用者快速掌握可用的功能。

在 `dir()` 的輸出中，可能會包含許多內部函數與開發者 API：
- 以底線 `_` 開頭的函數或屬性（如 `__init__`）通常是 API 開發者使用的，可忽略。
- 以動詞開頭的名稱通常是函數（例如 `create_box`、`analyze`），這些函數對應於 GUI 中的操作，可使用 `help()` 來查詢詳情。
- 以名詞開頭的名稱通常是屬性（例如 `solution_type`、`modeler`），這些屬性代表 AEDT 內部的物件或設置，可直接存取其值。

舉例，在IDE console輸入app.create_new_project，按下Enter，返回：
```bash
In [6]: app.create_new_project
Out[6]: <bound method Design.create_new_project of <ansys.aedt.core.hfss.Hfss object at 0x000001B5E9FA58D0>>
```
bound method說明app.create_new_project是一個函數，函數需要調用並給定正確的參數才能正確動作，如何查找app.create_new_project的參數？對於函數，可以使用 `help()` 來獲取詳細資訊，例如：

```python
In [7]: help(app.create_new_project)
Help on method create_new_project in module ansys.aedt.core.application.design:

create_new_project(name) method of ansys.aedt.core.hfss.Hfss instance
    Create a project within AEDT.
    
    Parameters
    ----------
    name :
        Name of the project.
    
    Returns
    -------
    bool
        ``True`` when successful, ``False`` when failed.
    
    References
    ----------
    >>> oDesktop.NewProject
```

此命令會顯示 `create_new_project` 函數的功能、參數與返回值，幫助使用者了解如何使用該函數。

### 直接存取屬性值
如果名稱是屬性（名詞開頭），可以直接存取其值，例如：

```python
In [8]: app.design_name
Out[8]: 'HFSS_JRU'
```
有些屬性可以直接修改
```python
In [13]: app.design_name = 'new_design'
```
有些則不支援直接修改，這需要嘗試過才知道。

屬性值的類型可能包括：
- 整數、浮點數、字串等基本類型。
- `list`、`tuple`、`dictionary` 等資料結構。
- 另一個物件（例如 `app.modeler` 是一個物件，代表幾何建模工具）。

如果屬性是另一個物件，可以再次使用 `dir()` 來進一步探索，例如：

```python
print(dir(app.modeler))
```

這將顯示 `modeler` 物件內的所有函數與屬性，幫助使用者更深入理解 AEDT 的內部結構。

```python
In [11]: app.modeler
Out[11]: <ansys.aedt.core.modeler.modeler_3d.Modeler3D at 0x1b5e86bcca0>

In [12]: dir(app.modeler)
Out[12]: 
['Position',
 'SweepOptions',
 '_GeometryModeler__refresh_object_type',
 '_Primitives3D__create_temp_project',
 '_Primitives3D__get_all_mapping',
 ...
```
這裡的 app.modeler 是一個 Modeler3D 類別的物件，可以使用 dir() 來探索其可用屬性與方法。其中包含各種 2D、3D 建模函數，例如 create_box。若要查詢 create_box 的參數，可使用 help(app.modeler.create_box)，其他函數也可依此方式查找詳細資訊。

```python
In [19]: help(app.modeler.create_box)
Help on method create_box in module ansys.aedt.core.modeler.cad.primitives_3d:

create_box(origin, sizes, name=None, material=None, **kwargs) method of ansys.aedt.core.modeler.modeler_3d.Modeler3D instance
    Create a box.
    
    Parameters
    ----------
    origin : list
        Anchor point for the box in Cartesian``[x, y, z]`` coordinates.
    sizes : list
       Length of the box edges in Cartesian``[x, y, z]`` coordinates.
    name : str, optional
        Name of the box. The default is ``None``, in which case the
        default name is assigned.
    material : str, optional
        Name of the material.  The default is ``None``, in which case the
        default material is assigned. If the material name supplied is
        invalid, the default material is assigned.
    
    Returns
    -------
    :class:`ansys.aedt.core.modeler.cad.object_3d.Object3d` or bool
        3D object or ``False`` if it fails.
    
    References
    ----------
    >>> oEditor.CreateBox
    
    Examples
    --------
    This example shows how to create a box in HFSS.
    The required parameters are ``position`` that provides the origin of the
    box and ``dimensions_list`` that provide the box sizes.
    The optional parameter ``matname`` allows you to set the material name of the box.
    The optional parameter ``name`` allows you to assign a name to the box.
    
    This method applies to all 3D applications: HFSS, Q3D, Icepak, Maxwell 3D, and
    Mechanical.
    
    >>> from ansys.aedt.core import hfss
    >>> hfss = Hfss()
    >>> origin = [0,0,0]
    >>> dimensions = [10,5,20]
    >>> box_object = hfss.modeler.create_box(origin=origin,sizes=dimensions,name="mybox",material="copper")

```
## 4. 函數返回為物件
函數的返回值可能是另一個物件，例如在 PyAEDT 中，某些 API 方法會返回特定的類別物件，讓使用者能夠進一步操作。例如：

```python
In [21]: box = app.modeler.create_box([0, 0, 0], [10, 10, 10])
```
這裡的 create_box() 返回一個 Object3D 物件，該物件包含各種屬性與方法，我們可以呼叫函數或修改屬性。

```python
In [25]: box.material_name
Out[25]: 'vacuum'

In [26]: box.material_name = 'copper'
```

透過這種方式，PyAEDT 提供了物件導向的操作流程，使開發更具模組化與靈活性。


## 5. 結論
透過上述方法，使用者可以迅速在 PyAEDT 中定位對應的函數與屬性，提升開發效率。熟悉 AEDT GUI 的組織方式將進一步加速這個過程，使開發者更容易找到適用的 API 來實現模擬自動化。例如，app.mesh 包含所有與網格（mesh）相關的屬性與修改函數，而 app.post 則負責報表（report）與數據擷取。善用 dir()、help() 等內建工具，不僅能高效探索 PyAEDT，還能提升程式開發的靈活性與準確性，加快開發迭代速度。

其他
- 使用進階 IDE 如 Spider，可以直接將函數拖曳到 Help 欄位，排版過的內容更便於閱讀。
- 在 GitHub 上搜尋相關關鍵字，也能幫助找到相關的函數或屬性。
- 如果還是找不到，可以聯繫 ANSYS 的技術支援尋求幫助。

![2025-02-13_15-52-41](/assets/2025-02-13_15-52-41.png)

