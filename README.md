
Reference:
1. [MongoDB Schema Design Best Practices](https://www.youtube.com/watch?v=QAqK-R9HUhc&ab_channel=MongoDB)
2.[Load資料到csv with pandas](https://stackoverflow.com/questions/17805304/how-can-i-load-data-from-mongodb-collection-into-pandas-dataframe)


把 schema 設計出來，ETL串起來，airflow檔案可以在本地端跑就行了，(airflow run?) 
看是否可以minikube連到本地端的

### data model
- activity
   - activity(upsert)
- review
   -review_image  (upsert)
   - image也要獨立一張表(upsert)


以review的表來說
airflow 流程:
<!-- 1. python -> create schema -->
1. crawler and dump to mongodb (包成container)
   1.  update to replace (load)
   review需要的activity用airflow的傳遞
2. mongodb find and output to csv and load to github (使用command)
https://docs.mongodb.com/manual/reference/method/db.collection.findOneAndReplace/#mongodb-method-db.collection.findOneAndReplace


- [ ] 在airflow使用的mysql docker-compose run
- [ ] 

```
#!/usr/bin/env python3
#-*- coding: utf-8 -*-

# import PyMongo and a few of its classes
from pymongo import MongoClient, ASCENDING, DESCENDING

# create a client instance of MongoClient
mongo_client = MongoClient("mongodb://localhost:27017")

# very simple create_index()
col.create_index("an_index")

# create an index in descending order
resp = col.create_index([ ("field_to_index", -1) ])
print ("index response:", resp)

# create an index in ASCENDING order
resp = col.create_index([ ("field_to_index", ASCENDING) ])
print ("index response:", resp)

# create a compund index
resp = col.create_index(
[
("field_to_index", 1),
("second_field_indexed", DESCENDING)
]
)

print ("index response:", resp) 
```