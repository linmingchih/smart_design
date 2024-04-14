AEDT XML 控制檔案介紹
---

GDSII檔案主要被用於描述集成電路的圖形設計資料，但它不包含材料的物理或電氣特性等製程相關資訊。因此，在進行電磁場模擬時，僅有GDSII檔案是不足夠的。要進行有效的模擬，必須知道每一層的具體物理和電氣特性，這些資訊通常包含在控制檔案中。

AEDT支援多種格式的控制檔，例如： 
- `*.xml` AEDT標準結構化控制檔案，也是我們本書要介紹的格式
- `*.tech`  
- `*.layermap`  
- `*.ircx` 和 `*.itf` 
- `*.vlc.tech` 

控制檔案充當GDSII資料和模擬軟體之間的橋梁，它包含了層的對應、厚度、連結方式以及材料特性等重要資訊。例如，AEDT使用XML格式的控制檔案來實現這一功能。這個XML檔案詳細描述了每層的配置、物理和電氣特性（如導電係數、介電常數等），以及結構簡化、網絡（Nets）、端口（Port）等額外元素。

因此，將GDSII檔案與相應的XML控制檔案結合使用，可以建構出一個完整的模型，這個模型不僅包含了設計的幾何資訊，還融合了進行精確模擬所需的所有材料和結構特性。

### XML基本語法
XML（Extensible Markup Language）是一種標記語言，它讓文檔具有結構化的格式，並且能夠在不同的系統和設備之間交換數據。XML 非常類似 HTML，但是它是自我描述性的，並且可以定義用戶自己的標籤。以下是一些 XML 基本語法的介紹，特別適合入門者了解：
#### I. XML 文檔的結構

XML 文檔由許多元素組成，基本結構包括： 
- **標籤（Tags）** ：元素的名稱，被尖括號包圍。例如：`<tagname>` 表示開始標籤，`</tagname>` 表示結束標籤。 
- **元素（Elements）** ：由一個開始標籤和一個結束標籤，以及其中的內容組成。例如：`<greeting>你好, 世界!</greeting>`。 
- **屬性（Attributes）** ：在開始標籤中提供額外信息。格式為 `key="value"`。例如：`<student grade="A">張三</student>`。
#### II. 規則

XML 有一些基本規則需要遵循：
- 每個開始標籤都必須有對應的結束標籤。 
- 標籤對大小寫敏感，`<Tag>` 和 `<tag>` 被認為是不同的標籤。 
- 正確的嵌套是必須的。例如，`<b><i>text</i></b>` 是正確的，但 `<b><i>text</b></i>` 是錯誤的。
- 屬性值必須被引號包圍。
#### III. XML 聲明

一個 XML 文檔的開頭通常包含一個 XML 聲明，它聲明了文檔的 XML 版本和字符編碼。例如：

```xml
<?xml version="1.0" encoding="UTF-8"?>
```


#### IV. 註解

XML 中的註解可以使用 `<!-- 註解內容 -->` 來添加，註解的內容不會被處理。例如：

```xml
<!-- 這是一個註解 -->
```


#### V. 實例

以下是一個簡單的 XML 實例：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<greetings>
    <greeting>你好, 世界!</greeting>
    <greeting language="English">Hello, world!</greeting>
</greetings>
```


### AEDT 控制檔 XML介紹
AEDT 採用了XML格式，並制定了一組完整的schema（模式定義），用以定義數據的結構、描述文檔中哪些元素可以出現以及它們如何出現。每個頂層標籤代表了XML文件中的一個重要部分，通過這些頂層標籤（如`Stackup`、`Geometry`、`Components`等） ，確定了電路板設計的各個方面，包括物理布局、電氣特性和模擬參數等。這樣的結構設計使得數據組織清晰，並支持軟件在解析和操作這些數據時，能夠根據預定的規則和標準進行。下面介紹這些頂層元素及其用途：

1. **Stackup（堆疊）** ：此元素用於定義電路板的材料、層次和通孔（vias）。它對於確定電路板的物理和電氣屬性非常重要。 
2. **Geometry（幾何）** ：此元素允許在轉換輸出中加入多邊形。這在設計中用於定義形狀和布局。 
3. **Boundaries（邊界）** ：在GDS轉換中，此元素主要用於點位基礎的電路端口創建和定義HFSS的範圍。這對於電磁模擬尤其重要。 
4. **Components（組件）** ：選擇組件的架構版本。這對於確保設計元件與設計工具兼容非常關鍵。 
5. **CutoutSubdesign（切割子設計）** ：可以對多邊形執行幾何剪裁。這在需要對特定區域進行細節調整時非常有用。 
6. **SimulationSetups（模擬設置）** ：定義HFSS模擬設置和掃描。這是進行電磁性能分析前的重要步驟。 
7. **ImportOptions（導入選項）** ：指定各種導入選項，如文件格式和轉換規則，以確保數據正確載入。 
8. **GDS_CELL_RULES（GDS單元規則）** ：控制導入哪些單元。這有助於管理大型設計中的元件和層次。 
9. **GDS_NET_DEFINITIONS（GDS網絡定義）** ：允許您定義VDD（正電壓）、Ground（接地）和Signal（信號）網。這對於電路的電氣連接至關重要。 
10. **GDS_COMPONENTS（GDS組件）** ：用於創建組件群組。可以通過GDS_AUTO_COMPONENT元素自動完成這一過程。

以上各元素在XML控制文件中扮演著不同的角色，合理使用這些元素能夠有效地控制和優化電子設計和模擬過程。

> :memo: **附註**<br>關於AEDT XML語法細節可以參考**HFSS 3D Layout Help**當中'GDS Translation Using XML Control Files (ECAD Xplorer)'章節。


### 簡單XML範例
以下是一個只包含 `Stackup` 標籤的簡單XML範例：

```xml
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<c:Control xmlns:c="http://www.ansys.com/control" schemaVersion="1.0">
	<Stackup schemaVersion="1.0">
		<Materials>
			<Material Name="m1_cond">
				<Conductivity>
					<Double>43000000</Double>
				</Conductivity>
			</Material>
			<Material Name="m2_cond">
				<Conductivity>
					<Double>43000000</Double>
				</Conductivity>
			</Material>
			<Material Name="via_cond">
				<Conductivity>
					<Double>43000000</Double>
				</Conductivity>
			</Material>
			<Material Name="IMD_A">
				<Permittivity>
					<Double>3.23</Double>
				</Permittivity>
			</Material>
			<Material Name="IMD_B">
				<Permittivity>
					<Double>2.8</Double>
				</Permittivity>
			</Material>
		</Materials>
		<ELayers LengthUnit="um">
			<Dielectrics>
				<Layer Name="IMD8" Material="IMD_B" Thickness="0.5"/>
				<Layer Name="IMD7" Material="IMD_A" Thickness="0.1"/>
				<Layer Name="IMD6" Material="IMD_B" Thickness="0.1"/>
				<Layer Name="IMD5" Material="IMD_A" Thickness="0.1"/>
				<Layer Name="IMD4" Material="IMD_B" Thickness="0.1"/>
				<Layer Name="IMD3" Material="IMD_A" Thickness="0.1"/>
				<Layer Name="IMD2" Material="IMD_B" Thickness="3"/>
				<Layer Name="IMD1" Material="IMD_A" Thickness="1"/>
			</Dielectrics>
			<Layers>
				<Layer Name="300" Material="m1_cond" GDSDataType="0" TargetLayer="metal1" Type="conductor" Thickness="0.5" Elevation="1"/>
				<Layer Name="200" Material="m2_cond" GDSDataType="0" TargetLayer="metal2" Type="conductor" Thickness="0.5" Elevation="4"/>
			</Layers>
			<Vias>
				<Layer Name="100" Material="via_cond" GDSDataType="0" TargetLayer="via12" StartLayer="metal1" StopLayer="metal2">
					<CreateViaGroups Method="proximity" Tolerance="5um" CheckContainment="true"/>
					<SnapViaGroups Method="areaFactor" Tolerance="3" RemoveUnconnected="true"/>
				</Layer>
			</Vias>
		</ELayers>
	</Stackup>
</c:Control>
```

以上這個XML文件是一個控制文件，用於描述一個堆疊結構（Stackup）及其材料特性。來設定模型的不同層的物理和電氣參數。以下為逐段解釋：

1. **XML聲明** : `<?xml version="1.0" encoding="UTF-8" standalone="no" ?>` 定義了這是一個XML文件，使用UTF-8編碼，並非獨立文件（意味著可能有外部實體或者DTD）。 
2. **Control元素** : `<c:Control xmlns:c="http://www.ansys.com/control" schemaVersion="1.0">` 定義了XML命名空間，並指出這是用於ANSYS控制文件的根元素。 
3. **Stackup** : `<Stackup schemaVersion="1.0">` 標記了堆疊結構的開始，包括使用的材料和層的定義。 
4. **Materials** : `<Materials>` 定義了在電路堆疊中用到的所有材料的電性。
	- m1_cond、m2_cond、via_cond：這些是導電材料，電導率為43000000 S/m。
	- IMD：這是一種介電材料，其介電常數為3.23。 
5. **ELayers** : `<ELayers LengthUnit="um">` 定義了電路的每一層，包括介電層和導體層，並指定了長度單位為微米（um）。 
6. **Dielectrics** : `<Dielectrics>` 指出了介電層的配置。介電層在XML文件中按照一定的順序獨立定義，而這個順序在導入到AEDT後會被保留。注意以下幾點：
	- 介電層的順序是按照它們在XML中的列出順序來維持的。
	- 導入AEDT後，最上面的介電層（Topmost dielectric）會處於最頂部。
	- 所有的介電層都是連續的，這意味著它們將會緊密地堆疊在一起，沒有間隙。

7. **Layers** : `<Layers>` 定義了導體層的相關資訊。
	- 層200對應於GDSII的metal1，層300對應於metal2。這些層使用m1_cond和m2_cond材料，厚度均為0.5微米，且分別位於電路板的1和4微米高度位置。 
8. **Vias** : `<Vias>` 定義了通孔層的配置。
	- 層100使用via_cond材料，表示這是一個通孔，從metal1層開始，到metal2層結束。

這個XML控制文件通常在將GDSII數據導入到3D Layout之前被創建，以確保所有的層都有正確的物理和電氣特性。


### 2.3 實驗操作
#### I. 匯入控制檔
按照之前Lab 1所學匯入GDSII方法，匯入example.gds。在跳出GDS Import視窗視窗之後，點擊“Import control file…”按鈕來導入一個控制檔案example.xml。

![2024-04-12_12-27-05](/assets/2024-04-12_12-27-05.png)

我們可以觀察到以下數值的變化：
1. **層級(Layers)順序重新排列：**
在上方的截圖中，列出了三個層級100、200和300依序排列。在下方的截圖中，層級300、100和200的順序按照XML當中的Elevation定義被重新排列，

2. **導入層名稱(Import layer name)** :
	- 上方截圖顯示“Import layer name”列與"File layer name"內容相同。
	- 下方截圖展示了層級300、100和200分別對應到“metal2”、“via1”和“metal1”，這表明XML已經對應了GDSII檔案中的層級到特定的堆疊層名稱。 

3. **型別改變**
觀察編號為100的layer，型別變成via。且其Lower (下界) 和 Upper (上界)分別對應到「metal1」和「metal2」。表示layer 100（via12）是連接metal1層和metal2層的通孔。這兩個欄位定義了通孔的上下連接界限。

4. **介電層加入** 
我們看到了在導入介面下方新增了一個名為“Dielectrics”的區塊，並且具體列出了一層名為“IMD”的介電層。

#### II. 預覽堆疊及GDS Cells

GDS Import Window 右下角的按鈕**Preview Stackup**按鈕是用於預覽目前設定層疊結構的功能。點擊該按鈕後，應該會顯示一個視覺化的層疊預覽，就像在圖片中間所見到的那樣。這個預覽會呈現不同材料層的堆疊次序和厚度，以幫助用戶理解實際結構。

「Preview Stackup」按鈕允許用戶在最終確認並導入檔案之前，檢視每層的物理特性，例如材料、厚度等，這對於電路板設計和半導體製造流程中的規劃和驗證非常重要。這有助於預測元件的電氣性能並確保設計符合技術要求。

![2024-04-14_09-15-08](/assets/2024-04-14_09-15-08.png)

GDS Import Window 右下角的按鈕**Summary**可以開啟箭頭所指的「GDSII Cell Summary」視窗。當你進行 GDSII 檔案的導入配置後，點擊「Summary」按鈕後，系統會彙總所導入設計中的元件資訊，如單元格的數量和形狀類型等，並在「GDSII Cell Summary」視窗中顯示出來。

![2024-04-14_09-16-30](/assets/2024-04-14_09-16-30.png)

#### III. 檢視匯入結構

![2024-04-14_09-18-17](/assets/2024-04-14_09-18-17.png)