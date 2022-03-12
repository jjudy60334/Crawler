
import pymongo
from datetime import datetime

from crawler.Operator.MongoDB import MongoOperator

myclient = pymongo.MongoClient("mongodb://host.docker.internal:27017")
mydb = myclient["klook"]
mycol = mydb["activity_test"]
# update_activity_ids = [i['activity_id'] for i in upload_data]
# print(update_activity_ids)

# delete_result = mycol.delete_many({"activity_id": {"$in": update_activity_ids}})
# print(delete_result.deleted_count)
####validate ###


class MonogoDBLoader(MongoOperator):
    def __init__(self, host, port, username, password, db):
        self._mongo_operator = self._connect_mongo(
            host=host, port=port, username=username, password=password, db=db)
        print(host, port, username, password, db)
        super().__init__()

    def replace_many(self, collection_name, data_list, key):
        collection = self._mongo_operator.get_collection(collection_name)
        for data in data_list:
            collection.replace_one({key: data[key]}, data, True)

    def execute_activity(self, activity_name, activity_data):
        self.replace_many(activity_name, activity_data, 'activity_id')
        return [i['activity_id'] for i in activity_data]

    def execute_review(self, review_name, review_data, image_name, image_data):
        self.replace_many(review_name, review_data, 'review_id')
        self.replace_many(image_name, image_data, 'image_id')
