XML 控制檔案介紹
---

GDSII檔案主要被用於描述集成電路的圖形設計資料，但它不包含材料的物理或電氣特性等製程相關資訊。因此，在進行電磁場模擬時，僅有GDSII檔案是不足夠的。要進行有效的模擬，必須知道每一層的具體物理和電氣特性，這些資訊通常包含在控制檔案中。

AEDT支援多種格式的控制檔，例如： 
- `*.xml` AEDT標準結構化控制檔案。 
- `*.tech` 可能是某些技術或設計軟體的特定格式。 
- `*.layermap` 可能指的是包含圖層信息的映射文件。 
- `*.ircx` 和 `*.itf` 可能是特定行業或軟體的專用檔案格式。 
- `*.vlc.tech` 這個擴展名不是很常見，可能是特定軟體的專有格式。

控制檔案充當GDSII資料和模擬軟體之間的橋梁，它包含了層的對應、厚度、連結方式以及材料特性等重要資訊。例如，AEDT使用XML格式的控制檔案來實現這一功能。這個XML檔案詳細描述了每層的配置、物理和電氣特性（如導電係數、介電常數等），以及結構簡化、網絡（Nets）、端口（Port）等額外元素。

因此，將GDSII檔案與相應的XML控制檔案結合使用，可以建構出一個完整的模型，這個模型不僅包含了設計的幾何資訊，還融合了進行精確模擬所需的所有材料和結構特性。

### 2.1 XML基本語法
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


### 2.2 GDSII 控制檔 XML介紹

```xml
<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<c:Control
	xmlns:c="http://www.ansys.com/control" schemaVersion="1.0">
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
			<Material Name="IMD">
				<Permittivity>
					<Double>3.23</Double>
				</Permittivity>
			</Material>
		</Materials>
		<ELayers LengthUnit="um">
			<Dielectrics>
				<Layer Name="IMD" Material="IMD"  Thickness="5"/>
			</Dielectrics>
			<Layers>
				<Layer Name="200" Material="m1_cond" GDSDataType="0" TargetLayer="metal1" Type="conductor" Thickness="0.5" Elevation="1"/>
				<Layer Name="300" Material="m2_cond" GDSDataType="0" TargetLayer="metal2" Type="conductor" Thickness="0.5" Elevation="4"/>
			</Layers>
			<Vias>
				<Layer Name="100" Material="via_cond" GDSDataType="0" TargetLayer="via12"  StartLayer="metal1" StopLayer="metal2"></Layer>
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
6. **Dielectrics** : `<Dielectrics>` 指出了介電層的配置。
	- IMD層使用名為IMD的材料，厚度為5微米。 
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

![2024-04-12_12-31-45](/assets/2024-04-12_12-31-45.png)

GDS Import Window 右下角的按鈕**Summary**可以開啟箭頭所指的「GDSII Cell Summary」視窗。當你進行 GDSII 檔案的導入配置後，點擊「Summary」按鈕後，系統會彙總所導入設計中的元件資訊，如單元格的數量和形狀類型等，並在「GDSII Cell Summary」視窗中顯示出來。

![2024-04-12_12-32-00](/assets/2024-04-12_12-32-00.png)

#### III. 檢視匯入結構

![2024-04-12_12-43-56](/assets/2024-04-12_12-43-56.png)

