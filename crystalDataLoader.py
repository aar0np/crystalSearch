import csv
import os
import json

from PIL import Image
from astrapy.db import AstraDB
from langchain.embeddings.openai import OpenAIEmbeddings

# Astra connection
ASTRA_DB_APPLICATION_TOKEN = os.environ.get("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_API_ENDPOINT= os.environ.get("ASTRA_DB_API_ENDPOINT")

# initialize the OpenAI chat model for embeddings
embeddings = OpenAIEmbeddings()

db = AstraDB(
    token=ASTRA_DB_APPLICATION_TOKEN,
    api_endpoint=ASTRA_DB_API_ENDPOINT,
)
# create "collection" (vector-enabled table)
col = db.create_collection("crystal_data", dimension=1536, metric="cosine")

#IMAGE_DIR = "images/"
CSV = "gemstones_and_chakras.csv"

with open(CSV) as csvHandler:
    crystalData = csv.reader(csvHandler)
    first = True

    for line in crystalData:

        # skip header line
        if first == False:
            # map columns
            gemstone = line[0]
            image = line[1]
            alt_name = line[2]
            chakras = line[3]
            phys_attributes = line[4]
            emot_attributes = line[5]
            meta_attributes = line[6]
            origin = line[7]
            description = line[8]
            birth_month = line[9]
            zodiac_sign = line[10]
            mohs_hardness = line[11]

            # split out minimum and maximum mohs hardress
            mh_list = mohs_hardness.split('-')
            mohs_min_hardness = 1.0
            mohs_max_hardness = 9.0
            if mh_list[0][0:4] != 'Vari':
                mohs_min_hardness = mh_list[0]
                mohs_max_hardness = mh_list[0]
                if len(mh_list) > 1:
                    mohs_max_hardness = mh_list[1]

            metadata = {f"gemstone: {gemstone}"}
            text = (f"gemstone: {gemstone}| alternate name: {alt_name}| chakra: {chakras}| physical attributes: {phys_attributes}| emotional attributes: {emot_attributes}| metaphysical attributes: {meta_attributes}| origin: {origin}| birth month: {birth_month}| zodiac sign: {zodiac_sign}| maximum mohs hardness: {mohs_max_hardness}| minimum mohs hardness: {mohs_min_hardness}")
            text_emb = embeddings.embed_query(text)
            print(text)

            crystal_id = image
            if crystal_id == "":
                # every crystal should have an image
                crystal_id = gemstone
                # don't load data for crystals without images
            else:
                chakras = chakras.replace(', ','","')
                strJson = '{"_id":"' + crystal_id + '","text":"' + text + '","chakra":["' + chakras + '"],"birth_month":"' + birth_month + '","zodiac_sign":"' + zodiac_sign + '","$vector":' + str(text_emb) + '}'
                #print(strJson)
                doc = json.loads(strJson)
                col.insert_one(doc)
        else:
            first = False
