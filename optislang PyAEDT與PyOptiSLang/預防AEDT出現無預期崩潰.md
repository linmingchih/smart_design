預防AEDT出現無預期崩潰
---

```python
import subprocess
import psutil

from pyvariant import list_2_variant_xy_data

if 'OSL_REGULAR_EXECUTION' not in locals(): 
    OSL_REGULAR_EXECUTION = False


if not OSL_REGULAR_EXECUTION:
    w = 1.0
    a = 1.0

process = subprocess.Popen(
    [r'C:\Users\mlin\.ansys_python_venvs\2024_8_14\Scripts\python.exe', 'd:/demo7/test.py', str(a), str(w)],
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

try:
    stdout, stderr = process.communicate(timeout=5)
    if process.returncode == 0:
        print("Success:", stdout)
        try:
            x, y = eval(stdout)
            variant_y = list_2_variant_xy_data(y, x)
        except Exception as e:
            print(f"Error parsing output: {e}")
    else:
        print(f"Error running script: {stderr}")

except subprocess.TimeoutExpired:
    print("Process timed out")
    process.terminate()

    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == "ansysedt.exe":
            proc.kill()
            print(f"Terminated {proc.info['name']} with PID {proc.info['pid']}")
```


```python
from pyaedt import Hfss
import sys
import random
import time

time.sleep(random.randint(1,3))


from math import sin

a = float(sys.argv[1])
w = float(sys.argv[2])
 
x = [0.01*i for i in range(1000)]
y = [a*sin(w*i) for i in x]

print((x, y))

```