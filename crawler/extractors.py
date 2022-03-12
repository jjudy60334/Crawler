
import requests
import json
from crawler.logger import LoggingMixin
from abc import ABC, abstractmethod


class JsonExtractor:
    # def __init__(self):
    def extract(self, file_path: str) -> list:
        with open(file_path) as f:
            lines = f.readlines()
        f.close()
        datas = []
        for i in lines:
            datas.append(json.loads(i))
        return datas


class Crawler(LoggingMixin, ABC):
    def crawl(self, url):
        headers = {
            "accept-language": "zh-TW",
            "accept": "application/json, text/plain, */*",
            "user-agent":
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36"}
        r = requests.get(url, headers=headers)
        result = json.loads(r.text)
        return result

    def flip_page(self, craw_fun, extract_data, get_content_count, transfer_fun):
        page = 1
        data = craw_fun(page)
        extract_data.extend(transfer_fun(data))
        while (int(get_content_count(data)) > page * self._size):
            page += 1
            data = craw_fun(page)
            extract_data.extend(transfer_fun(data))

    @abstractmethod
    def turn_result_to_extract_data(self, **kwargs):
        pass

    @abstractmethod
    def get_content_count(self, **kwargs):
        pass

    @abstractmethod
    def execute(self, **kwargs):
        pass


class Activity_Crawler(Crawler):
    def __init__(self, country_id, size):
        self._size = size
        self._country_id = country_id
        self.extract_data = []

    def crawl_content(self, page) -> dict:
        base_url = "https://www.klook.com/v1/experiencesrv/category/activity"
        url = f"{base_url}?country_ids={self._country_id}&frontend_id_list=19&size={self._size}&start={page}"
        data = self.crawl(url=url)
        return data

    def turn_result_to_extract_data(self, data):
        return data['result']['activities']

    def get_content_count(self, data) -> int:
        return data['result']['total']

    def execute(self) -> list:
        self.flip_page(self.crawl_content, self.extract_data,
                       self.get_content_count, self.turn_result_to_extract_data)
        return self.extract_data


class Review_Crawler(Crawler):
    def __init__(self, activity_ids, size):
        self._size = size
        self._activity_ids = activity_ids
        self.extract_data = []
        self._activity_id = None

    def crawl_content(self, page) -> dict:
        base_url = f"https://www.klook.com/v1/usrcsrv/activities/{self._activity_id}/images/get"
        url = f"{base_url}?page={page}&limit={self._size}"
        data = self.crawl(url=url)
        return data

    def turn_result_to_extract_data(self, data) -> dict:
        output = data['result']['review_images_info']
        for i in output:
            i['activity_id'] = self._activity_id
        return output

    def get_content_count(self, data) -> int:
        return data['result']['reviews_count']

    def execute(self):
        for activity_id in self._activity_ids:
            self._activity_id = activity_id
            self.flip_page(self.crawl_content, self.extract_data,
                           self.get_content_count, self.turn_result_to_extract_data)

        return self.extract_data


# print([t['activity_id'] for t in test.execute()[0]])
# activity_ids = [
#     58082, 51850]

# test = Review_Crawler(activity_ids=activity_ids, size=50)
# result = test.execute()
# print(len(result))
# print([t['activity_id'] for t in test.execute()()[0]])
