import json
import string
from typing import TypeVar, List
import pymongo
from pymongo.database import Database

from InfraSracture.Infra.dal.data_rep import DataRep
from InfraSracture.Infra.dal.json_encoder.json_encoder import CustomEncoder
from InfraSracture.objects.data_classes.product_data import Product


class MongoDbAccess:
    T = TypeVar('T')

    @staticmethod
    def initialize_mongo_client() -> Database:
        client = pymongo.MongoClient(DataRep.mongo_connection_string)
        database_name = DataRep.mongo_connection_string.split("net")[1].replace("/", "")
        database = client[database_name]
        return database

    @staticmethod
    def select_all_documents_from_table(table_name: string, T) -> List[T]:
        database = MongoDbAccess.initialize_mongo_client()
        collection = database[table_name]
        all_documents = collection.find()
        table_as_object = []

        for document in all_documents:
            json_str = json.dumps(document, cls=CustomEncoder)
            load = json.loads(json_str)
            product_instance = T(**load)
            table_as_object.append(product_instance)
        return table_as_object

