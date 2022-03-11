
from logger import LoggingMixin
from datetime import datetime
import json


class Transformer(LoggingMixin):
    def __init__(self):
        self.text = None
        self.types_mapping = {'str': str,
                              'int': int,
                              'float': float,
                              'datetime': 'datetime',
                              'bool': bool}
        self.schema = None

    def get_schema(self, file_path):
        with open(file_path, newline='') as jsonfile:
            schema = json.load(jsonfile)
        for k, v in schema.items():
            if type(v) == dict:
                for value_k, value_v in v.items():
                    schema[k][value_k] = self.types_mapping[value_v]
            else:
                schema[k] = self.types_mapping[v]
        self.schema = schema
        return self.schema

    def transform_data_slice(self, data_slice):
        trasnformed_data_slice = {}
        for k, v in self.schema.items():
            if k in data_slice:
                if type(v) != dict:
                    if v == "datetime":
                        trasnformed_data_slice[k] = datetime.strptime(data_slice[k], "%Y-%m-%d %H:%M:%S")
                    else:
                        trasnformed_data_slice[k] = v(data_slice[k])
                else:
                    if data_slice[k]:
                        trasnformed_data_slice[k] = dict()
                        for value_k, value_v in v.items():
                            trasnformed_data_slice[k][value_k] = value_v(
                                data_slice[k][value_k]) if data_slice[k] else None
                    else:
                        trasnformed_data_slice[k] = None

        return trasnformed_data_slice

    def add_update_date(self, data_slice):
        data_slice['update_dt'] = datetime.now()
        return data_slice

    def transform_data(self, data):
        transformed_data = []
        for data_slice in data:
            trasformed_data_slice = self.transform_data_slice(data_slice)
            transformed_data.append(self.add_update_date(trasformed_data_slice))
        return transformed_data

    def execute(self, schema_path, data):
        self.get_schema(schema_path)
        transformed_data = self.transform_data(data)
        return transformed_data


class KlookTransformer(Transformer):
    def __init__(self, schema_path):
        self._schema_path = schema_path
        super().__init__()

    def get_subset_document_data(self, data: list, subset_key: str, reference_key: list):
        subset_document_data = []
        for d in data:
            subset_list = d.get(subset_key)
            if subset_list:
                for subset_data in subset_list:
                    for key in reference_key:
                        subset_data[key] = d[key]
                    subset_document_data.append(subset_data)
        return subset_document_data

    def execute_activity(self, data):
        activity_schema_path = '/'.join([self._schema_path, 'activity.json'])
        # tag_schema_path = '/'.join([self._schema_path, 'tag.json'])
        activity_data = self.execute(activity_schema_path, data)
        # tag_data = self.get_subset_document_data(data, 'tags', ['activity_id'])
        # tag_data = self.execute(tag_schema_path, tag_data)
        return activity_data

    def execute_review(self, data):
        review_schema_path = '/'.join([self._schema_path, 'review.json'])
        image_schema_path = '/'.join([self._schema_path, 'image.json'])
        review_data = self.execute(review_schema_path, data)
        image_schema_data = self.get_subset_document_data(data, 'images', ['review_id'])
        image_schema_data = self.execute(image_schema_path, image_schema_data)
        return review_data, image_schema_data
