"""
This code provides an abstraction over the pymongo,
mongoDB queries.
It is recommended to call these methods when querying the database
rather than using the pymongo methods.
"""
import os
from typing import Any, Iterable, List, Mapping, Optional, Union
from config import DBX_API_KEY, MONGO_URI
import dropbox

import pymongo
from pymongo.results import (
    DeleteResult,
    InsertManyResult,
    InsertOneResult,
    UpdateResult,
)


class DB:
    # Private variables (DONOT access outside the class)
    _build = os.environ.get("BUILD", "dev")
    try:
        _client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS = 3000)

        if _build == "dev":
            database = _client.attendance_dev
        elif _build == "staging":
            database = _client.attendance_staging
        elif _build == "prod":
            database = _client.attendance

        _client.server_info()   #trigger exception if cannot connect to db

        # dbx = dropbox.Dropbox(DBX_API_KEY)
    except Exception as e:
        print(str(e))




    # The following methods are used when we expect to work with
    # only one document of a collection.
    # These operate on the first document that matches in the collection.
    # Usually, these methods are recommended to use.
    @staticmethod
    def insert_one(collection: str, data: dict) -> InsertOneResult:
        """
        Insert one document to a collection.

        Args:
            collection (str): The collection to insert to
            data (dict): The data to insert

        Returns:
            InsertOneResult: Returns if succesfull else prints error
        """
        try:
            return DB.database[collection].insert_one(data)
        except pymongo.errors.DuplicateKeyError as dupErr:
            raise Exception(
                f"Duplicated data entry for the {collection} collection "
                f"for {dupErr.details['keyValue']}"
            )

    @staticmethod
    def find_one(
        collection: str,
        query: Mapping[str, Any] = None,
        return_values: Union[Mapping[str, bool], List[str]] = None,
    ) -> Optional[Mapping[str, Any]]:
        """
        Find a document which matches the query in the collection.

        Args:
            collection (str): Collection Name
            query (Mapping[str, Any], optional): filter query. Defaults to None.
            return_values (Union[Mapping[str, bool], List[str]], optional):
                The keys to return. Defaults to None.

        Returns:
            Optional[Mapping[str, Any]]: Returns the document if found else None
        """
        return DB.database[collection].find_one(query, return_values)




    @staticmethod
    def find_one_and_update(
        collection: str,
        query: Mapping[str, Any],
        data:dict,
        action: str = "$set",
        return_values: Union[Mapping[str, bool], List[str]] = None,
    ) -> Optional[Mapping[str, Any]]:
        """
        Find a document which matches the query in the collection and update it.

        Args:
            collection (str): Collection Name
            query (Mapping[str, Any], optional): filter query. Defaults to None.
            return_values (Union[Mapping[str, bool], List[str]], optional):
                The keys to return. Defaults to None.

        Returns:
            Optional[Mapping[str, Any]]: Returns the document if found else None
        """
        return DB.database[collection].find_one_and_update(query,{action: data}, return_values)

    @staticmethod
    def update_one(
        collection: str,
        query: Mapping[str, Any],
        data: dict,
        action: str = "$set",
        array_filters: list = None,
    ) -> UpdateResult:
        """
         Update the first document which matches the query with the new data.

        Args:
            collection (str): collection name to update
            query (Mapping[str, Any]): A  filter query that matches
                 the document to update.
            data (dict): The modifications to apply.
            action (str, optional): mongo action to perform.
                Currently tested for "$set", "$push", "$addToSet". Defaults to "$set".
            array_filters (list, optional): A list of filters specifying which
                array elements an update should apply. Defaults to None.

        Returns:
            UpdateResult: Information about updated document
        """
        return DB.database[collection].update_one(
            query, {action: data}, array_filters=array_filters
        )

    @staticmethod
    def update_one_multiple_actions(
        collection: str,
        query: Mapping[str, Any],
        actionData: dict,
        array_filters: list = None,
    ) -> UpdateResult:
        """
        Similar to update_one but can perform more than one action as specified
        in the actionData dictionary.

        Args:
            collection (str): collection name
            query (Mapping[str, Any]): A  filter query that matches
                 the document to update.
            actionData (dict): The modifications to apply.
            array_filters (list, optional): A list of filters specifying which
                array elements an update should apply. Defaults to None.

        Returns:
            UpdateResult: Information about updated document
        """
        return DB.database[collection].update_one(
            query, actionData, array_filters=array_filters
        )

    @staticmethod
    def delete_one(collection: str, query: Mapping[str, Any]) -> DeleteResult:
        """
        Deletes the first document of the collection which
        matches the query.

        Args:
            collection (str): The collection to delete from
            query (Mapping[str, Any]): The query to find the document

        Returns:
            DeleteResult: Information about deleted document
        """
        return DB.database[collection].delete_one(query)

    # The following methods work on one or more documents of a collection.
    # Usually, we do not use these methods other than find_many.
    # Be careful when you use them.




    @staticmethod
    def find_one_and_delete(collection: str, query: Mapping[str, Any]) -> DeleteResult:
        """
        Deletes the first document of the collection which
        matches the query.

        Args:
            collection (str): The collection to delete from
            query (Mapping[str, Any]): The query to find the document

        Returns:
            DeleteResult: Information about deleted document
        """
        return DB.database[collection].find_one_and_delete(query)

    # The following methods work on one or more documents of a collection.
    # Usually, we do not use these methods other than find_many.
    # Be careful when you use them.

    @staticmethod
    def insert_many(collection: str, data: Iterable[dict]) -> InsertManyResult:
        """
        Inserts more than one document in a collection.

        Args:
            collection (str): Collection to insert to
            data (dict): The data to insert

        Returns:
            InsertManyResult: Information about Insertion
        """
        return DB.database[collection].insert_many(data)

    @staticmethod
    def find_many(
        collection: str,
        query: Mapping[str, Any] = None,
        return_values: Union[Mapping[str, bool], List[str]] = None,
    ) -> pymongo.cursor.Cursor:
        """
        Returns all the documents which match the query
        Args:
            collection (str): Collection Name
            return_values (Union[Mapping[str, bool], List[str]]), optional):
                 The keys to return. Defaults to None.

        Returns:
            pymongo.cursor.Cursor: List like Iterable object
        """
        return DB.database[collection].find(query, return_values)

    @staticmethod
    def update_many(
        collection: str,
        query: Mapping[str, Any],
        data: dict,
        action: str = "$set",
        array_filters: list = None,
    ) -> UpdateResult:
        """
        Update more than one document of the collection that matches the collection
        with the new data

        Args:
            collection (str): Collection to update
            query (Mapping[str, Any]): Query to match
            data (dict): The update data
            action (str, optional): Update Action. Defaults to "$set".
            array_filters (list, optional): A list of filters specifying which
                array elements an update should apply. Defaults to None.

        Returns:
            UpdateResult: Information about the updated documents
        """
        return DB.database[collection].update_many(
            query, {action: data}, array_filters=array_filters
        )

    @staticmethod
    def delete_many(collection: str, query: Mapping[str, Any]) -> DeleteResult:
        """
        Delete many all the documents matching the query
        CAUTION: used only for deleting verification documents

        Args:
            collection (str): Collection to delete from
            query (Mapping[str, Any]): Query to match for the documents

        Returns:
            DeleteResult: Information of delete results
        """
        return DB.database[collection].delete_many(query)

    @staticmethod
    def count(collection: str, query: Mapping[str, Any] = None) -> int:
        """
        Count of number of documents in the collection matching the query

        Args:
            collection (str): The collection to count from
            query (Mapping[str, Any], optional): Query to match. Defaults to None.

        Returns:
            int: COunts matching the query
        """
        return DB.database[collection].count_documents(query or {})

    @staticmethod
    def does_document_exist(collection: str, query: Mapping[str, Any]) -> bool:
        """
        Checks if document exists

        Args:
            collection (str): Collection to check from
            query (Mapping[str, Any]): The query to match

        Returns:
            bool: True if document exists else False
        """
        return bool(DB.database[collection].find_one(query, ["_id"]))

    @staticmethod
    def set_unique(collection: str, keys: Union[List[str], str]) -> bool:
        """
        Make a particular key unique

        Args:
            collection (str): The collection to choose
            keys (Union[List[str], str]): Keys to make as unique index

        Returns:
            bool: Returns if operation completed successfully
        """
        if not isinstance(keys, list):
            keys = [keys]
        return DB.database[collection].create_index(
            [(key, pymongo.ASCENDING) for key in keys], unique=True
        )

    @staticmethod
    def moveData(SourceCollection: str, DestCollection: str, data: Mapping[str, Any]):
        """
        Move from one collection to another

        Args:
            SourceCollection (str): Source Collection
            DestCollection (str): Destination COllection
            data (Mapping[str, Any]): Data to move
        """
        # NOTE: save and remove are deprecated
        DB.database[DestCollection].insert_one(data)
        DB.database[SourceCollection].delete_one(data)

    @staticmethod
    def list_collections() -> List[str]:
        """
        Lists al the collections in the database

        Returns:
            List[str]: List of names of collections in database
        """
        return DB.database.list_collection_names()