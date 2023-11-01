import pymongo
import numpy as np
from utils import *
import pickle

class ImageDB:

    address = "mongodb://10.249.42.78:27017/"
    db_name = "image_db"
    collection_images = "ecr_images"
    collection_layers = "ecr_layers"
    images_number = 155
    n = 50 # 一次性生成多少请求

    # 加快读取速度
    data = "./storage/"
    data_images = data + "images.npy"
    data_layers = data + "layers.pkl"
    
    def __init__(self):
        try:
            self.images = np.load(ImageDB.data_images, allow_pickle=True)
            self.layers = pickle.load(open(ImageDB.data_layers, "rb"))
            print("loading data from local...")
        except: 
            print("loading data from mongodb...")
            client = pymongo.MongoClient(ImageDB.address)
            db = client[ImageDB.db_name]
            col_images = db[ImageDB.collection_images]
            col_layers = db[ImageDB.collection_layers]
            self.images = np.array(list(col_images.find().sort([("popularity", -1)]).limit(ImageDB.images_number)))
            self.layers = {}
            for image in self.images:
                for layer in image["layers"]:
                    self.layers[layer] = col_layers.find_one({"digest": layer})
            np.save(ImageDB.data_images, self.images)
            pickle.dump(self.layers, open(ImageDB.data_layers, "wb"))

    # 生成新的请求/一堆容器
    def new_requests(self, zipf=True):
        if zipf:
            idx = zipf_distribution(1.1, ImageDB.images_number, ImageDB.n)
        else:
            idx = uniform_distribution(ImageDB.images_number, ImageDB.n)

        return self.images[idx]

    # 获取某个image对应的所有layer
    def get_image_layers(self, image):
        layers = []
        for l in image["layers"]:
            layers.append(self.layers[l])
        return np.array(layers)

    def get_image_layers_digest(self, image):
        layers = self.get_image_layers(image)
        return set([l["digest"] for l in layers])

    # 获取某个image对应的layer的大小
    def get_image_layers_size(self, image):
        layers = self.get_image_layers(image)
        size = 0
        for l in layers:
            size += l["size"]
        return size

    def get_images(self):
        return self.images

    def get_layers(self):
        return self.layers

    def check(self):
        for i in self.images:
            print(i["name"])
            for l in i["layers"]:
                assert(l in self.layers.keys())


if __name__ == "__main__":
    db = ImageDB()
    db.check()