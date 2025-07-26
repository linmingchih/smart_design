AI 助攻，AEDT 後處理分析一分鐘搞定
---

一位訊號完整性工程師 Alex，正埋首於一項棘手的任務：使用 PyAEDT 分析一個複雜的電路板上電源完整性（PI）專案。他完成模擬設定並成功在AEDT當中顯示出阻抗曲線，接下來希望能透過 PyAEDT 腳本，快速將數據與目標規格比較，並自動標示出「通過/失敗」（Pass/Fail）的區間。

然而，他很快就遇到了瓶頸。PyAEDT 雖然功能強大，但在客製化的圖表繪製，特別是自動判定並標示出失敗區間的功能上，似乎有所欠缺。他花了好幾個小時，查閱了各種資料，卻始終找不到一個滿意的解決方案。

「這實在太花時間了，」Alex 挫折地對自己說，「一定有更聰明的方法。」

抱著一線希望，他預約了與 Ansys 資深應用工程師 Lin 的線上會議。

### 瓶頸與轉機 

「Lin，我快被這個後處理搞瘋了。」視訊一接通，Alex 就迫不及待地吐露了他的困境。「我需要一個 PyAEDT 腳本來自動分析這個阻抗圖，但要做到 Pass/Fail 的判定，還要能自動框出 Fail 的頻段，實在是太複雜了。」

Lin 點點頭，他完全理解 Alex 的處境。「Alex，你遇到的問題很常見。PyAEDT 的核心在於驅動模擬流程，但數對於這種高度客製化的後處理視覺化，確實缺少足夠的函數支持。」

看著 Alex 失望的表情，Lin 話鋒一轉，笑著說：「不過，你今天找對人了。與其花大把時間去一行一行地寫程式，不如我們試試一個更『智慧』的幫手？」

### AI 的驚奇展示

Alex 半信半疑地看著 Lin。只見 Lin 請他分享手邊的兩個檔案 Target.txt 以及那份讓他頭痛的 CSV 數據。

「現在，看好了。」Lin 分享了自己的螢幕，打開一個ChatGPT對話視窗。「這是我最近在使用的 AI 助理。我只要把你的需求，連同你剛剛給我的檔案，一起『餵』給它就行了。」

Lin 熟練地將兩個檔案上傳，然後在對話框中輸入了一段清晰的指令：

「請參考我提供的 CSV 檔案，幫我生成一個新的 Python 腳本，用來完成電源分配網路（PDN）的阻抗分析。這個腳本需要：

1.  讀取 `impedance_profile.csv` 裡的量測數據。
2.  讀取一個名為 `Target.txt` 的規格限制檔案。
3.  在同一張圖上，用對數座標（log-log scale）畫出量測曲線和規格限制線。
4.  自動標示出量測值超過規格的「失敗」區間。
5.  在圖表上標註出量測曲線的最大值和最小值。
6.  明確標示出失敗區間的頻率範圍。
7.  最後將這張分析圖儲存成一個圖片檔案。」

Alex 屏氣凝神地看著螢幕。在他看來，這是一個需要至少半天時間才能完成的複雜任務。

然而，奇蹟發生了。

不到一分鐘，AI 的回應框中，一段完整、註解清晰的 Python 程式碼赫然出現。


### 成果與啟示

Lin 沒有多做解釋，直接複製了那段程式碼，並在本機端執行。瞬間，一張專業、資訊完整的分析圖表就呈現在兩人眼前。

![pdn_check_result_annotated](/assets/pdn_check_result_annotated.png)

圖表上，藍色的量測曲線與紅色的規格限制線一目了然。更重要的是，量測值超標的區段被醒目的橘色區塊清楚標示，圖表的圖例中甚至自動計算並顯示了失敗的頻率範圍。曲線的最高點與最低點，也都被準確地標示了出來。

「我的天…」Alex 驚訝得說不出話來，「這…這太不可思議了！我花了快一整天的時間，你和 AI 不到一分鐘就解決了！」

Lin 笑著說：「這就是 AI 在工程領域的潛力。它不是要取代我們，而是要成為我們最強大的助手。像這種重複性高、規則明確的後處理工作，正是 AI 最擅長的領域。它能將我們從繁瑣的程式碼中解放出來，讓我們能更專注在真正核心的工程挑戰上——像是分析『為什麼』會失敗，以及『如何』解決它。」

這次的震撼教育，為 Alex 打開了一扇通往新世界的大門。他意識到，善用 AI 的能力，將能極大地提升工作效率。從今天起，他的工作流程中，多了一個不可或缺的智慧夥伴。

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

def plot_pdn_check(
    csv_file: str,
    limit_file: str,
    output_image: str = "pdn_check_result_annotated.png"
):
    # === 1. 讀取資料 ===
    curve_df = pd.read_csv(csv_file)
    limit_df = pd.read_csv(limit_file, sep="\t")
    limit_df.columns = ['Frequency_MHz', 'Target_mOhm']

    freq_col = curve_df.columns[0]
    z_col = curve_df.columns[1]

    # === 2. log-log 內插限制線 ===
    log_interp_func = interp1d(
        np.log10(limit_df['Frequency_MHz']),
        np.log10(limit_df['Target_mOhm']),
        bounds_error=False,
        fill_value="extrapolate"
    )
    curve_df['Limit_mOhm'] = 10 ** log_interp_func(np.log10(curve_df[freq_col]))

    # === 3. 判斷 Pass/Fail ===
    curve_df['Pass'] = curve_df[z_col] <= curve_df['Limit_mOhm']

    # === 4. 繪圖 ===
    x = curve_df[freq_col].values
    y_meas = curve_df[z_col].values
    y_limit = curve_df['Limit_mOhm'].values
    fail_mask = ~curve_df["Pass"].values

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(x, y_meas, label='Measured', color='blue', linewidth=2)
    ax.plot(x, y_limit, label='Limit Line', color='red', linestyle='--', linewidth=2)
    ax.fill_between(x, y_meas, y_limit,
                    where=fail_mask, interpolate=True,
                    color='orange', alpha=0.4, label='Fail Region')

    # === 5. 標註最大/最小值 ===
    max_idx = np.argmax(y_meas)
    min_idx = np.argmin(y_meas)
    ax.plot(x[max_idx], y_meas[max_idx], 'ro')
    ax.text(x[max_idx], y_meas[max_idx]*1.1, f"Max: {y_meas[max_idx]:.2f} mΩ",
            fontsize=10, color='red')
    ax.plot(x[min_idx], y_meas[min_idx], 'go')
    ax.text(x[min_idx], y_meas[min_idx]*0.9, f"Min: {y_meas[min_idx]:.2f} mΩ",
            fontsize=10, color='green')

    # === 6. 標註 Fail 區段範圍 ===
    fail_freqs = x[fail_mask]
    if len(fail_freqs) > 0:
        fail_start = fail_freqs.min()
        fail_end = fail_freqs.max()
        ax.axvspan(fail_start, fail_end, color='gray', alpha=0.2,
                   label=f"Fail Band: {fail_start:.2f}–{fail_end:.2f} MHz")

    # === 7. 圖表美化 ===
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel("Frequency (MHz)", fontsize=12)
    ax.set_ylabel("Impedance (mOhm)", fontsize=12)
    ax.set_title("PDN Impedance Check with Annotation", fontsize=14)
    ax.grid(True, which="both", ls="--", linewidth=0.5)
    ax.legend()
    plt.tight_layout()

    # === 8. 儲存 ===
    plt.savefig(output_image, dpi=300)
    plt.close()
    return output_image

# === 範例使用 ===
plot_pdn_check(
    csv_file="impedance_profile.csv",
    limit_file="Target.txt",
    output_image="pdn_check_result_annotated.png"
)
```