import os

from crystalServices import get_crystals_by_image
from crystalServices import get_crystals_by_facets
from flask import Flask, render_template
from webforms import SearchForm

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
    return dict(form=form)

# create search function
@app.route('/search', methods=["POST"])
async def search():
    form = SearchForm()

    search_image = form.search_image.data
    search_image_file = search_image.filename

    # save locally
    search_image.save(os.path.join(basedir, INPUT_IMAGE_DIR, search_image_file))

    # execute vector search in Astra DB
    image_results = await get_crystals_by_image(search_image_file)

    return render_template("search.html", data=image_results, search_image_file=search_image_file)

# create faceting function (left nav drop-downs)
@app.route('/facet', methods=["POST"])
async def facet():
	form = SearchForm()

	chakra = form.chakra_select.data
	birth_month = form.birth_month_select.data
	zodiac_sign = form.zodiac_select.data

	data_results = await get_crystals_by_facets(chakra, birth_month, zodiac_sign)

	return render_template("facet.html", data=data_results, chakra=chakra, birth_month=birth_month, zodiac_sign=zodiac_sign)
