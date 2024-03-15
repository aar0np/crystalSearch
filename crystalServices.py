import json
from astraConn import get_by_vector
from astraConn import get_by_id
from astraConn import get_by_metadata
from sentence_transformers import SentenceTransformer
from PIL import Image
import os

INPUT_IMAGE_DIR = "static/input_images/"
IMAGES_COLLECTION_NAME = "crystal_images"
DATA_COLLECTION_NAME = "crystal_data"
model = None

async def get_crystal_by_image(file_path):
    global model

    if model is None:
        model = SentenceTransformer('clip-ViT-B-32')

    # load image from file_path and generate embedding
    img_emb = model.encode(Image.open(INPUT_IMAGE_DIR + file_path))

    # execute vector search
    results = await get_by_vector(IMAGES_COLLECTION_NAME, img_emb, 3)
    images = []

    for image_count, result in enumerate(results):
    	images.append(result['text'])

    return images

async def get_crystal_by_id_list(id_list):
	results = {}
	for idx in range(len(id_list)):
		crystal_data = await get_by_id(DATA_COLLECTION_NAME, id_list[idx])
		#print(crystal_data['data']['document']['text'])
		results[id_list[idx]] = parse_crystal_data(crystal_data['data']['document']['text'])

	return results

async def get_crystals_by_facets(chakra, birth_month, zodiac_sign):
	results = {}
	crystals_data = await get_by_metadata(DATA_COLLECTION_NAME, chakra, birth_month, zodiac_sign)

	if crystals_data is not None:
		for crystal in crystals_data['data']['documents']:
			#print(crystal)
			id = crystal['_id']
			results[id] = parse_crystal_data(crystal['text'])

	return results

def parse_crystal_data(crystal_data):
	crystal_properties = crystal_data.split("|")

	crystal = Crystal()
	crystal.name = crystal_properties[0].split(": ")[1]
	crystal.alternate_name = crystal_properties[1].split(": ")[1]
	crystal.chakra = crystal_properties[2].split(": ")[1]
	crystal.physical_attributes = crystal_properties[3].split(": ")[1]
	crystal.emotional_attributes = crystal_properties[4].split(": ")[1]
	crystal.metaphysical_attributes = crystal_properties[5].split(": ")[1]
	crystal.origin = crystal_properties[6].split(": ")[1]
	crystal.birth_month = crystal_properties[7].split(": ")[1]
	crystal.zodiac_sign = crystal_properties[8].split(": ")[1]
	crystal.maximum_mohs_hardness = crystal_properties[9].split(": ")[1]
	crystal.minimum_mohs_hardness = crystal_properties[10].split(": ")[1]

	return crystal

class Crystal:
	name: str
	alternate_name: str
	chakra: str
	physical_attributes: str
	emotional_attributes: str
	metaphysical_attributes: str
	origin: str
	birth_month: str
	zodiac_sign: str
	maximum_mohs_hardness: int
	minimum_mohs_hardness: int
