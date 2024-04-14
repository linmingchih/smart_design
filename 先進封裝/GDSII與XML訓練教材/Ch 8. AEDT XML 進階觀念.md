AEDT XML 進階觀念
---
XML（Extensible Markup Language，可擴展標記語言）是一種廣泛使用的標記語言，它設計用來儲存和傳輸數據。XML 提供了一種結構化的數據格式，使得數據既可以由機器讀取，也便於人工閱讀。

XML 文件通常包含標籤和文本內容，這些標籤類似於HTML，但用戶可以自定義標籤名稱，以適應不同的數據儲存需求。這種靈活性使得 XML 非常適合於數據交換和網絡服務，如SOAP和REST。

一個典型的 XML 文件可能會這樣構造：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<書籍>
    <書名>XML 簡介</書名>
    <作者>張三</作者>
    <出版年份>2021</出版年份>
    <出版社>科技出版社</出版社>
</書籍>
```

在這個例子中，`<書籍>`、`<書名>`、`<作者>`等是自定義標籤，它們用來描述特定的資訊，並組織成一個結構化的格式。XML 的這種結構化特點使其非常適合於復雜數據的表達和傳輸。

#### Schema
XML Schema（常用副檔名為 `.xsd`）是一種用來描述 XML 文檔結構和驗證 XML 文檔是否符合結構的語言。XML Schema 定義了 XML 文檔中允許的元素、屬性、元素的順序以及元素的數據類型等。

使用 XML Schema 有幾個主要的好處： 
1. **標準化** ：Schema 為 XML 文檔的結構提供了清晰的規範，使得不同的系統和應用程式可以基於共同的標準交換數據。 
2. **數據完整性** ：通過檢查 XML 文檔是否符合預定的 Schema，可以確保數據的準確性和完整性。 
3. **互操作性** ：具有 Schema 支持的應用程式能夠更容易地與其他系統互動，因為它們共享相同的數據結構定義。

一個簡單的 XML Schema 定義範例如下：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
    <xs:element name="書籍">
        <xs:complexType>
            <xs:sequence>
                <xs:element name="書名" type="xs:string"/>
                <xs:element name="作者" type="xs:string"/>
                <xs:element name="出版年份" type="xs:integer"/>
                <xs:element name="出版社" type="xs:string"/>
            </xs:sequence>
        </xs:complexType>
    </xs:element>
</xs:schema>
```



在這個範例中，我們定義了一個 `書籍` 元素，它包含四個子元素：`書名`、`作者`、`出版年份` 和 `出版社`，並且分別指定了它們的數據型別。這樣的 Schema 確保了任何符合此 Schema 的 XML 文件都會有一致的結構和數據類型，從而實現數據的正確交換和處理。

#### 數據讀取
XML 解析器（parser）的工作流程。讓我更詳細地解釋一下這個過程： 
1. **語法檢查** ：XML 解析器首先檢查 XML 文件是否符合基本的 XML 規範，包括標籤的開關是否匹配、屬性是否正確引用、以及文件是否遵守 XML 的結構規則等。這種檢查通常稱為「良好格式」（well-formed）檢查。 
2. **驗證（如果適用）** ：如果 XML 文件與一個 XML Schema（或其他類型的 schema，如 DTD）關聯，解析器會進一步檢查 XML 文件是否符合該 schema 的規則。這包括元素和屬性的數據類型、順序、必需性等方面。這一步稱為「有效性」（validity）檢查。 
3. **數據提取** ：一旦 XML 文件通過了上述的檢查，解析器會解讀文件的內容，並將數據載入到應用程序中，供後續處理使用。這可能包括將數據轉換為對象、插入資料庫或進行其他類型的數據操作。

### AEDT XML技術檔案的Schema
上面提到 AEDT 採用 XML 格式來儲存和管理技術設計數據。為了確保這些數據的一致性和正確性，AEDT 使用特定的 XML Schema 定義（XSD）來標準化 XML 文件的結構。這些 Schema 文件，如 `Stackup.xsd`、`SimulationSetup.xsd` 等，位於軟件安裝目錄下，通常是 C:\Program Files\AnsysEM\v241\Win64。當開發者或使用者需要確認 XML 文件是否支持某一特殊設定，可以直接使用文字編輯器打開這些 XSD 文件進行查找。

比方說開啟`Stackup.xsd`，當中有一段Material屬性的敘述如下：
```xml


  <xsd:complexType name="Material">
    <xsd:all>
      <xsd:element name="Permittivity" type="MaterialProperty" minOccurs="0" />
      <xsd:element name="Permeability" type="MaterialProperty" minOccurs="0" />
      <xsd:element name="Conductivity" type="MaterialProperty" minOccurs="0" />
      <xsd:element name="DielectricLossTangent" type="MaterialProperty" minOccurs="0" />
      <xsd:element name="MagneticLossTangent" type="MaterialProperty" minOccurs="0" />
      <xsd:element name="ThermalConductivity" type="MaterialProperty" minOccurs="0" />
      <xsd:element name="SpecificHeat" type="MaterialProperty" minOccurs="0" />
      <xsd:element name="ThermalExpansionCoefficient" type="MaterialProperty" minOccurs="0" />
      <xsd:element name="MassDensity" type="MaterialProperty" minOccurs="0" />
      <xsd:element name="YoungsModulus" type="MaterialProperty" minOccurs="0" />
      <xsd:element name="PoissonsRatio" type="MaterialProperty" minOccurs="0" />
    </xsd:all>
    <xsd:attribute name="Name" type="xsd:string" />
  </xsd:complexType>
```

在上述的 XML Schema 定義中，`Material` 是一個複合類型（complexType），它設計來表示物質的各種物理和機械性質。這個結構通過多個元素和一個屬性來詳細描述材料的特性。以下是這個 `Material` 複合類型所包含的元素和屬性的詳細說明：

1. **Permittivity** ：材料的介電常數，反映材料對電場的反應能力。 
2. **Permeability** ：材料的磁導率，表示材料對磁場的透過能力。 
3. **Conductivity** ：材料的導電性，影響材料導電的能力。 
4. **DielectricLossTangent** ：介電損耗正切，描述材料在交變電場中能量損失的一個參數。 
5. **MagneticLossTangent** ：磁損耗正切，用於描述材料在磁場中的能量損失。 
6. **ThermalConductivity** ：熱導率，表示材料傳導熱能的能力。 
7. **SpecificHeat** ：比熱容，材料單位質量的熱容量。 
8. **ThermalExpansionCoefficient** ：熱膨脹係數，反映材料在溫度變化時體積或長度變化的程度。 
9. **MassDensity** ：質量密度，材料單位體積的質量。 
10. **YoungsModulus** ：楊氏模量，材料抵抗形變的剛性指標。 
11. **PoissonsRatio** ：泊松比，描述材料在受力時橫向收縮與縱向伸長的比率。

### Material Property
以上所有材料都支援Material Property數據型別，但是Material Property又是如何定義？回到 `Stackup.xsd` 文件中，我們可以找到`MaterialProperty` 的複合類型定義，這種格式允許三種不同類型的數據表示。這使得材料特性可以非常靈活地表述，以適應不同的工程需求和模擬條件。具體包括： 
1. **Double** ：使用 `xsd:double` 類型，允許為材料特性指定一個單一的浮點數值。 
2. **Equation** ：透過 `FreqEquation` 類型，可以為特性提供一個頻率相關的方程式，以描述其變化。 
3. **Table** ：利用 `FreqTbl` 類型，允許提供一個表格來描述材料特性隨頻率的變化情況。

```xml
  <xsd:complexType name="MaterialProperty">
    <xsd:sequence>
    <xsd:choice>
      <xsd:element name="Double" type="xsd:double" />
      <xsd:element name="Equation" type="FreqEquation" />
      <xsd:element name="Table" type="FreqTbl" />
    </xsd:choice>
      <xsd:choice minOccurs="0" maxOccurs="1">
        <xsd:element name="QuadraticThermalModifier" type ="QuadraticThermalModifier"/>
      </xsd:choice>
    </xsd:sequence>
  </xsd:complexType>
```

因為 AEDT 複雜度，官方幫助文件或教材中無法詳細介紹完整的 XML 標籤及資料型別，但透過直接查閱相關的 XML Schema 定義，使用者可以清晰地瞭解 AEDT XML支援的完整範圍。這些 Schema 提供了豐富的細節，對於高階使用者來說是極為有用的，因為它們能夠根據這些信息更精確地設定和使用模擬軟件。


### XSD Tree View：強大的XSD分析工具
[XSD Tree View](https://myxml.in/xsd-treeview.html) 是一個非常有用的工具，特別是對於需要處理和瞭解 AEDT XML 結構的開發人員來說。它允許使用者輸入 XSD 檔案的內容，然後自動產生一個示例 XML 檔案。這個生成的 XML 檔案將包含 XSD 中定義的所有元素（標籤）和屬性，並以樹狀結構呈現，使得整個 XML 的結構層次一目了然。下面是根據 `Stack.xsd` 輸出的XML當中的一部分。可以完整看到每個標籤所支援的屬性：

```xml
  <ELayers LengthUnit="mm" MetalLayerSnappingTolerance="string">
    <!--Optional:-->
    <Dielectrics BaseElevation="0">
      <!--1 or more repetitions:-->
      <Layer Name="string" TargetLayer="string" Color="token" Material="string" ConvertPolygonToCircle="true" ConvertPolygonToCircleRatio="1.051732E7" ReconstructArcs="true" ArcTolerance="string" UnionPrimitives="false" DefeatureMinTraceWidth="string" Thickness="1.051732E7"/>
    </Dielectrics>
    <Layers>
      <!--1 or more repetitions:-->
      <Layer Name="string" TargetLayer="string" Color="token" Material="string" ConvertPolygonToCircle="true" ConvertPolygonToCircleRatio="1.051732E7" ReconstructArcs="true" ArcTolerance="string" UnionPrimitives="true" DefeatureMinTraceWidth="string" Negative="true" SolveInside="false" EtchFactor="1.051732E7" StartLayer="string" StopLayer="string" IsDrillLayer="false" Thickness="1.051732E7" Type="conductor" Elevation="1.051732E7" GDSDataType="string" GDSIIVia="false">
        <!--Optional:-->
        <DCThickness Thickness="string" Type="string"/>
        <!--You have a CHOICE of the next 3 items at this level-->
        <GroissSurfaceRoughness Roughness="string"/>
        <GroisseSurfaceRoughness Roughness="string"/>
        <HuraySurfaceRoughness NoduleRadius="string" HallHuraySurfaceRatio="1.051732E7"/>
        <!--You have a CHOICE of the next 3 items at this level-->
        <GroissBottomSurfaceRoughness Roughness="string"/>
        <GroisseBottomSurfaceRoughness Roughness="string"/>
        <HurayBottomSurfaceRoughness NoduleRadius="string" HallHuraySurfaceRatio="1.051732E7"/>
        <!--You have a CHOICE of the next 3 items at this level-->
        <GroissSideSurfaceRoughness Roughness="string"/>
        <GroisseSideSurfaceRoughness Roughness="string"/>
        <HuraySideSurfaceRoughness NoduleRadius="string" HallHuraySurfaceRatio="1.051732E7"/>
      </Layer>
    </Layers>
    <!--Optional:-->
    <Vias>
      <!--1 or more repetitions:-->
      <Layer Name="string" TargetLayer="string" Color="token" Material="string" ConvertPolygonToCircle="false" ConvertPolygonToCircleRatio="1.051732E7" ReconstructArcs="false" ArcTolerance="string" UnionPrimitives="false" DefeatureMinTraceWidth="string" GDSDataType="string" StartLayer="string" StopLayer="string" SolveInside="true">
        <!--Optional:-->
        <DCThickness Thickness="string" Type="string"/>
        <!--Optional:-->
        <CreateViaGroups Method="proximity" Persistent="false" Tolerance="string" CheckContainment="true"/>
        <!--Optional:-->
        <SnapViaGroups Method="areaFactor" Tolerance="string" RemoveUnconnected="false"/>
        <!--Zero or more repetitions:-->
        <TSVProperties Thickness="string" Material="string"/>
      </Layer>
    </Vias>
  </ELayers>
```