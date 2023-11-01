from cluster import Server

# 先不实现序列拉取
class Analysis:
    def __init__(self, data, cluster, requests, deploy):
        self.cluster = cluster
        self.requests = requests
        self.deploy = deploy

        self.servers = [Server(data, cluster.bandwidth, cluster.container_capacity, cluster.storage_capacity) for k in range(cluster.server_numbers)]

        self.tick = [0 for k in range(cluster.server_numbers)]
        self.startup_latency = [] # 每个请求的启动延迟
        self.total_startup_latency = 0
        self.simulator()

    def simulator(self):
        for i, k in enumerate(self.deploy):
            image = self.requests[i]
            self.tick[k] += self.servers[k].deploy_container(image)
            self.startup_latency.append(self.tick[k])

    def get_startup_latency(self):
        return self.startup_latency

    def get_total_startup_latency(self):
        return sum(self.startup_latency)

    
    def show(self):
        print("total_startup_latency: ", self.get_total_startup_latency())
        print("startup_latency: ", self.get_startup_latency())


