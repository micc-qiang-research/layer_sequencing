from schedulers.LASA import LASA
from schedulers.RS import RS
from cluster import Cluster
from analysis import Analysis
import draw

def exp_one(data, algo="LASA"):
    # 准备环境
    requests = data.new_requests()
    cluster = Cluster()

    # 调度
    if algo == "LASA":
        scheduler = LASA(data, cluster)
    else:
        scheduler = RS(data, cluster)
    deployment = scheduler.schedule(requests)

    # 分析结果
    analysis = Analysis(data, cluster,requests, deployment)
    # analysis.show()

    return analysis.get_startup_latency()
    # draw.prepare_draw_cdf([1,2,3,4,5,6,7,8,9,10], [11,2,1,5,3,9,8,7,6,4])
    # draw.draw_cdf("lat_cdf.csv")

def exp(data):
    latency = {}

    algo = ["LASA", "RS"]
    for i in algo:
        latency[i] = exp_one(data, i)
    draw.prepare_draw_cdf(latency["LASA"], latency["RS"])
    draw.draw_cdf()


