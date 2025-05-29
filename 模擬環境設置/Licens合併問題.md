如何正確合併 ANSYS License 檔案：避免 SUPERSEDE 與 ISSUED 日期造成的陷阱
---

在近期的工作中，我嘗試將兩份 ANSYS 的 FlexNet License 檔案（以下簡稱 A 與 B）同時加入 ANSYS License Manager 中，卻發現僅有其中一份檔案的功能被正確識別。即使我將兩份 license 手動合併成單一檔案，問題依舊存在 —— License Manager 僅認得其中一組 license，另一組則完全被忽略。


### 初步假設：VENDOR\_STRING 不一致？
在本案例中，兩份 license 分別由公司內不同部門獨立採購，對應不同的 customer 編號（VENDOR_STRING）。第一時間，我以為問題出在 `VENDOR_STRING` 欄位的差異。例如：

* License A 使用 `customer:00602995`
* License B 使用 `customer:01115160`

我懷疑不同客戶編號可能造成合併失效。然而，事後證明這並非主要原因，因為 ANSYS 的 License Manager 本身支援多客戶號合併，只要格式正確並不會導致無效。


### 真正關鍵：ISSUED 日期與 SUPERSEDE 行為

透過進一步比對與詢問 ANSYS License 管理人員，我發現問題其實出在每條 License Increment 的 **`ISSUED` 日期不一致**：

* 有些 Increment 標示為 `ISSUED=08-may-2025`
* 其他 Increment 則為 `ISSUED=26-may-2025`

這種情況下，若兩份檔案中含有同一功能（例如 `anshpc_pack`），FlexNet 的 **`SUPERSEDE` 機制** 會將日期較早的 Increment 視為已被取代，因此忽略掉它，即使其數量原本應可累加。

#### 什麼是 SUPERSEDE？（中文意思為「取代」）

以下是一段在 license 檔案中實際出現的例子，位於我們嘗試合併的其中一個檔案中：

```
INCREMENT anshpc_pack ansyslmd 2026.0508 permanent 1 \
	VENDOR_STRING=customer:00602995 SUPERSEDE ISSUER=SIEBEL \
	ISSUED=08-may-2025 START=09-may-2025 AUTH={ ansyslmd=( \
	LK=0E1FCA763F6A SIGN="0020 559A 3312 57AD 4AEB F61B EDA0 F500 \
	39DA 9B4C 271B 5582 C5D4 2287 9C73" SIGN2="00FC 2E9F FF81 008D \
	7DBB 0511 8BDF 9D00 E7A8 88F8 5893 06AE 013C ABB7 A06A") \
	ansoftd=( SIGN="0022 D6A2 8505 0FDE 7D39 6BFD 1217 F100 F1C2 \
	8739 047C 89A5 8396 09B9 11B6" SIGN2="0062 4690 E663 F26B C625 \
	1446 BA1B EA00 6569 D61B 5289 0127 6715 311A 7AA9") }
```

`SUPERSEDE` 是 FlexNet license 檔案中的一個關鍵指令，用來判定「相同功能代號的 license increment 應以哪一筆為準」。當系統發現有重複的 feature name（例如 `anshpc_pack`）時，會以 **`ISSUED` 日期較晚者為準**，並忽略掉所有 `ISSUED` 較舊的相同功能。

因此，若在合併檔案時，功能重複但 `ISSUED` 不一致，就會發生數量無法累加的情況，導致看似有效的 license 被完全忽略。


### 解決方案：統一 ISSUED 日期重新發行

最終，我們請 ANSYS 的 license 管理人員協助處理。他們的建議如下：

> 若要將兩份 license 合併為一，請務必確認：
>
> * 所有 license increment 的 `ISSUED` 日期完全一致
> * 這樣 FlexNet 才能將相同功能的 increment 進行數量累加，而不會互相覆蓋

我們請他們 **在相同的日期（例如 28-May-2025）重新發行 License A 與 B**，合併後果然成功，License Manager 也能正確識別所有功能與數量。


### 小結

當你在合併 ANSYS license 檔案時，若遇到某些功能無法被識別，除了檢查 `VENDOR_STRING` 與語法格式外，請務必注意 **`ISSUED` 日期是否一致**。這個看似不起眼的欄位，實際上控制了 FlexNet 的 `SUPERSEDE` 機制，往往是 license 合併失敗的根本原因。


