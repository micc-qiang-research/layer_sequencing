import scipy.stats as stats
import numpy as np
import math
import pandas as pd

MB = 10**6
GB = 10**9

result_path = "./__result__/"

# 设置全局可复现
np.random.seed(0)

def zipf_distribution(a, n, size):
    zipf = stats.zipfian(a, n) 
    values = np.array(zipf.rvs(size=size), dtype=int) - 1
    return values

def uniform_distribution(n, size):
    uniform = stats.uniform()
    values = np.array(np.floor(uniform.rvs(size=size)*n), dtype=int)
    return values

# 随机选择[0,k) 之间的一个数
def randInt(K):
    return int(np.random.rand(1)[0]*K)

def np_to_csv(data, path):
    pd.DataFrame(data).to_csv(path, index=None, header=None)
