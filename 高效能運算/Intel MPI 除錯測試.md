Intel MPI 除錯測試
---
本文介紹如何在 Ansys 2025 R2 (v252) 環境下，使用 Intel MPI 進行除錯測試，確保多台電腦能順利進行分散式運算。

MPI（Message Passing Interface）是 Ansys 分散式運算時用來讓多台機器互相溝通的關鍵機制。如果 MPI 設定錯誤，像是路徑、授權、或網路沒通，就會導致模擬無法跨機執行。


### 測試前準備

請在每台要參與運算的電腦上做三件事：

1. 啟用 Intel MPI 環境設定

   ```bat
   "%I_MPI_ONEAPI_ROOT%\env\vars.bat"
   ```

2. 把 Ansys 的 MPI 執行檔路徑加到系統變數裡

   ```bat
   set PATH=%PATH%;C:\Program Files\ANSYS Inc\v252\AnsysEM\common\fluent_mpi\multiport\mpi\win64\intel\bin
   ```

3. 確認能夠互相以主機名稱（hostname）連線，例如 `PC01`, `PC02`, `PC03`。



### 開始測試

#### ✅ 單機測試（確認本機 MPI 正常）

```bat
mpiexec -n 2 -ppn 1 -hosts localhost "c:\Program Files\ANSYS Inc\v252\AnsysEM\schedulers\diagnostics\Utils\intelmpi_test.exe"
```

這會在同一台電腦上開出兩個 MPI 程序，看是否能互通。

#### ✅ 雙機測試（測試兩台電腦之間的通訊）

```bat
mpiexec -n 2 -ppn 1 -hosts localhost,PC02 "c:\Program Files\ANSYS Inc\v252\AnsysEM\schedulers\diagnostics\Utils\intelmpi_test.exe"
```

#### ✅ 三機測試（測試整個小叢集）

```bat
mpiexec -n 3 -ppn 1 -hosts localhost,PC02,PC03 "c:\Program Files\ANSYS Inc\v252\AnsysEM\schedulers\diagnostics\Utils\intelmpi_test.exe"
```



### 預期結果

若設定正確，你會看到類似這樣的訊息：

```
Intel MPI
Hello world! I'm rank 0 of 1 running on PC01.localdomain
Intel MPI
Hello world! I'm rank 0 of 1 running on PC02.localdomain
```

代表：

* 每台主機都有成功啟動 MPI 程序；
* 各節點能互相辨識、通訊順暢；
* 基本的 MPI 環境沒問題。



### 如果執行失敗怎麼辦？

1. 先**重開每台機器**，確保環境變數與服務重載成功。
2. 若還是不行，可以開啟 **MPI 除錯模式**，會顯示更詳細的啟動訊息：

   ```bat
   mpiexec -genv I_MPI_Debug=6 -n 2 -ppn 1 -hosts localhost "c:\Program Files\ANSYS Inc\v252\AnsysEM\schedulers\diagnostics\Utils\intelmpi_test.exe"
   ```
3. 除錯訊息會列出：

   * 使用的 MPI 版本與模式（如 shared memory 或 TCP）
   * 每個 rank 對應的主機與 CPU
   * 內部通訊初始化狀態

   這有助於判斷是哪一個節點或設定出問題。

