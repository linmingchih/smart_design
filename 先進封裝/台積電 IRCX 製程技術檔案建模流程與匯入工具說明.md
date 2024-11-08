台積電 IRCX 製程技術檔案建模流程與匯入工具說明
---
### IRCX 檔案格式概述

台積電的製程技術檔案通常提供的是 .ircx 格式，該格式有加密與未加密兩種版本。若您的 IRCX 為未加密格式，可直接在匯入 GDS 時瀏覽 .ircx 檔案，便能將製程參數（例如層厚度與 layer mapping）與 GDS 檔案一起匯入至 3DL。

您也可以參考 [GDSImportWizard](https://github.com/YongshengGuo/GDSImportWizard?tab=readme-ov-file) 工具，它包含詳細的文件說明，透過該工具的圖形化介面（GUI）可以更方便地匯入未加密的 IRCX 和 GDS 檔案。該工具支援自動建立元件或過孔（via）分組，有助於加速流程。此外，3DL 與 GDSWizard 皆支援 Synopsys 的 .itf 製程參數檔案，但不支援 Cadence 的 .ict 製程參數檔案。

### 加密格式 IRCX 的匯入流程
若您的 IRCX 檔案為加密格式，GDSWizard 將無法支援，僅能透過 3DL 匯入 GDS 時手動瀏覽加密的 .ircx 檔案。此外，您需要layer map 檔案與filter 檔案的協助：

Layer map 檔案：由於加密 IRCX 檔案的製程參數內部層與外部 GDS 層之間的對應關係被加密，需透過 layer map 來明確定義各層對應。
Filter 檔案：即使使用 layer map 進行映射，IRCX 檔案中仍可能包含多餘圖層，這些層可能無需導入，因此使用 filter 檔案可篩選並保留所需的圖層。
由於加密格式的操作流程較為複雜，建議參閱附上的 PDF 文件，以深入了解整體步驟。