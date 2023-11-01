from data import ImageDB
from experiment import exp

if __name__ == "__main__":
    db = ImageDB()
    # images = db.new_requests()
    # for i in images[:1]:
    #     print(db.get_image_layers(i))
    exp(db)
