from utils import MB,GB,SidneyDecomposition

class Cluster:
    def __init__(self):
        self.server_numbers = 15  # 集群中机器数量
        self.bandwidth = 10 * MB / 8
        self.container_capacity = 50 
        self.storage_capacity = 20 * GB

class Job:
    def __init__(self, is_container_job, data):
        self.is_container_job = is_container_job
        self.data = data
    
    def is_container_job(self):
        return self.is_container_job

class Server:
    def __init__(self, data, bandwidth, container_capacity, storage_capacity):
        self.data = data
        self.bandwidth = bandwidth
        self.container_capacity = container_capacity
        self.storage_capacity = storage_capacity
        self.layers = set() # 当前该server上含有的layer的digest
        self.container_capacity_used = 0 # 已经使用的容器容量
        self.storage_capacity_used = 0 # 已经使用的存储容量

    # 此server添加image后，增加的容器容量
    def get_icrement(self, image):
        layers = self.data.get_image_layers(image)
        increment = 0
        for layer in layers:
            if layer["digest"] not in self.layers:
                increment += layer["size"]
        return increment

    # 部署容器，返回部署完成增长的时间
    def deploy_container(self, image, L_inc = None):
        if L_inc is None:
            L_inc = self.get_icrement(image)
        layers = self.data.get_image_layers_digest(image)
        self.layers.update(layers)
        self.container_capacity_used += 1
        self.storage_capacity_used += L_inc
        return L_inc / self.bandwidth

    # 检测是否能部署此容器
    def can_deploy_container(self, image, L_inc = None):
        if L_inc is None:
            L_inc = self.get_icrement(image)
        return self.container_capacity - self.container_capacity_used >= 1 and \
            self.storage_capacity - self.storage_capacity_used >= L_inc

    
    # 添加一个job
    def add_job(self, is_container, data):
        if not hasattr(self, "jobs"):
            self.jobs = []
        
        job = Job(is_container, data)
        self.jobs.append(job)
        return len(self.jobs) - 1 # 返回添加的任务的index
    
    def get_job_by_index(self, index):
        return self.jobs[index]

    def get_job_number(self):
        return len(self.jobs)

    def convert_to_pred_job_seq_problem(self, images):
        layers = {}
        W = []
        P = []
        dag = set()
        lower_bound_p = 1 / self.bandwidth
        for image in images:
            cid = self.add_job(True, image)
            W.append(1)
            P.append(0)
            for layer in self.data.get_image_layers(image):
                if layer["digest"] not in layers:
                    lid = self.add_job(False, layer)
                    W.append(0)
                    P.append(layer["size"] / self.bandwidth)
                    layers[layer["digest"]] = lid
                else:
                    lid = layers[layer["digest"]]
                dag.add((lid, cid))
        P = [lower_bound_p if p == 0 else p for p in P]
        return self.get_job_number(), dag, W, P

    def deploy_container_by_glsa(self, images):
        n, dag, W, P = self.convert_to_pred_job_seq_problem(images)
        Y = SidneyDecomposition(n, dag, W, P).run()
        print(Y)
