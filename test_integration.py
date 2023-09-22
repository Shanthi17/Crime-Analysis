import unittest
import psycopg2
import os
from pymongo import MongoClient

from dotenv import load_dotenv
load_dotenv()

# Test Connection with PostgreSQL
class TestDatabaseConnection(unittest.TestCase):

    def setUp(self):
        self.conn = psycopg2.connect(
            dbname=os.environ['db_name'],
            user=os.environ['user'],
            password=os.environ['db_password'],
            host=os.environ['host'],
            port=os.environ['port']
        )

    def tearDown(self):
        self.conn.close()

    def test_database_connection(self):
        self.assertIsNotNone(self.conn)

    def test_table_exists(self):
        self.cur = self.conn.cursor()
        table_names = ['userdata', 'ucr_crime_1975_2015']
        for table_name in table_names:
            self.cur.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_name=%s", [table_name])
            self.assertTrue(self.cur.fetchone()[0] == 1, f"Table '{table_name}' does not exist")


# Test Connection with PostgreSQL
class TestMongoDB(unittest.TestCase):
    def setUp(self):
        self.client = MongoClient("mongodb+srv://"+ os.environ['username'] +":"+ os.environ['password'] +"@cluster0.kyfkech.mongodb.net/Crime")
        self.db = self.client['Crime']

    def test_database_connection(self):
        # Check if the connection to the database is successful
        self.assertTrue(self.client is not None)

    def test_denver_crime_exists(self):
        # Check if the collection 'test_collection' exists
        self.assertTrue('Denver_Crime' in self.db.list_collection_names())

    def test_offense_codes_exists(self):
        # Check if the collection 'test_collection' exists
        self.assertTrue('Offense_Codes' in self.db.list_collection_names())

    def tearDown(self):
        self.client.drop_database('test_db')


class TestCRUDOperations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = MongoClient("mongodb+srv://"+ os.environ['username'] +":"+ os.environ['password'] +"@cluster0.kyfkech.mongodb.net/Crime")
        cls.db = cls.client.Crime
        cls.collection = cls.db.Denver_Crime

    @classmethod
    def tearDownClass(cls):
        cls.client.close()


    def setUp(self):
        self.document_id = self.collection.insert_one({"incident_id":{"$numberInt":"2017421901"},"offense_id":{"$numberDouble":"2017421909299901.0"},"OFFENSE_CODE":{"$numberInt":"2999"},"OFFENSE_CODE_EXTENSION":{"$numberInt":"0"},"OFFENSE_TYPE_ID":"criminal-mischief-other","OFFENSE_CATEGORY_ID":"public-disorder","FIRST_OCCURRENCE_DATE":"6/25/2017 8:40:00 PM","LAST_OCCURRENCE_DATE":{"$numberDouble":"NaN"},"REPORTED_DATE":"6/27/2017 7:01:00 PM","INCIDENT_ADDRESS":"2920 W 32ND AVE","GEO_X":{"$numberInt":"3133773"},"GEO_Y":{"$numberInt":"1702660"},"GEO_LON":{"$numberDouble":"-105.0241665"},"GEO_LAT":{"$numberDouble":"39.7616457"},"DISTRICT_ID":"1","PRECINCT_ID":{"$numberInt":"113"},"NEIGHBORHOOD_ID":"highland","IS_CRIME":{"$numberInt":"1"},"IS_TRAFFIC":{"$numberInt":"0"},"VICTIM_COUNT":{"$numberInt":"1"}}).inserted_id

    def test_create_document(self):
        document = {"incident_id":{"$numberInt":"2017421900"},"offense_id":{"$numberDouble":"2017421909299900.0"},"OFFENSE_CODE":{"$numberInt":"2999"},"OFFENSE_CODE_EXTENSION":{"$numberInt":"0"},"OFFENSE_TYPE_ID":"criminal-mischief-other","OFFENSE_CATEGORY_ID":"public-disorder","FIRST_OCCURRENCE_DATE":"6/25/2017 8:40:00 PM","LAST_OCCURRENCE_DATE":{"$numberDouble":"NaN"},"REPORTED_DATE":"6/27/2017 7:01:00 PM","INCIDENT_ADDRESS":"2920 W 32ND AVE","GEO_X":{"$numberInt":"3133773"},"GEO_Y":{"$numberInt":"1702660"},"GEO_LON":{"$numberDouble":"-105.0241665"},"GEO_LAT":{"$numberDouble":"39.7616457"},"DISTRICT_ID":"1","PRECINCT_ID":{"$numberInt":"113"},"NEIGHBORHOOD_ID":"highland","IS_CRIME":{"$numberInt":"1"},"IS_TRAFFIC":{"$numberInt":"0"},"VICTIM_COUNT":{"$numberInt":"1"}}
        result = self.collection.insert_one(document)
        self.assertTrue(result.inserted_id is not None)

    def test_read_document(self):
        #document = self.collection.find_one({"_id":ObjectId('64547060fc183c846d93ca5d')})
        document = self.collection.find_one({"_id": self.document_id})
        query_result = int(document['incident_id']['$numberInt'])
        self.assertEqual(query_result, 2017421901)

    def test_update_document(self):
        result = self.collection.update_one({"_id": self.document_id}, {"$set": {"VICTIM_COUNT": 2}})
        self.assertEqual(result.modified_count, 1)

    def test_delete_document(self):
        result = self.collection.delete_one({"_id": self.document_id})
        self.assertEqual(result.deleted_count, 1)

