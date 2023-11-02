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


def prepare_draw_cdf_s(data):
    assert len(data) >= 2, "unmatched data length"
    ds = []
    prob = []
    inc = 100. / len(data[0])
    k = inc
    for i in range(len(data[0])):
        prob.append(k)
        k += inc
    ds.append(prob)
    for i in data:
        ds.append(sorted(i))
    ds = np.array(ds).T
    np_to_csv(ds, result_path + "lat_cdf.csv")


def draw_cdf(n, label, filename = "lat_cdf.csv"):
    #读取CSV文件
    data = pd.read_csv(result_path + filename)

    prob = data.iloc[:,0]
    for i in range(n):
        delays = data.iloc[:,i+1]
        plt.plot(delays, prob, label=label[i])

    #设置图表属性
    plt.xlabel('Latency')
    plt.ylabel('CDF') 
    # plt.xlim(0,80000)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    draw_cdf(2, ["RS", "RS+UPL"], "lat_cdf.csv")
