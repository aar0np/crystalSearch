from crystalServices import get_crystal_by_image
from crystalServices import get_crystal_by_id_list
from crystalServices import get_crystals_by_facets
from flask import Flask, render_template
from webforms import SearchForm #, ZODIAC_CHOICES, BIRTH_MONTH_CHOICES, CHAKRA_CHOICES

import os

app = Flask(__name__)
app.config.from_object('config.DevConfig')

INPUT_IMAGE_DIR = "static/input_images/"
basedir = os.path.abspath(os.path.dirname(__file__))

@app.route('/')
def index():
    return render_template('main.html')

# Pass stuff to navbar
@app.context_processor
def base():
    form = SearchForm()
    #nav_form = FacetForm()
    return dict(form=form)
    #return dict(form=form, nav_form=nav_form)

# create search function
@app.route('/search', methods=["POST"])
async def search():
    form = SearchForm()

    #if form.searched.data != "":
    	 # (old text search code)
    #    # execute vector search in Astra DB
    #    #response = await get_car_by_text(form.searched.data)
    #    return render_template("search.html", form=form, searched=None, search_image_file="noImage.png")
    #elif form.search_image.data != "":
    search_image = form.search_image.data
    search_image_file = search_image.filename
    #print(search_image)
    #print(search_image_file)
    # save locally
    search_image.save(os.path.join(basedir, INPUT_IMAGE_DIR, search_image_file))
    # execute vector search in Astra DB
    image_results = await get_crystal_by_image(search_image_file)
    data_results = await get_crystal_by_id_list(image_results)
    return render_template("search.html", images=image_results, data=data_results, search_image_file=search_image_file)

# create faceting function (left nav drop-downs)
@app.route('/facet', methods=["POST"])
async def facet():
	form = SearchForm()
	#print(f"form={form.data}")

	chakra = form.chakra_select.data
	birth_month = form.birth_month_select.data
	zodiac_sign = form.zodiac_select.data

	#print(f"chakra={chakra}")
	#print(f"birth_month={birth_month}")
	#print(f"zodiac_sign={zodiac_sign}")

	data_results = await get_crystals_by_facets(chakra, birth_month, zodiac_sign)
	#print(f"data_results={data_results}")

	return render_template("facet.html", data=data_results, chakra=chakra, birth_month=birth_month, zodiac_sign=zodiac_sign)
