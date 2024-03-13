import os

from astrapy.db import AstraDB
from sentence_transformers import SentenceTransformer
from matplotlib import pyplot as plt
from matplotlib import image as mpimg

# Astra connection
ASTRA_DB_APPLICATION_TOKEN = os.environ.get("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_API_ENDPOINT= os.environ.get("ASTRA_DB_API_ENDPOINT")

db = AstraDB(
    token=ASTRA_DB_APPLICATION_TOKEN,
    api_endpoint=ASTRA_DB_API_ENDPOINT,
)
col = db.collection("crystal_images")

model = SentenceTransformer('clip-ViT-B-32')
IMAGE_DIR = "static/images/"
user_input = "blue agate"

while user_input != "exit":
    text_emb = model.encode(user_input)
    results = col.vector_find(text_emb.tolist(), limit=1, fields={"text", "$vector"})

    for result in results:
        #print(result)
        plt.title(result["text"])
        image = mpimg.imread(IMAGE_DIR + result["text"])
        plt.imshow(image)
        plt.show()

        user_input = input("Next search? ")
