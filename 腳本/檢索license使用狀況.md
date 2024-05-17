檢索license使用狀況
---
以下是Ansys License Manager的界面，其中“View FlexNet Debug Log”選項是用來查看FlexNet發布的除錯日誌。包含了關於license服務器操作的詳細技術信息，像是使用者對於軟件license的使用和歸還的詳細記錄。這些記錄包括每個用戶的開始和結束時間，這對於追蹤和優化license的使用非常有幫助。

如果想要進行更進一步的統計分析，您可以將這些日志文件導出，然後使用Python來進一步的分析。這樣可以幫助您更好地管理license的分配，並且確定是否需要購買更多的license或者重新分配現有的license以達到更高效的使用。

Ansys License Manager允許用戶直接從界面中導出日志文件，通過點擊界面右上角的“SAVE TO FILE”按鈕即可進行保存。保存後的文件通常是文本格式，可以用任何文本編輯器打開，也可以用程式語言如Python來讀取和處理這些數據，從而進行更深入的分析。

![2024-05-17_08-00-09](/assets/2024-05-17_08-00-09_acmv2dzzm.png)


下面這段程式碼分為兩部分。第一部分用於讀取和解析日誌文件中的license使用記錄。第二部分則是主要用來追蹤license的借出和歸還時間，並將這些信息保存至CSV文件中以供進一步分析。

```python
import re
from datetime import datetime, timedelta

with open(r"D:\demo\license.log") as f:
    text = f.readlines()

date = None
previous_time_stamp = None
information = []
for line in text:
    if 'TIMESTAMP' in line:
        date = line.strip().split()[-1]
        continue
    
    try:
        time_string = line.split()[0]
        time_stamp = datetime.strptime(time_string, '%H:%M:%S').time()
    except:
        continue
    
    if date and previous_time_stamp and time_stamp < previous_time_stamp:
        date_from_string = datetime.strptime(date, '%m/%d/%Y').date()
        date = (date_from_string + timedelta(days=1)).strftime('%m/%d/%Y')
        print(date)

    previous_time_stamp = time_stamp   
    
    
    if date:
        m = re.search('(\d+:\d+:\d+).*(IN|OUT): "(.*)" (\S*)', line)
        if m:
            time = m.group(1)
            status = m.group(2)
            increment = m.group(3)
            user = m.group(4)
            
            time_object = datetime.strptime('{} {}'.format(date, time), '%m/%d/%Y %H:%M:%S')
            information.append((time_object, status, increment, user))

#%%
result = []
queue = []
for info in information:
    time_object, status, increment, user = info
    
    if status == 'OUT':
        queue.append((time_object, status, increment, user))
    
    if status == 'IN':
        for n, (time_object0, _, increment0, user0) in enumerate(queue):
            if increment == increment0 and user == user0:
                out = queue.pop(n)
                result.append((out, info))
                break
        print(info)
        
result.sort()
with open('d:/demo/statistics.csv', 'w') as f:
    for item in result:
        t0, _, increment, user = item[0]
        t1, _, increment, user = item[1]
        line = ', '.join([str(t0), user, increment, str(t1-t0).replace(', ', '_').replace(' ','')])
        f.write(line + '\n')
    
```
![2024-05-17_08-06-13](/assets/2024-05-17_08-06-13.png)