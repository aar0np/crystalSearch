import os, sys

from astrapy.db import AstraDB
from sentence_transformers import SentenceTransformer
from matplotlib import pyplot as plt
from matplotlib import image as mpimg
from PIL import Image

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

if (len(sys.argv) < 1):
	print("You must provide an image file name.\n astrapySearchByImagepy <image>")
	exit()

# get image and generate embedding
imageName=sys.argv[1]
img_emb = model.encode(Image.open(imageName))
print(img_emb)

##show image
#simage = mpimg.imread(imageName)
#plt.imshow(simage)
#plt.show()

# search by image
results = col.vector_find(img_emb.tolist(), limit=3, fields={"text", "$vector"})

for result in results:
	image = mpimg.imread(IMAGE_DIR + result["text"])
	print(result["text"])
	plt.imshow(image)
	plt.show()
