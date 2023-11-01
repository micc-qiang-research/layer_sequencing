## 数据集
- 155 most popular images
- total size of images: 60GB
- 810 unique layers in tital
- total size of unique layers: 30GB (有共享的可能)


## 实验参数
- bandwidth: 10Mbps
- edge nodes: 15
- running container number: 50
- storage capacity: 20GB
- total number of containers: 200
- $\alpha$ : 0.5


## 实验
1. 从数据集中随机（zipf, uniform）选取n个镜像作为容器的镜像
2. 执行调度算法（LASA）
3. 获取运行指标（total startup time，CDF等）