from pymongo import MongoClient

LOCAL_HOST = "mongodb://localhost:27017"
DATABASE_NAME = "phone_book_db"


class MongoDBConnection:
    def __init__(self, host=LOCAL_HOST, db_name=DATABASE_NAME):
        self.client = MongoClient(host)
        self.db = self.client[db_name]

    def get_collection(self, collection_name):
        return self.db[collection_name]


def mongodb_query_execute(collection_name, query_type, data=None, filter=None, update_data=None, projection=None):
    connection = MongoDBConnection()
    collection = connection.get_collection(collection_name)

    if query_type == "find":
        if projection:
            return collection.find({}, projection)
        elif filter:
            return collection.find({filter})
        else:
            return collection.find()
    elif query_type == "find_one":
        return collection.find_one(filter)
    elif query_type == "insert_one":
        if data is not None:
            return collection.insert_one(data)
        else:
            raise ValueError("Data is required to insert")
    elif query_type == "insert_many":
        if data is not None:
            return collection.insert_many(data)
        else:
            raise ValueError("Data is required to insert")
    elif query_type == "update_one":
        if filter is not None and update_data is not None:
            return collection.update_one(filter, update_data)
        else:
            raise ValueError("Filter and Updated_data are required to update")
    elif query_type == "update_many":
        if filter is not None and update_data is not None:
            return collection.update_many(filter, update_data)
        else:
            raise ValueError("Filter and Update_data are required to update")
    elif query_type == "delete_one":
        if filter is not None:
            return collection.delete_one(filter)
        else:
            raise ValueError("Filter is required to delete")
    else:
        raise ValueError("Invalid query_type provided.")
