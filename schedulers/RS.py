import numpy as np
from utils import randInt
from cluster import Server

class RS:
    max_retry = 100

    def __init__(self, data, cluster):
        self.cluster = cluster
        self.data = data
        self.servers = []
        for k in range(cluster.server_numbers):
            self.servers.append(Server(data, cluster.bandwidth, cluster.container_capacity, cluster.storage_capacity))

    def schedule(self, requests):
        deployment = []
        for r in requests:
            retry = 0
            while True:
                k = randInt(10)
                if self.servers[k].can_deploy_container(r):
                    self.servers[k].deploy_container(r)
                    deployment.append(k)
                    break
                retry += 1
                assert retry <= RS.max_retry, "retry too many times!"
                    
        return deployment