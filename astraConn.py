import os

from astrapy.db import AstraDB

# Astra connection
ASTRA_DB_APPLICATION_TOKEN = os.environ.get("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_API_ENDPOINT= os.environ.get("ASTRA_DB_API_ENDPOINT")

# global cache variables to re-use a single Session
db = None
collection = None

def init_collection(table_name):
    global db
    global collection

    if db is None:
        db = AstraDB(
            token=ASTRA_DB_APPLICATION_TOKEN,
            api_endpoint=ASTRA_DB_API_ENDPOINT,
        )
    
    collection = db.collection(table_name)

async def get_by_vector(table_name, vector_embedding, limit=1):
    init_collection(table_name)

    results = collection.vector_find(vector_embedding.tolist(), limit=limit, fields={"text","$vector"})
    return results

async def get_by_id(table_name, id):
    init_collection(table_name)

    result = collection.find_one(filter={"_id": id})
    return result

async def get_by_metadata(table_name, chakra, birth_month, zodiac_sign):
    init_collection(table_name)

    conditions = []

    print(chakra)
    print(birth_month)
    print(zodiac_sign)

    if chakra != "--Chakra--":
        condition_chakra = {"chakra": {"$in": [chakra]}}
        conditions.append(condition_chakra)
    if birth_month != "--Birth Month--":
        condition_birth_month = {"birth_month": birth_month}
        conditions.append(condition_birth_month)
    if zodiac_sign != "--Zodiac Sign--":
        condition_zodiac_sign = {"zodiac_sign": zodiac_sign}
        conditions.append(condition_zodiac_sign)

    #crystal_filter = {"$and": [{"$and": [{"chakra": {"$in": [chakra]}}, {"birth_month": birth_month}]}, {"zodiac_sign": zodiac_sign}]}
    crystal_filter = ""

    if len(conditions) > 2:
        crystal_filter = {"$and": [{"$and": [conditions[0], conditions[1]]}, conditions[2]]}
    elif len(conditions) > 1:
        crystal_filter = {"$and": [conditions[0], conditions[1]]}
    elif len(conditions) > 0:
        crystal_filter = conditions[0]
    else:
        return 

    results = collection.find(crystal_filter)
    return results
