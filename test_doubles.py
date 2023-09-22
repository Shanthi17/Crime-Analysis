from pymongo import MongoClient
import mongomock
import os
import unittest
from unittest.mock import patch


class TestCRUDOperations(unittest.TestCase):

    def setUp(self):
        self.client= MongoClient("mongodb+srv://"+ os.environ['username'] +":"+ os.environ['password'] +"@cluster0.kyfkech.mongodb.net/Crime")
        self.db = self.client.Crime
        self.collection = self.db.Offense_Codes
        self.mock_collection = mongomock.MongoClient().db.collection
        self.patcher = patch.object(self.db, 'collection', self.mock_collection)
        self.patcher.start()

    def test_create_document(self):
        # test object
        document = {"OBJECTID":{"$numberInt":"301"},"OFFENSE_CODE":{"$numberInt":"9999"},"OFFENSE_CODE_EXTENSION":{"$numberInt":"1"},"OFFENSE_TYPE_ID":"test","OFFENSE_TYPE_NAME":"test","OFFENSE_CATEGORY_ID":"test","OFFENSE_CATEGORY_NAME":"test","IS_CRIME":{"$numberInt":"1"},"IS_TRAFFIC":{"$numberInt":"0"}}
        result = self.collection.insert_one(document)
        self.assertTrue(result.inserted_id is not None)

    def test_read_document(self):
        # Test reading a document from the collection
        result = self.collection.find_one({'OFFENSE_TYPE_ID':"test"})
        query_result = int(result['OBJECTID']['$numberInt'])
        self.assertEqual(query_result, 301)

if __name__ == '__main__':
    unittest.main()