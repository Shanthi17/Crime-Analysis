from source.dateparser import date_sorter

def parse_input(form):
        headers = { 'fid': "_id",
                    'fii': "incident_id",
                    'foi': "offense_id",
                    'foc': "OFFENSE_CODE",
                    'foce': "OFFENSE_CODE_EXTENSION",
                    'foti': "OFFENSE_TYPE_ID",
                    'foci': "OFFENSE_CATEGORY_ID",
                    'ffod': "FIRST_OCCURRENCE_DATE",
                    'flod': "LAST_OCCURRENCE_DATE",
                    'frd': "REPORTED_DATE",
                    'fia': "INCIDENT_ADDRESS",
                    'fgx': "GEO_X",
                    'fgy': "GEO_Y",
                    'fglong': "GEO_LON",
                    'fglat': "GEO_LAT",
                    'fdi': "DISTRICT_ID",
                    'fpi': "PRECINCT_ID",
                    'fni': "NEIGHBORHOOD_ID",
                    'fic': "IS_CRIME",
                    'fit': "IS_TRAFFIC",
                    'fvc': "VICTIM_COUNT" }
        queryterms = { 'id': "_id",
                    'ii': "incident_id",
                    'oi': "offense_id",
                    'oc': "OFFENSE_CODE",
                    'oce': "OFFENSE_CODE_EXTENSION",
                    'oti': "OFFENSE_TYPE_ID",
                    'oci': "OFFENSE_CATEGORY_ID",
                    'fod': "FIRST_OCCURRENCE_DATE",
                    'lod': "LAST_OCCURRENCE_DATE",
                    'rd': "REPORTED_DATE",
                    'ia': "INCIDENT_ADDRESS",
                    'gx': "GEO_X",
                    'gy': "GEO_Y",
                    'glong': "GEO_LON",
                    'glat': "GEO_LAT",
                    'di': "DISTRICT_ID",
                    'pi': "PRECINCT_ID",
                    'ni': "NEIGHBORHOOD_ID",
                    'ic': "IS_CRIME",
                    'it': "IS_TRAFFIC",
                    'vc': "VICTIM_COUNT" }
        queryfilters, formfilters = [], []
        for item in form:
            if form[item] == 'y' and item in headers:
                formfilters.append(headers[item])
            elif item in queryterms:
                if item in ['vc','ii','oc','oce','gx','gy','glong','glat','di','pi','ic','it']:
                    queryfilters.append({queryterms[item]: int(form[item])})
                else:
                    queryfilters.append({queryterms[item]: form[item]})
        return formfilters,queryfilters

# def col_join_on_crime(mongodb, col1string, col2string):
#     db = mongodb['Crime']
    
#     return db[col2string].aggregate([
#     {
#         "$lookup": {
#             "from": col1string,
#             "localField": "OFFENSE_CODE",
#             "foreignField": "OFFENSE_CODE",
#             "as": "linked_crime"
#             }
#     },
#     {
#         "$unwind": "$linked_crime"
#     },
#     {
#         "$project": {
#             'crime_name': { '$cond': [ { '$eq': [ '$OFFENSE_TYPE_NAME', '$linked_crime.crime_name' ] }, 1, 0] } 
#             }
#     },
#     {'$match' : { 'crime_name' : 1}}
#     ])

def add_crime_ids(query_attributes):
    query_attributes.append('OFFENSE_CODE')
    query_attributes.append('OFFENSE_CODE_EXTENSION')
    return query_attributes

def add_geo_attr(query_attributes):
    query_attributes.append('GEO_LON')
    query_attributes.append('GEO_LAT')
    return query_attributes

def rem_attrs(dicts, listofattributes):
    for item in dicts:
        for attribute in listofattributes:
            item.pop(attribute, None)
    return dicts

def ret_dict(returnfields):
    if returnfields is not None:
        return_dict = {}
        return_dict['_id'] = False
        for item in returnfields:
            return_dict[item] = True
    else:
        return_dict = None
    return return_dict

def query_parser(query_results, returnfields):
    query_list = []
    for record in query_results:
        query_list.append(record)

    if "FIRST_OCCURRENCE_DATE" in returnfields:
        query_list = date_sorter(query_list)
    
    return query_list

def dict_match_on_crime(mongodb, query_list, query_attributes):
    db = mongodb['Crime']
    col = db['Offense_Codes']

    return_dict = ret_dict(query_attributes)
    return_dict['OFFENSE_TYPE_NAME'] = True

    for incident_dict in query_list:
        code = int(incident_dict['OFFENSE_CODE'])
        ext = int(incident_dict['OFFENSE_CODE_EXTENSION'])
        queryfilters = [{'OFFENSE_CODE': code}, {'OFFENSE_CODE_EXTENSION': ext}]
    
        query = { '$and': [item for item in queryfilters] }
        crime_code_result = col.find(query, return_dict).limit(1)
        crime_code_result = query_parser(crime_code_result, ['OFFENSE_CODE', 'OFFENSE_CODE_EXTENSION', 'OFFENSE_TYPE_NAME'])
        incident_dict['OFFENSE_TYPE_NAME'] = crime_code_result[0]['OFFENSE_TYPE_NAME']


    return query_list

# crime_db = ct.MongoConnector()
# mongo_db = crime_db.startup_db_client()
# print(col_join_on_crime(mongo_db,'Denver_Crime','Offense_Codes'))