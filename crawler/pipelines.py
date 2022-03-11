from extractors import Activity_Crawler, Review_Crawler
from transformers import KlookTransformer
from loaders import MonogoDBLoader


class KlookActivityPipeline():
    def __init__(self, contry_id, size, schema_path, host, port, db, username=None, password=None):
        self._extractor = Activity_Crawler(contry_id, size)
        self._transformer = KlookTransformer(schema_path=schema_path)
        self._loader = MonogoDBLoader(host, port, db, username=None, password=None)

    def execute(self, schema):
        data = self._extractor.execute()
        transformed_data = self._tranformer.execute_activity(data)
        self._loader.execute_activity('activity', transformed_data)
        return True


class KlookReviewPipeline():
    def __init__(self, activity_ids, size, schema_path, host, port, db, username=None, password=None):
        self._extractor = Review_Crawler(activity_ids, size)
        self._transformer = KlookTransformer(schema_path=schema_path)
        self._loader = MonogoDBLoader(host, port, db, username=None, password=None)

    def execute(self, schema):
        data = self._extractor.execute()
        transformed_data = self._tranformer.execute_review(data)
        self._loader.execute_review('activity', transformed_data)
        return True
# # y = mycol.find({"activity_id": i["activity_id"]})
# from extractors import Activity_Crawler, Review_Crawler, JsonExtractor
# from transformers import KlookTransformer
# activity_ids = [
#     58082, 51850]
# a_c = Review_Crawler(activity_ids, 50)
# # a_c = Activity_Crawler(14, 50)
# data = a_c.execute()
# print(len(data))
# print(data[0])


# test = KlookTransformer('crawler/schema')
# # activity_data = test.execute_activity(data)
# review_data, image_data = test.execute_review(data)
# print(len(review_data), len(image_data))
# print(image_data[0])
# # print(len(activity_data))
# loader = MonogoDBLoader(host="host.docker.internal", port=27017, db="klook")
# # loader.execute_activity('activity', activity_data)
# loader.execute_review('review', review_data, 'image', image_data)
# # file_path = 'file_json.json'
# # extractor = JsonExtractor()
# # data = extractor.extract(file_path)
# # upload_data = data[0]['result']["activities"]
# # test = KlookTransformer('crawler/schema')

# # tag_data = test.get_tag_data(upload_data)


# print('tag_data')

# # test = KlookTransformer('crawler/schema')
# # test.get_schema('crawler/schema/activity.json')
