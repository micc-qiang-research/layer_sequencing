import pandas as pd
import matplotlib.pyplot as plt
from utils import result_path, np_to_csv
import numpy as np


def prepare_draw_cdf(data1, data2):
    assert len(data1) == len(data2), "unmatched data length"
    data1 = sorted(data1)
    data2 = sorted(data2)
    prob = []
    inc = 100. / len(data1)
    k = inc
    for i in range(len(data1)):
        prob.append(k)
        k += inc
    data = np.array([prob, data1, data2]).T
    np_to_csv(data, result_path + "lat_cdf.csv")

def draw_cdf(filename = "lat_cdf.csv"):
    #读取CSV文件
    data = pd.read_csv(result_path + filename)

    #提取延迟列
    delays = data.iloc[:,0]
    dep_delays = data.iloc[:,1]
    kube_delays = data.iloc[:,2]


    #绘制CDF曲线
    plt.plot(dep_delays, delays, label='LASA')
    plt.plot(kube_delays, delays, label='RS')

    #设置图表属性
    plt.xlabel('Latency')
    plt.ylabel('CDF') 
    # plt.xlim(0,80000)
    plt.legend()


    plt.show()

if __name__ == "__main__":
    draw_cdf("lat_cdf.csv")
