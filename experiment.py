from schedulers.LASA import LASA
from schedulers.RS import RS
from cluster import Cluster
from analysis import Analysis
import draw

def exp_one(data, requests, place_algo, seq_algo):
    # 准备环境
    # requests = data.new_requests()
    cluster = Cluster()

    # 调度
    if place_algo == "LASA":
        scheduler = LASA(data, cluster)
    else:
        scheduler = RS(data, cluster)
    deployment = scheduler.schedule(requests)

    # 分析结果
    analysis = Analysis(data, cluster,requests, deployment, seq=seq_algo)
    # analysis.show()

    return analysis.get_startup_latency()
    # draw.prepare_draw_cdf([1,2,3,4,5,6,7,8,9,10], [11,2,1,5,3,9,8,7,6,4])
    # draw.draw_cdf("lat_cdf.csv")

def exp(data):
    requests = data.new_requests()
    latency = {}
    latency_data = []
    latency_name = []

    place_algo = ["LASA", "RS"]
    seq_algo = ["GLSA", "FCFS"]
    for place in place_algo:
        for seq in seq_algo:
            name = place+"-"+seq
            lat = exp_one(data, requests, place, seq)
            latency[name] = lat
            latency_data.append(lat)
            latency_name.append(name)
    
    draw.prepare_draw_cdf_s(latency_data)
    draw.draw_cdf(len(place_algo)*len(seq_algo), latency_name, "lat_cdf.csv")


