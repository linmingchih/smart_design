CUDA性能與CPU計算性能比較
---
### 測試平台
Dell 7680, Windows 11，搭配：
- 13th Gen Intel(R) Core(TM) i7-13850HX   2.10 GHz

- NVIDIA RTX 5000 Ada Generation Laptop GPU，配備了12,800個CUDA核心


### 測試代碼
做1024x1024矩陣相乘，用CPU以最簡單的迴圈對矩陣元素逐一計算需約400秒，用Numba Jit約2.8秒，用GPU CUDA計算僅需0.21秒。

```python
import os

os.environ['CUDA_HOME'] = r'C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.4'

from numba import cuda
import numpy as np
import time

@cuda.jit
def matrix_multiply_gpu(A, B, C):

    sA = cuda.shared.array(shape=(32, 32), dtype=np.float32)
    sB = cuda.shared.array(shape=(32, 32), dtype=np.float32)
    
    x, y = cuda.grid(2)
    tx, ty = cuda.threadIdx.x, cuda.threadIdx.y
    bw, bh = cuda.blockDim.x, cuda.blockDim.y

    if x >= C.shape[0] or y >= C.shape[1]:
        return
    
    tmp = 0.0
    for i in range(int(A.shape[1] / bw)):
        sA[ty, tx] = A[x, ty + i * bw]
        sB[ty, tx] = B[tx + i * bh, y]
        cuda.syncthreads()

        for j in range(bw):
            tmp += sA[ty, j] * sB[j, tx]
        cuda.syncthreads()

    C[x, y] = tmp


def host_matrix_multiply_gpu(A, B):
    A_global_mem = cuda.to_device(A)
    B_global_mem = cuda.to_device(B)
    C_global_mem = cuda.device_array((A.shape[0], B.shape[1]), dtype=np.float32)
    threadsperblock = (16, 16)
    blockspergrid_x = int(np.ceil(A.shape[0] / threadsperblock[0]))
    blockspergrid_y = int(np.ceil(B.shape[1] / threadsperblock[1]))
    blockspergrid = (blockspergrid_x, blockspergrid_y)
    matrix_multiply_gpu[blockspergrid, threadsperblock](A_global_mem, B_global_mem, C_global_mem)
    return C_global_mem.copy_to_host()


#%%
from numba import jit
import numpy as np
import time

@jit(nopython=True)
def matrix_multiply_cpu(A, B):
    M, K = A.shape
    K, N = B.shape
    C = np.zeros((M, N), dtype=np.float32)
    for i in range(M):
        for j in range(N):
            sum = 0
            for k in range(K):
                sum += A[i, k] * B[k, j]
            C[i, j] = sum
    return C

# 初始化數據
A = np.random.rand(1024, 1024).astype(np.float32)
B = np.random.rand(1024, 1024).astype(np.float32)

# GPU 計算
start_time_gpu = time.time()
C_gpu = host_matrix_multiply_gpu(A, B)
gpu_time = time.time() - start_time_gpu

# CPU 計算
start_time_cpu = time.time()
C_cpu = matrix_multiply_cpu(A, B)
cpu_time = time.time() - start_time_cpu

print("GPU version took {:.5f} seconds.".format(gpu_time))
print("CPU version took {:.5f} seconds.".format(cpu_time))
```

![2024-05-11_22-08-22](/assets/2024-05-11_22-08-22.png)