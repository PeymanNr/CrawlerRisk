import json
from abc import ABC, abstractmethod
from mongo import MongoDatabase


class StroageAbstract(ABC):

    @abstractmethod
    def store(self, data, *args):
        pass

    @abstractmethod
    def load(self):
        pass


class MongoStorage(StroageAbstract):
    def __init__(self):
        self.mongo = MongoDatabase()

    def store(self, data, collection, *args):
        collection = getattr(self.mongo.database, collection)
        if isinstance(data, list) and len(data) > 1:
            collection.insert_many(data)
        else:
            collection.insert_one(data)

    def load(self):
        # collection = self.mongo.database.get(collection_name)
        # if filter_data is not None:
        #     data = collection.find(filter_data)
        # else:
        #     data = collection.find()
        # return data
         return self.mongo.database.advertisements_links.find({'flag': False})
    def update_flag(self, data):
        self.mongo.database.advertisements_links.find_one_and_update(
            {'_id': data['_id']},  {'$set': {'flag': True}}
        )


class FileStorage(StroageAbstract):

    def store(self, data, filename, *args):
        with open(f'storelist/adv/{filename}.json', 'w') as f:
            f.write(json.dumps(data))
        print(f'storelist/adv/{filename}.json')

    def load(self):
        with open('storelist/adv/advertisements_links.json', 'r') as f:
            links = json.loads(f.read())
        return links
