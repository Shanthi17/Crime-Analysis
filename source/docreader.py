from source.queries import ret_dict, query_parser
from pprint import pprint

class read_doc():
    def __init__(self) -> None:
        #self.doc = pd.read_csv('data/raw/crime.csv', encoding= 'ISO-8859-1').to_dict()

        pass
    def db_insert(self):
        pass


class mongo_read(read_doc):
    def __init__(self) -> None:
        super().__init__()

    # def csv_to_json(self, filename):
    #     data = pd.read_csv(filename)
    #     return data.to_dict()

    # def print_records(self, query_results):
    #     for i, record in enumerate(query_list):
    #         print(f'Record number: {i}')
    #         pprint(record)
    #         print('\n')
    #     df = pd.DataFrame.from_dict(query_results)
    #     print(df)

    # def db_insert_csv(self, filepath, dbname, colname, mongo_db):
    #     datadict = pd.read_csv(filepath, encoding= 'ISO-8859-1').to_dict()
    #     header = [header for header in datadict]
    #     db = mongo_db[dbname]
    #     col = db[colname]
    #     for i in datadict[header[0]]:
    #         row = {}
    #         for j in header:
    #             row[j] = datadict[j][i] ##{'Incident_number': 2134556}
    #         col.insert_one(row)

    def db_find(self, mongo_connect, dbname, colname, query, returnfields = None):
        return_dict = ret_dict(returnfields)
        
        if "FIRST_OCCURRENCE_DATE" in returnfields:
            sort_param = "FIRST_OCCURRENCE_DATE"
        elif len(returnfields) == 0:
            return []
        else:
            sort_param = returnfields[0]

        db = mongo_connect[dbname]
        col = db[colname]

        query_results = col.find(query, return_dict).sort(sort_param).limit(50)
        
        query_list = query_parser(query_results, returnfields)

        return query_list


#crime_db = ct.MongoConnector()
#mongo_db = crime_db.startup_db_client()
#crime_codes = mongo_read()
#query = { '$and': [{"GEO_LAT": 39.7616457} , {"GEO_LON": -105.0241665}] }
# query = { 'OFFENSE_CODE': 3501, 'OFFENSE_CODE_EXTENSION': 0}
#query_attributes = ['OFFENSE_TYPE_ID', 'FIRST_OCCURRENCE_DATE', 'INCIDENT_ADDRESS', 'NEIGHBORHOOD_ID']
# query_attributes = None
# query = { 'incident_id': 2017421909} 
#test=crime_codes.db_insert_csv('data/raw/crime.csv', 'Crime', 'Denver_Crime', mongo_db)
#test1=crime_codes.db_insert_csv('data/offense_codes.csv', 'Crime', 'Offense_Codes', mongo_db)
#query_list = crime_codes.db_find(mongo_db, 'Crime', 'Denver_Crime', query, query_attributes)

# crime_codes.print_records(query_list)

#df = pd.DataFrame(query_list)
#print(df)
## figure out how to sort by attribute




