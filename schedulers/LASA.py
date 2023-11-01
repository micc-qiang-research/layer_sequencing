from cluster import Server

# 暂不考虑layer grouping
class LASA:
    def __init__(self, data, cluster, alpha=0.5):
        self.cluster = cluster
        self.data = data
        self.servers = []
        for k in range(cluster.server_numbers):
            self.servers.append(Server(data, cluster.bandwidth, cluster.container_capacity, cluster.storage_capacity))
        self.K = cluster.server_numbers
        self.alpha = alpha
    
    def score(self, inc, cur, bandwidth):
        return (self.alpha * cur + (1-self.alpha) * inc) / bandwidth

    # 放置算法
    # 返回 {container_object_id: server_id, ...}
    def lcaa(self, images):
        deployment = []

        for image in images:
            k_a = -1
            score_a = 2 * self.data.get_image_layers_size(image) / min([self.servers[k].bandwidth for k in range(self.K)])
            for k in range(self.K):
                L_inc = self.servers[k].get_icrement(image)
                score = self.score(L_inc, self.servers[k].container_capacity_used, self.servers[k].bandwidth)
                if score < score_a and self.servers[k].can_deploy_container(image, L_inc):
                    k_a = k
                    score_a = score

            if k_a == -1:
                assert False, "No server can hold this image!"
            # 选定server[k_a]
            self.servers[k_a].deploy_container(image, L_inc)
            deployment.append(k_a)

        return deployment
        
    def schedule(self, requests):
        place = self.lcaa(requests)
        return place
