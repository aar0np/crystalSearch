import csv
import json

from os import path, environ
from dotenv import load_dotenv
from PIL import Image
from astrapy.db import AstraDB
from sentence_transformers import SentenceTransformer

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

# Astra connection
ASTRA_DB_APPLICATION_TOKEN = environ.get("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_API_ENDPOINT= environ.get("ASTRA_DB_API_ENDPOINT")

db = AstraDB(
    token=ASTRA_DB_APPLICATION_TOKEN,
    api_endpoint=ASTRA_DB_API_ENDPOINT,
)

# create "collection"
col = db.create_collection("crystal_data", dimension=512, metric="cosine")

model = SentenceTransformer('clip-ViT-B-32')
IMAGE_DIR = "static/images/"
CSV = "gemstones_and_chakras.csv"

with open(CSV) as csvHandler:
    crystalData = csv.reader(csvHandler)
    # skip header row
    next(crystalData)

    for line in crystalData:

        image = line[1]
       	# Only load crystals with images
        if image != "" and path.exists(IMAGE_DIR + image):

            # map columns
            gemstone = line[0]
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

        	# reformat chakras to be more JSON-friendly
            chakras = chakras.replace(', ','","')

            # split out minimum and maximum mohs hardress
            mh_list = mohs_hardness.split('-')
            mohs_min_hardness = 1.0
            mohs_max_hardness = 9.0
            if mh_list[0][0:4] != 'Vari':
                mohs_min_hardness = mh_list[0]
                mohs_max_hardness = mh_list[0]
                if len(mh_list) > 1:
                    mohs_max_hardness = mh_list[1]

            metadata = (f"gemstone: {gemstone}")
            text = (f"gemstone: {gemstone}| alternate name: {alt_name}| physical attributes: {phys_attributes}| emotional attributes: {emot_attributes}| metaphysical attributes: {meta_attributes}| origin: {origin}| maximum mohs hardness: {mohs_max_hardness}| minimum mohs hardness: {mohs_min_hardness}")

            img_emb = model.encode(Image.open(IMAGE_DIR + image))
            strJson = (f'{{"_id":"{image}","text":"{text}","chakra":["{chakras}"],"birth_month":"{birth_month}","zodiac_sign":"{zodiac_sign}","$vector":{str(img_emb.tolist())}}}')
            doc = json.loads(strJson)
            col.insert_one(doc)
