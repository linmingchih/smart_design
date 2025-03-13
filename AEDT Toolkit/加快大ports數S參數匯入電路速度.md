加快大ports數S參數匯入電路速度
---

優化 S 參數（Touchstone）在 ANSYS Designer 中的匯入效率。

ANSYS Designer 匯入 `.sNp` 檔案時，需進行轉換，當 ports 過多（如 50+）時，可能需數分鐘甚至十幾分鐘。**先轉換為 SPICE (`.sp`) 格式**，再由 ANSYS Designer 讀取，可大幅減少等待時間。

1. **選擇 Touchstone (`.sNp`) 檔案**，使用 `OpenFileDialog` 讓使用者選擇 S 參數檔案。
2. **解析檔案，取得 Ports 與模型類型**，用 **正則表達式** 提取 **端口名稱 (`Port[N] = Name`)** 與 **S 參數模型類型**（S、Y、Z 參數等）。
3. **產生 SPICE (`.sp`) 檔案**，**建立 SPICE 子電路模型**，直接引用 Touchstone 檔案，讓 Designer 讀取時不再解析 S 參數，加速匯入。

**提升 ANSYS Designer 處理 S 參數的速度**，適用於**多端口 (`multi-port`) Touchstone 檔案**。
**先轉換再匯入 SPICE，可節省大量時間，提高工作效率。**


#### 1. 包裹S參數為SP檔案

![2025-03-13_08-27-56](/assets/2025-03-13_08-27-56.png)

#### 2. 匯入SP檔案
![2025-03-13_08-39-30](/assets/2025-03-13_08-39-30.png)

### snp_to_sp.py
```python
import sys
import clr
clr.AddReference("System.Windows.Forms")

from System.Windows.Forms import DialogResult, OpenFileDialog
dialog = OpenFileDialog()
dialog.Filter = "ANSYS Touchstone files (*.s*p)|*.s*p"

if dialog.ShowDialog() == DialogResult.OK:
    snp_path = dialog.FileName
else:
    pass

import re, os
ports = []

spice_path = snp_path.split('.')[0] + '.sp'
basename = os.path.basename(snp_path).split('.')[0]

with open(snp_path) as f:
    for line in f:
        if not line.strip():
            continue
        m = re.search('Port\[(\d+)\] = ([\w+\.#]*)', line)
        if m:
            ports.append(m.group(2))
        elif line[0] == '#':
            model_type = line.split()[2]
        else:
            try:
                _ = [float(i) for i in line.strip().split()]
                break
            except:
                pass
            
with open(spice_path, 'w') as f:
    f.writelines('.subckt {} {}\n'.format(basename, ' '.join(ports)))
    f.writelines('.model _{} {} TSTONEFILE="{}" INTERPOLATION=LINEAR INTDATTYP=MA HIGHPASS=10 LOWPASS=10 convolution=0 enforce_passivity=0 Noisemodel=External\n'.format(basename, model_type, snp_path))
    f.writelines('S1 {} FQMODEL="_{}"\n'.format(' '.join(ports), basename))
    f.writelines('.ends')
    AddWarningMessage('SPICE file {} is saved.'.format(spice_path))
    ```