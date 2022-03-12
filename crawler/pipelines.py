from crawler.extractors import Activity_Crawler, Review_Crawler
from crawler.transformers import KlookTransformer
from crawler.loaders import MonogoDBLoader
from crawler.logger import LoggingMixin


class KlookActivityPipeline(LoggingMixin):
    def __init__(self, country_id, size, schema_path, host, port, username=None, password=None, db=None):
        self._extractor = Activity_Crawler(country_id, size)
        self._transformer = KlookTransformer(schema_path=schema_path)
        self._loader = MonogoDBLoader(host=host, port=port, db=db, username=username, password=password)

    def execute(self):
        data = self._extractor.execute()
        self.log.info('extract data')
        transformed_data = self._transformer.execute_activity(data)
        self.log.info('transform data')
        self._loader.execute_activity('activity', transformed_data)
        self.log.info('load data')
        return [i['activity_id'] for i in transformed_data]


class KlookReviewPipeline(LoggingMixin):
    def __init__(self, activity_ids, size, schema_path, host, port, username=None, password=None, db=None):
        self._extractor = Review_Crawler(activity_ids, size)
        self._transformer = KlookTransformer(schema_path=schema_path)
        self._loader = MonogoDBLoader(host=host, port=port, db=db, username=username, password=password)

    def execute(self):
        data = self._extractor.execute()
        self.log.info('extract data')
        transformed_review_data, transformed_image_data = self._transformer.execute_review(data)
        self.log.info('transform data')
        self._loader.execute_review('review', transformed_review_data, 'image', transformed_image_data)
        self.log.info('load data')
        return True
