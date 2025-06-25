第3章 使用 PyAEDT 進行 TDR（時域反射）分析
---

這個範例中使用了電路模擬器（Circuit）來設計和分析一個差分時域反射計（TDR）的設置。以下是這段代碼各部分的功能說明：

> [pcie.s4p下載](https://github.com/linmingchih/smart_design/blob/main/assets/pcie.s4p)

1. **初始化電路模擬器** : 
  - `Circuit(non_graphical=True)`：創建一個新的Circuit對象，`non_graphical=True`表示在無圖形介面模式下運行，適用於腳本化和自動化流程。
 
2. **導入和創建元件** : 
  - `create_model_from_touchstone`：從Touchstone文件（這裡是`pcie.s4p`）導入一個模型。Touchstone文件通常用於描述網絡參數，如S參數。
 
  - `create_touchstone_component`：在電路中創建一個基於導入的Touchstone文件的元件。
 
  - `create_component`和`create_resistor`：創建其他需要的元件，包括探針和電阻。
 
3. **建立連接** : 
  - `connect_schematic_components`：將元件按指定的端口連接起來。例如，將Touchstone元件的端口連接到探針和電阻上，並將電阻接地。
 
4. **設置分析** : 
  - `create_setup`：創建一個新的仿真設置，指定仿真類型為`NexximTransient`，設定仿真的時間範圍。
 
  - `analyze_all`：執行所有設置的仿真。
 
5. **生成和導出報告** : 
  - `create_report`：生成報告，此處生成差分時域反射報告。
 
  - `export_report_to_jpg`：將報告導出為JPEG格式，儲存至指定路徑。

這個代碼的用途在於透過腳本自動設計和分析電子電路，特別是在信號完整性分析中常用的時域反射測量。這種自動化流程可以大幅節省手動設置和分析的時間，並且可以方便地集成到更大的設計和測試流程中。

```python
from pyaedt import Circuit

circuit = Circuit()

circuit.modeler.components.create_model_from_touchstone(r"c:/demo/pcie.s4p")

#%%
s1 = circuit.modeler.components.create_touchstone_component('pcie')
x, y = s1.location
probe = circuit.modeler.components.create_component('a1', 
                                                    'Probes',
                                                    'TDR_Differential_Ended',
                                                    location=(x-0.02, y)
                                                    ,angle=90)
rp = circuit.modeler.components.create_resistor(location=(x+0.02, y+0.01))
rn = circuit.modeler.components.create_resistor(location=(x+0.02, y-0.01))

x, y = location=rp.pins[0].location
g1 = circuit.modeler.components.create_gnd(location=(x, y-0.0025))
x, y = location=rn.pins[0].location
g2 = circuit.modeler.components.create_gnd(location=(x, y-0.0025))


circuit.modeler.components.create_wire([probe.pins[1].location, 
                                        s1.pins[0].location])

circuit.modeler.components.create_wire([probe.pins[0].location, 
                                        s1.pins[1].location])

circuit.modeler.components.create_wire([rp.pins[1].location, 
                                        s1.pins[2].location])

circuit.modeler.components.create_wire([rn.pins[1].location, 
                                        s1.pins[3].location])


setup = circuit.create_setup('mysetup', 'NexximTransient')
setup.props['TransientData'] = ['10ps', '10ns']
circuit.analyze()

report = circuit.post.create_report(f"O(A{probe.id}:zdiff)", 
                                    domain='Time',
                                    primary_sweep_variable='Time',
                                    variations={"Time": ["All"]},
                                    plotname='differential_tdr')
circuit.post.export_report_to_jpg('c:/demo',  report.plot_name)

```
![differential_tdr](/assets/differential_tdr.jpg)

---

### 🧠 PyAEDT 與物件導向程式設計（OOP）概念說明

物件導向是一種用「物件」來模擬現實世界的方法。在 PyAEDT 中，我們將一個電路設計看成是一個「物件」，並透過這個物件去建立元件、連接線路、設定模擬與產生報表。每個物件都包含：

- **屬性（Attributes）**：例如元件的名稱、ID、阻值等特性
- **方法（Methods）**：可以對物件做的事情，例如建立元件、連接、執行模擬

#### 🕰 生活中的物件導向例子：手錶

為了幫助初學者理解，舉一個日常生活的例子：「手錶」也是一個物件。

- **屬性（Attributes）**：品牌、顏色、時間、電池狀態、錶帶材質
- **方法（Methods）**：顯示時間、設定鬧鐘、啟動碼錶、切換模式、開啟背光

我們可以這樣理解：你有一支手錶（物件），可以讀取現在時間（方法），也可以修改它的顏色或更換錶帶（修改屬性）。這和程式中我們對電路物件操作的邏輯是一樣的。例如你設定鬧鐘，就是呼叫方法；而你調整時間格式，就是在修改屬性。

---

#### 📘 程式碼解析

```python
from pyaedt import Circuit

circuit = Circuit(non_graphical=True)
```
這裡 `Circuit` 是一個類別（Class），我們透過它建立了 `circuit` 物件。這個物件代表我們的電路環境，可以讓我們操作各種模擬功能，如元件建立、參數設定與模擬分析。

```python
s1 = circuit.modeler.components.create_touchstone_component('pcie')
probe = circuit.modeler.components.create_component('a1', 'Probes','TDR_Differential_Ended')
```
這段是透過 `circuit.modeler.components` 建立元件。這些方法會**回傳一個元件物件（component object）**，例如 `s1` 或 `probe`，每個元件都可以有自己的名稱、編號、屬性與行為。

#### 🔁 修改物件屬性與物件巢狀結構

當方法回傳一個元件物件後，我們可以修改它的屬性，例如：

```python
rp = circuit.modeler.components.create_resistor()
rp.parameters["R"] = "50ohm"
```
這裡 `rp` 是一個電阻元件物件，我們對它的 `parameters` 屬性指定一個阻值。這就是物件導向程式設計的精神：**我們對物件下指令，並根據需要修改它的內容。**

同時，要特別注意：
- **方法回傳的本身可以是一個新的物件**，例如 `create_resistor()` 回傳的就是電阻元件物件；
- **屬性也可能是物件**，例如 `circuit.modeler` 是一個「建模器」物件，它裡面還有 `components` 屬性（也是一個物件），可以再呼叫方法來建立元件；
- **物件之間可以層層巢狀**，形成清晰的結構，也讓使用者能有條理地管理模擬元件與設定。

這種設計不僅有助於組織與管理，還能透過共通方法與介面，提升模組的重複使用性與可維護性。

#### 🔍 查詢物件有哪些屬性與方法

Python 提供兩個內建函式可以幫助我們快速探索物件：

```python
print(dir(rp))   # 列出 rp 物件所有可以使用的屬性與方法
help(rp)         # 顯示 rp 的詳細說明文件
```
這對初學者非常有幫助，可以了解物件有哪些功能、能做什麼操作，並協助寫程式時避免錯誤。例如當你不知道某個模組是否支援某項操作時，先用 `dir()` 看看它有什麼方法，再用 `help()` 詳讀使用方式。

#### 🔌 元件連接與模擬

```python
circuit.modeler.connect_schematic_components(s1.composed_name, probe.composed_name, 1, 1)
```
這是透過 `connect_schematic_components()` 方法，將元件的引腳互相連接。透過物件名稱與屬性，我們可以精確地指定每個元件的連接方式，讓整體電路圖自動生成，避免人工操作錯誤。

#### ⚙️ 建立模擬與後處理

```python
setup = circuit.create_setup('mysetup', 'NexximTransient')
setup.props['TransientData'] = ['10ps', '10ns']
```
這裡 `create_setup()` 會回傳一個模擬設定物件 `setup`，我們可以透過它的 `props` 屬性來修改模擬參數。像是時間步長、模擬長度等，都可以直接在屬性中設定。

```python
report = circuit.post.create_report(...)
circuit.post.export_report_to_jpg(...)
```
最後透過 `post` 物件，我們可以產生報表並輸出圖片。這些動作都能以腳本實現，方便重複模擬、版本控制與報表生成自動化。

---

#### ✅ 小結
- 每個模組都是一個物件（如 `circuit`, `setup`, `s1`）
- 方法可以建立新物件（例如元件、模擬設定）
- 回傳的物件可以再進一步修改其屬性（如參數、名稱）
- 屬性與方法本身也可能是其他物件，可再深入操作
- 可以用 `dir()` 與 `help()` 查詢物件有哪些方法與功能
- 物件可以巢狀結構化，讓整個模擬架構更有彈性與可讀性
- 透過清楚的結構與分工，PyAEDT 讓電路模擬工作流程更具模組化、可擴充性與自動化潛力

### 網表版


```python
from pyaedt import Circuit

path = 'c:/demo/pcie.s4p'
 
netlist = f'''
.model channel S TSTONEFILE="{path}"
+ INTERPOLATION=LINEAR INTDATTYP=MA HIGHPASS=10 LOWPASS=10 convolution=0 enforce_passivity=0 Noisemodel=External

S26656 net_1 net_2 net_3 net_4 FQMODEL="channel"

R11185 net_3 0 50 
R60784 net_4 0 50 

'''

with open('c:/demo/tdr.cir', 'w') as f:
    f.write(netlist)
    
circuit = Circuit()
probe = circuit.modeler.components.create_component('a1', 
                                                    'Probes',
                                                    'TDR_Differential_Ended',)

circuit.modeler.components.create_page_port('net_1', location=probe.pins[0].location)
circuit.modeler.components.create_page_port('net_2', location=probe.pins[1].location)


circuit.add_netlist_datablock('c:/demo/tdr.cir')

setup = circuit.create_setup('mysetup', 'NexximTransient')
setup.props['TransientData'] = ['10ps', '10ns']
circuit.analyze()

report = circuit.post.create_report(f"O(A{probe.id}:zdiff)", 
                                    domain='Time',
                                    primary_sweep_variable='Time',
                                    variations={"Time": ["All"]},
                                    plotname='differential_tdr')
circuit.post.export_report_to_jpg('c:/demo',  report.plot_name)

```